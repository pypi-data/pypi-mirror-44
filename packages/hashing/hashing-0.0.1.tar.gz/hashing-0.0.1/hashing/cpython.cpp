// Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include "aquahash.h"

const Py_ssize_t GIL_MIN_SIZE = 4096;

#define min(a, b) \
  ({__typeof__ (a) _a = (a); \
    __typeof__ (b) _b = (b); \
    _a < _b ? _a : _b; })


typedef struct {
  PyObject_HEAD;
  AquaHash state;
  PyThread_type_lock lock;
} Aquahash;


PyDoc_STRVAR(hashing_doc, "Various hashing functions.");


static PyObject *Aquahash_new(PyTypeObject *type, PyObject *args, PyObject *kwargs) {

  Aquahash *self = NULL;
  Py_buffer salt = {.buf=NULL, .obj=NULL, .len=0};

  static const char * const _keywords[] = {"salt", NULL};
  static _PyArg_Parser _parser = {"|$s*:Aquahash", _keywords, 0};

  if (!_PyArg_ParseTupleAndKeywordsFast(args, kwargs, &_parser, &salt)) return NULL;
  __m128i salt_val = {0, 0};
  if (salt.len) memcpy(&salt_val, salt.buf, min(salt.len, (long)sizeof(salt_val)));
  if (salt.obj) PyBuffer_Release(&salt);

  self = (Aquahash *) type->tp_alloc(type, 0);
  if (!self) return NULL;

  self->state = AquaHash(salt_val);
  self->lock = NULL;
  return (PyObject*)self;
}


static PyObject *Aquahash_update(Aquahash *self, PyObject *args) {
  Py_buffer data = {.buf=NULL, .obj=NULL, .len=0};
  if (!PyArg_ParseTuple(args, "s*:update", &data)) return NULL;

  // Release the GIL for large inputs.
  bool should_allow_threads = (data.len >= GIL_MIN_SIZE);
  if (should_allow_threads && !self->lock) {
    self->lock = PyThread_allocate_lock(); // Can fail, resulting in NULL.
  }
  if (should_allow_threads && self->lock) {
    Py_BEGIN_ALLOW_THREADS
    PyThread_acquire_lock(self->lock, 1); // Protect this hasher from concurrent mutation.
    self->state.Update((uint8_t*)data.buf, data.len);
    PyThread_release_lock(self->lock);
    Py_END_ALLOW_THREADS
  } else { // Either too small to be worthwhile, or else could not acquire lock.
    self->state.Update((uint8_t*)data.buf, data.len);
  }
  if (data.obj) PyBuffer_Release(&data);
  Py_RETURN_NONE;
}


static PyObject *Aquahash_digest(Aquahash *self, PyObject *noargs) {
  AquaHash copied_state = self->state;
  __m128i digest = copied_state.Finalize();
  return Py_BuildValue("y#", &digest, sizeof(digest));
}


static PyObject *Aquahash_digest_size(Aquahash *self, PyObject *noargs) {
  return Py_BuildValue("i", 16);
}


static PyObject *Aquahash_block_size(Aquahash *self, PyObject *noargs) {
  return Py_BuildValue("i", 64);
}


static void hashing_dealloc(Aquahash *self) {
  if (self->lock) {
    PyThread_free_lock(self->lock);
    self->lock = NULL;
  }
  PyObject_Del(self);
}


static struct PyMethodDef Aquahash_methods[] = {
  {"update", (PyCFunction)Aquahash_update, METH_VARARGS},
  {"digest", (PyCFunction)Aquahash_digest, METH_NOARGS},
  {"digest_size", (PyCFunction)Aquahash_digest_size, METH_NOARGS},
  {"block_size", (PyCFunction)Aquahash_block_size, METH_NOARGS},
  {NULL, NULL}
};

static PyTypeObject Aquahash_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "Aquahash",
    .tp_basicsize = sizeof(Aquahash),
    .tp_doc = "Various hash functions.",
    .tp_dealloc = (destructor)hashing_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_methods = Aquahash_methods,
    .tp_new = Aquahash_new
};


PyDoc_STRVAR(aquahash_doc, "Hash a `str` or bytes-like value using the AquaHash function.");

static PyObject *hashing_aquahash(PyObject *module, PyObject *args, PyObject *kwargs) {
  Py_buffer data = {.buf=NULL, .obj=NULL, .len=0};
  Py_buffer salt = {.buf=NULL, .obj=NULL, .len=0};

  static const char * const _keywords[] = {"data", "salt", NULL};
  static _PyArg_Parser _parser = {"s*|$s*:aquahash", _keywords, 0};
  if (!_PyArg_ParseTupleAndKeywordsFast(args, kwargs, &_parser, &data, &salt)) return NULL;

  __m128i salt_val = {0, 0};
  if (salt.len) memcpy(&salt_val, salt.buf, min(salt.len, (long)sizeof(salt_val)));
  if (salt.obj) PyBuffer_Release(&salt);

  __m128i digest;
  if (data.len >= GIL_MIN_SIZE) { // Unlike update(), we do not need a lock here because all state is private.
    Py_BEGIN_ALLOW_THREADS
    digest = AquaHash::Hash((uint8_t*)data.buf, data.len, salt_val);
    Py_END_ALLOW_THREADS
  } else {
    digest = AquaHash::Hash((uint8_t*)data.buf, data.len, salt_val);
  }
  if (data.obj) PyBuffer_Release(&data);

  return Py_BuildValue("y#", &digest, sizeof(digest));
}


static struct PyMethodDef module_functions[] = {
  {"aquahash", (PyCFunction)hashing_aquahash, METH_VARARGS|METH_KEYWORDS, aquahash_doc },
  {NULL, NULL}
};


static struct PyModuleDef module_def = {
  PyModuleDef_HEAD_INIT,
  .m_name = "cpython",
  .m_doc = hashing_doc,
  .m_size = 0,
  .m_methods = module_functions,
  .m_slots = NULL, // Single-phase initialization.
};


PyMODINIT_FUNC
PyInit_cpython(void) {

  PyObject *module = PyModule_Create(&module_def);
  if (!module) return NULL;

  if (PyType_Ready(&Aquahash_type) < 0) return NULL;
  Py_INCREF(&Aquahash_type);
  PyModule_AddObject(module, Aquahash_type.tp_name, (PyObject *)&Aquahash_type);

  return module;
}
