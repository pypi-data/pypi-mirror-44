/* memoryslots type *********************************************************/

#include "pyconfig.h"
#include "Python.h"
#include <string.h>

#ifndef Py_RETURN_NOTIMPLEMENTED
/* Macro for returning Py_NotImplemented from a function */
#define Py_RETURN_NOTIMPLEMENTED \
    return Py_INCREF(Py_NotImplemented), Py_NotImplemented
#endif

#define PyMemorySlots_GET_ITEM(op, i) (((PyMemorySlotsObject *)(op))->ob_item[i])
#define PyMemorySlots_SET_ITEM(op, i, v) (((PyMemorySlotsObject *)(op))->ob_item[i] = v)

#define PyMemorySlots_Check(op) (Py_TYPE(op) == &PyMemorySlots_Type)

#define IGS_GET_INDEX(op) ((struct itemgetset_object*)op)->i

#if PY_MAJOR_VERSION == 2
static PyObject *
_PyObject_GetBuiltin(const char *name)
{
    PyObject *mod_name, *mod, *attr;

    mod_name = PyUnicode_FromString("__builtin__");   /* borrowed */
    if (mod_name == NULL)
        return NULL;
    mod = PyImport_Import(mod_name);
    if (mod == NULL)
        return NULL;
    attr = PyObject_GetAttrString(mod, name);
    Py_DECREF(mod);
    return attr;
}
#endif

#define DEFERRED_ADDRESS(addr) 0

static PyTypeObject PyMemorySlots_Type;
typedef PyTupleObject PyMemorySlotsObject;
typedef PyTupleObject PyMemorySlotsReadonlyObject;

static PyObject *
PyMemorySlots_New(PyTypeObject *tp, Py_ssize_t size)
{
    PyMemorySlotsObject *op;
    int is_gc;
    
    if (size < 0) {
        PyErr_BadInternalCall();
        return NULL;
    }
    
    is_gc = PyType_IS_GC(tp);
    if (is_gc)
        op = (PyMemorySlotsObject*)_PyObject_GC_NewVar(tp, size);
    else
        op = (PyMemorySlotsObject*)_PyObject_NewVar(tp, size);
    if (op == NULL)
        return NULL;

    memset(op->ob_item, 0, Py_SIZE(op)*sizeof(void*));

    if (is_gc)
        PyObject_GC_Track(op);
    
    return (PyObject*)op;
}

static PyObject *
memoryslots_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyTupleObject *tmp; 
    PyMemorySlotsObject *newobj;
    Py_ssize_t i, n;
    PyObject *item;

    if (args == NULL)
        return PyMemorySlots_New(type, 0);
    
    if (PyTuple_CheckExact(args)) {
        tmp = (PyTupleObject*)args;
        Py_INCREF(args);
    } else {
        tmp = (PyTupleObject*)PySequence_Tuple(args);
        if (tmp == NULL)
            return NULL;        
    }

    n = PyTuple_GET_SIZE(tmp);

    if (type == &PyMemorySlots_Type) {
        newobj = (PyMemorySlotsObject*)PyMemorySlots_New(type, n);
    } else {
        //assert(PyType_IsSubtype(type, &PyMemorySlots_Type));
        newobj = (PyMemorySlotsObject*)(type->tp_alloc(type, n));
    }

    if (newobj == NULL) {
        Py_DECREF(tmp);
        return NULL;
    }

    for (i = n; --i >= 0; ) {
        item = PyTuple_GET_ITEM(tmp, i);
        newobj->ob_item[i] = item;
        Py_INCREF(item);
    }

    Py_DECREF(tmp);
    return (PyObject*)newobj;
}

static PyObject *
memoryslots_getnewargs(PyMemorySlotsObject *ob)
{
    PyObject *v;
    PyTupleObject *res;
    Py_ssize_t i, n = Py_SIZE(ob);

    res = (PyTupleObject*)PyTuple_New(n);

    if (res == NULL)
        return NULL;

    for (i = n; --i >= 0; ) {
        v = PyTuple_GET_ITEM(ob, i);
        PyTuple_SET_ITEM(res, i, v);
        Py_INCREF(v);
    }

    return (PyObject*)res;
}

static int
memoryslots_clear(PyMemorySlotsObject *op)
{
    Py_ssize_t i;

    for (i = Py_SIZE(op); --i >= 0; ) {
        Py_CLEAR(op->ob_item[i]);
    }
    return 0;
}

static void
memoryslots_dealloc(PyMemorySlotsObject *op)
{
    Py_ssize_t i;

    if PyType_IS_GC(Py_TYPE(op)) 
        PyObject_GC_UnTrack(op);

    /*Py_TRASHCAN_SAFE_BEGIN(op)*/
    for (i = Py_SIZE(op); --i >= 0; ) {
        Py_CLEAR(op->ob_item[i]);
    }
    Py_TYPE(op)->tp_free((PyObject *)op);
    /*Py_TRASHCAN_SAFE_END(op)*/
}

static void memoryslots_free(void *o) {
    if PyType_IS_GC(Py_TYPE((PyObject*)o))
        PyObject_GC_Del((PyObject*)o);
    else
        PyObject_Del((PyObject*)o);
}

static int
memoryslots_traverse(PyMemorySlotsObject *o, visitproc visit, void *arg)
{
    Py_ssize_t i;

    for (i = Py_SIZE(o); --i >= 0; ) {
        Py_VISIT(o->ob_item[i]);
    }
    return 0;
}

static PyObject *
memoryslots_repr(PyObject *dd)
{
    PyObject *baserepr;
    PyObject *v, *result;
    Py_ssize_t n;
        
    n = PyTuple_GET_SIZE(dd);

    if (n == 0) {
#if PY_MAJOR_VERSION >= 3
        result = PyUnicode_FromString("memoryslots()\0");
#else
        result = PyString_FromString("memoryslots()\0");
#endif
        return result;
    }

    if (n == 1) {
        v = PyTuple_GET_ITEM(dd, 0);
        baserepr = PyObject_Repr(v);
#if PY_MAJOR_VERSION >= 3
        result = PyUnicode_FromFormat("memoryslots(%U)", baserepr);
#else
        result = PyString_FromFormat("memoryslots(%s)", PyString_AS_STRING(baserepr));
#endif
        return result;
    }    
    
    baserepr = PyTuple_Type.tp_repr(dd);
    if (baserepr == NULL)
        return NULL;

#if PY_MAJOR_VERSION >= 3
    result = PyUnicode_FromFormat("memoryslots%U", baserepr);
#else
    result = PyString_FromFormat("memoryslots%s", PyString_AS_STRING(baserepr));
#endif
    Py_DECREF(baserepr);
    return result;
}

PyDoc_STRVAR(memoryslots_doc,
"memoryslots([...]) --> memoryslots\n\n\
");

static PyObject *
memoryslots_concat(PyMemorySlotsObject *a, PyObject *bb)
{
    Py_ssize_t size;
    Py_ssize_t i, n;
    PyObject **src, **dest;
    PyMemorySlotsObject *np;
    
    if (!PyTuple_Check(bb)) {
        PyErr_Format(PyExc_TypeError,
             "can only concatenate tuple (not \"%.200s\") to tuple",
                 Py_TYPE(bb)->tp_name);
        return NULL;
    }
#define b ((PyMemorySlotsObject *)bb)
    size = Py_SIZE(a) + Py_SIZE(b);
    if (size < 0)
        return PyErr_NoMemory();

    np = (PyMemorySlotsObject *) PyMemorySlots_New(Py_TYPE(a), size);
    if (np == NULL) {
        return NULL;
    }
    
    src = a->ob_item;
    dest = np->ob_item;

    n = Py_SIZE(a);
    if (n > 0) {
        for (i = 0; i < n; i++) {
            PyObject *v = src[i];
            Py_INCREF(v);
            dest[i] = v;
        }
    }
    
    src = b->ob_item;
    dest = np->ob_item + Py_SIZE(a);
    n = Py_SIZE(b);
    for (i = 0; i < n; i++) {
        PyObject *v = src[i];
        Py_INCREF(v);
        dest[i] = v;
    }
#undef b

    return (PyObject *)np;
}

static PyObject *
memoryslots_slice(PyMemorySlotsObject *a, Py_ssize_t ilow, Py_ssize_t ihigh)
{
#define aa ((PyMemorySlotsObject*)a)
    PyMemorySlotsObject *np;
    PyObject **src, **dest;
    Py_ssize_t i;
    Py_ssize_t len;
    
    if (ilow < 0)
        ilow = 0;
    if (ihigh > Py_SIZE(a))
        ihigh = Py_SIZE(a);
    if (ihigh < ilow)
        ihigh = ilow;
    if (ilow == 0 && ihigh == Py_SIZE(a) && Py_TYPE(a) == &PyMemorySlots_Type) {
        Py_INCREF(a);
        return (PyObject*)a;
    }

    len = ihigh - ilow;

    if (Py_TYPE(a) == &PyMemorySlots_Type)
        np = (PyMemorySlotsObject*)PyMemorySlots_New(&PyMemorySlots_Type, len);
    else    
        np = (PyMemorySlotsObject*)(Py_TYPE(a)->tp_alloc(Py_TYPE(a), len));    
    if (np == NULL)
        return NULL;
        
    src = aa->ob_item + ilow;
    dest = np->ob_item;
    if (len > 0) {
        for (i = 0; i < len; i++) {
            PyObject *v = src[i];
            Py_INCREF(v);
            dest[i] = v;
        }
    }
    return (PyObject *)np;
#undef aa
}

static int
memoryslots_ass_slice(PyMemorySlotsObject *a, Py_ssize_t ilow, Py_ssize_t ihigh, PyObject *v)
{
    PyObject **item;
    PyObject **vitem = NULL;
    PyObject *v_as_SF = NULL; /* PySequence_Fast(v) */
    Py_ssize_t n;
    Py_ssize_t k;
    int result = -1;
    
    if (v == NULL)
        return result;
    else {
        if ((PyObject*)a == v) {
            v = memoryslots_slice((PyMemorySlotsObject*)v, 0, Py_SIZE(v));
            if (v == NULL)
                return result;
                
            result = memoryslots_ass_slice(a, ilow, ihigh, v);
            Py_DECREF(v);
            return result;
        }
        v_as_SF = PySequence_Fast(v, "can only assign an iterable");
        if(v_as_SF == NULL) {
            return result;
        }
        n = PySequence_Fast_GET_SIZE(v_as_SF);
        vitem = PySequence_Fast_ITEMS(v_as_SF);
    }
    
    if (ilow < 0)
        ilow = 0;
    else if (ilow > Py_SIZE(a))
        ilow = Py_SIZE(a);

    if (ihigh < ilow)
        ihigh = ilow;
    else if (ihigh > Py_SIZE(a))
        ihigh = Py_SIZE(a);

    if (n != ihigh - ilow) {
        Py_XDECREF(v_as_SF);    
        return -1;
    }
    
    item = ((PyMemorySlotsObject*)a)->ob_item;
    if (n > 0) {
        for (k = 0; k < n; k++, ilow++) {
            PyObject *w = vitem[k];
            PyObject *u = item[ilow];
            Py_XDECREF(u);
            item[ilow] = w;
            Py_XINCREF(w);
        }
    }
    Py_XDECREF(v_as_SF);    
    return 0;
}


static int
memoryslots_ass_item(PyMemorySlotsObject *a, Py_ssize_t i, PyObject *v)
{
    PyObject *old_value;
    
    if (i < 0 || i >= Py_SIZE(a)) {
        PyErr_SetString(PyExc_IndexError,
                        "assignment index out of range");
        return -1;
    }
    
    if (v == NULL)
        return -1;
        
    old_value = PyMemorySlots_GET_ITEM(a, i);
    Py_XDECREF(old_value);
    PyMemorySlots_SET_ITEM(a, i, v);
    Py_INCREF(v);
    return 0;
}

static PyObject *
memoryslots_item(PyMemorySlotsObject *a, Py_ssize_t i)
{
    PyObject* v;
    
    if (i < 0 || i >= Py_SIZE(a)) {
        PyErr_SetString(PyExc_IndexError, "index out of range");
        return NULL;
    }
    v = a->ob_item[i];
    Py_INCREF(v);
    return (PyObject*)v;
}

static PyObject*
memoryslots_subscript(PyMemorySlotsObject* self, PyObject* item)
{
    if (PyIndex_Check(item)) {
        PyObject *v;
        Py_ssize_t i;
        
        i = PyNumber_AsSsize_t(item, PyExc_IndexError);
        if (i < 0) {
            if (i == -1 && PyErr_Occurred())
                return NULL;            
            i += Py_SIZE(self);
        }
        if (i < 0 || i >= Py_SIZE(self)) {
            PyErr_SetString(PyExc_IndexError, "index out of range");
            return NULL;
        }
        v = self->ob_item[i];
        Py_INCREF(v);
        return (PyObject*)v;
    }
    else if (PySlice_Check(item)) {
        Py_ssize_t start, stop, step, slicelength;

#if PY_MAJOR_VERSION >= 3
        if (PySlice_GetIndicesEx(item, (PyTuple_GET_SIZE(self)), &start, &stop, &step, &slicelength) < 0) {
            return NULL;
        }
#else
        if (PySlice_GetIndicesEx(((PySliceObject*)item), (PyTuple_GET_SIZE(self)), &start, &stop, &step, &slicelength) < 0)  {
            return NULL;
        }
#endif
                
        return memoryslots_slice(self, start, stop);
    }
    else {

#if PY_MAJOR_VERSION >= 3
        if (PyUnicode_Check(item))
#else
        if (PyString_Check(item))
#endif
      {
            PyObject *ob = PyObject_GetAttr((PyObject*)self, item);
            
            if (ob == NULL) {
                PyErr_Format(PyExc_KeyError, "Invalid key");
                return NULL;
            }
            //Py_INCREF(ob);
            return ob;
        }
        else {
            PyErr_Format(PyExc_TypeError,
                         "subscript must be integer, slice or string, but not %.200s",
                         Py_TYPE(item)->tp_name);
            return NULL;
        }
    }
}

static int
memoryslots_ass_subscript(PyMemorySlotsObject* self, PyObject* item, PyObject* value)
{
    if (PyIndex_Check(item)) {
        Py_ssize_t i = PyNumber_AsSsize_t(item, PyExc_IndexError);
        if (i == -1 && PyErr_Occurred())
            return -1;
        if (i < 0)
            i += PyList_GET_SIZE(self);
        return memoryslots_ass_item(self, i, value);
    }
    else if (PySlice_Check(item)) {
        Py_ssize_t start, stop, step, slicelength;

#if PY_MAJOR_VERSION >= 3
        if (PySlice_GetIndicesEx(item, (Py_SIZE(self)), &start, &stop, &step, &slicelength) < 0) {
            return -1; 
        }
#else
        if (PySlice_GetIndicesEx(((PySliceObject*)item), (Py_SIZE(self)), &start, &stop, &step, &slicelength) < 0) {
            return -1;
        }
#endif
        return memoryslots_ass_slice(self, start, stop, value);
    }
    else {

#if PY_MAJOR_VERSION >= 3
        if (PyUnicode_Check(item)) 
#else
        if (PyString_Check(item)) 
#endif
       {
            int res = PyObject_SetAttr((PyObject*)self, item, value);
            
            if (res < 1) {
                PyErr_Format(PyExc_KeyError, "Invalid key");
                return res;
            }
            return 0;
        }
        else {
            PyErr_Format(PyExc_TypeError,
                         "indices must be integers, not %.200s",
                         Py_TYPE(item)->tp_name);
            return -1;
        }
    }    
}

static PyObject *
memoryslots_repeat(PyMemorySlotsObject *a, Py_ssize_t n)
{
    Py_ssize_t i, j;
    Py_ssize_t size;
    PyTupleObject *np;
    PyObject **p, **items;
    if (n < 0)
        n = 0;
    if (Py_SIZE(a) == 0) {
        return PyMemorySlots_New(Py_TYPE(a), 0);
    }
    if (n > PY_SSIZE_T_MAX / Py_SIZE(a))
        return PyErr_NoMemory();
    size = Py_SIZE(a);
    np = (PyMemorySlotsObject *) PyMemorySlots_New(Py_TYPE(a), Py_SIZE(a) * n);
    if (np == NULL)
        return NULL;
    
    if (size == 0)
        return (PyObject *)np;
        
    p = np->ob_item;
    items = a->ob_item;
    for (i = 0; i < n; i++) {
        for (j = 0; j < size; j++) {
            *p = items[j];
            Py_INCREF(*p);
            p++;
        }
    }
    return (PyObject *) np;
}

PyDoc_STRVAR(memoryslots_len_doc,
"T.__len__() -- len of T");

static Py_ssize_t
memoryslots_len(PyMemorySlotsObject *op)
{
    return Py_SIZE(op);
}

PyDoc_STRVAR(memoryslots_sizeof_doc,
"T.__sizeof__() -- size of T in memory, in bytes");

static PyObject *
memoryslots_sizeof(PyMemorySlotsObject *self)
{
    Py_ssize_t res;

    res = PyMemorySlots_Type.tp_basicsize + Py_SIZE(self) * sizeof(PyObject*);
    return PyLong_FromSsize_t(res);
}

static PyObject *
memoryslots_richcompare(PyObject *v, PyObject *w, int op)
{
    PyMemorySlotsObject *vt, *wt;
    Py_ssize_t i;
    Py_ssize_t vlen, wlen;

    if (!PyType_IsSubtype(Py_TYPE(v), &PyMemorySlots_Type) || 
       (!PyType_IsSubtype(Py_TYPE(w), &PyMemorySlots_Type) && !PyTuple_Check(w)))
        Py_RETURN_NOTIMPLEMENTED;

    vt = (PyMemorySlotsObject *)v;
    wt = (PyMemorySlotsObject *)w;

    vlen = Py_SIZE(vt);
    wlen = Py_SIZE(wt);
    
    if ((vlen != wlen) && (op == Py_EQ || op == Py_NE)) {
        PyObject *res;
        if (op == Py_EQ)
            res = Py_False;
        else
            res = Py_True;
        Py_INCREF(res);
        return res;
    }    
    
    for (i = 0; i < vlen && i < wlen; i++) {
        int k = PyObject_RichCompareBool(vt->ob_item[i],
                                         wt->ob_item[i], Py_EQ);
        if (k < 0)
            return NULL;
        if (!k)
            break;
    }

    if (i >= vlen || i >= wlen) {
        /* No more items to compare -- compare sizes */
        int cmp;
        PyObject *res;
        switch (op) {
        case Py_LT: cmp = vlen <  wlen; break;
        case Py_LE: cmp = vlen <= wlen; break;
        case Py_EQ: cmp = vlen == wlen; break;
        case Py_NE: cmp = vlen != wlen; break;
        case Py_GT: cmp = vlen >  wlen; break;
        case Py_GE: cmp = vlen >= wlen; break;
        default: return NULL; /* cannot happen */
        }
        if (cmp)
            res = Py_True;
        else
            res = Py_False;
        Py_INCREF(res);
        return res;
    }

    /* We have an item that differs -- shortcuts for EQ/NE */
    if (op == Py_EQ) {
        Py_INCREF(Py_False);
        return Py_False;
    }
    if (op == Py_NE) {
        Py_INCREF(Py_True);
        return Py_True;
    }

    /* Compare the final item again using the proper operator */
    return PyObject_RichCompare(vt->ob_item[i], wt->ob_item[i], op);
}

static PySequenceMethods memoryslots_as_sequence = {
    (lenfunc)memoryslots_len,                          /* sq_length */
    (binaryfunc)memoryslots_concat,                    /* sq_concat */
    (ssizeargfunc)memoryslots_repeat,                  /* sq_repeat */
    (ssizeargfunc)memoryslots_item,                    /* sq_item */
    0,                                                 /* sq_slice */
    (ssizeobjargproc)memoryslots_ass_item,             /* sq_ass_item */
    0,                                                 /* sq_ass_item */
    0,                                                 /* sq_ass_slice */
    0,                                                 /* sq_contains */
};

static PyMappingMethods memoryslots_as_mapping = {
    (lenfunc)memoryslots_len,
    (binaryfunc)memoryslots_subscript,
    (objobjargproc)memoryslots_ass_subscript
};

static PySequenceMethods memoryslotsreadonly_as_sequence = {
    (lenfunc)memoryslots_len,                          /* sq_length */
    (binaryfunc)memoryslots_concat,                    /* sq_concat */
    (ssizeargfunc)memoryslots_repeat,                  /* sq_repeat */
    (ssizeargfunc)memoryslots_item,                    /* sq_item */
    0,                                                 /* sq_slice */
    0,                                                 /* sq_ass_item */
    0,                                                 /* sq_ass_item */
    0,                                                 /* sq_ass_slice */
    0,                                                 /* sq_contains */
};

static PyMappingMethods memoryslotsreadonly_as_mapping = {
    (lenfunc)memoryslots_len,
    (binaryfunc)memoryslots_subscript,
    0
};

PyDoc_STRVAR(memoryslots_copy_doc, "D.copy() -> a shallow copy of D.");

static PyObject *
memoryslots_copy(PyMemorySlotsObject *ob)
{
    return memoryslots_slice(ob, 0, PyTuple_GET_SIZE(ob));
}


PyDoc_STRVAR(memoryslots_reduce_doc, "D.__reduce__()");

static PyObject *
memoryslots_reduce(PyObject *ob)
{
    PyObject *args;
    PyObject *result;
    PyObject *tmp;

    tmp = PySequence_Tuple(ob);
    args = PyTuple_Pack(1, tmp);
    Py_DECREF(tmp);
    if (args == NULL)
        return NULL;
    
    result = PyTuple_Pack(2, &PyMemorySlots_Type, args);
    Py_DECREF(args);
    return result;
}

static long
memoryslots_hash(PyObject *v)
{
    register long x, y;
    register Py_ssize_t len = Py_SIZE(v);
    register PyObject **p;
    long mult = 1000003L;
    x = 0x345678L;
    p = ((PyTupleObject*)v)->ob_item;
    while (--len >= 0) {
        y = PyObject_Hash(*p++);
        if (y == -1)
            return -1;
        x = (x ^ y) * mult;
        /* the cast might truncate len; that doesn't change hash stability */
        mult += (long)(82520L + len + len);
    }
    x += 97531L;
    if (x == -1)
        x = -2;
    return x;
}

static PyMethodDef memoryslots_methods[] = {
    {"__getnewargs__",          (PyCFunction)memoryslots_getnewargs,  METH_NOARGS},
        /*{"copy", (PyCFunction)memoryslots_copy, METH_NOARGS, memoryslots_copy_doc},*/
    {"__copy__", (PyCFunction)memoryslots_copy, METH_NOARGS, memoryslots_copy_doc},
    {"__len__", (PyCFunction)memoryslots_len, METH_NOARGS, memoryslots_len_doc},
    {"__sizeof__",      (PyCFunction)memoryslots_sizeof, METH_NOARGS, memoryslots_sizeof_doc},     
    {"__reduce__", (PyCFunction)memoryslots_reduce, METH_NOARGS, memoryslots_reduce_doc},
    {NULL}
};

static PyObject* 
memoryslots_iter(PyObject *seq);

static PyTypeObject PyMemorySlots_Type = {
    PyVarObject_HEAD_INIT(DEFERRED_ADDRESS(&PyType_Type), 0)
    "recordclass.memoryslots.memoryslots",          /* tp_name */
    sizeof(PyMemorySlotsObject) - sizeof(PyObject*),      /* tp_basicsize */
    sizeof(PyObject*),                              /* tp_itemsize */
    /* methods */
    (destructor)memoryslots_dealloc,        /* tp_dealloc */
    0,                                      /* tp_print */
    0,                                      /* tp_getattr */
    0,                                      /* tp_setattr */
    0,                                      /* tp_reserved */
    (reprfunc)memoryslots_repr,             /* tp_repr */
    0,                                      /* tp_as_number */
    &memoryslots_as_sequence,               /* tp_as_sequence */
    &memoryslots_as_mapping,                /* tp_as_mapping */
    PyObject_HashNotImplemented,            /* tp_hash */
    0,                                      /* tp_call */
    0,                                      /* tp_str */
    PyObject_GenericGetAttr,                /* tp_getattro */
    PyObject_GenericSetAttr,                /* tp_setattro */
    0,                                      /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_BASETYPE,
                                            /* tp_flags */
    memoryslots_doc,                        /* tp_doc */
    (traverseproc)memoryslots_traverse,     /* tp_traverse */
    (inquiry)memoryslots_clear,             /* tp_clear */
    memoryslots_richcompare,                /* tp_richcompare */
    0,                                      /* tp_weaklistoffset*/
    memoryslots_iter,                       /* tp_iter */
    0,                                      /* tp_iternext */
    memoryslots_methods,                    /* tp_methods */
    0,                                      /* tp_members */
    0,                                      /* tp_getset */
    0,                                      /* tp_base */
    0,                                      /* tp_memoryslots */
    0,                                      /* tp_descr_get */
    0,                                      /* tp_descr_set */
    0,                                      /* tp_memoryslotsoffset */
    0,                                      /* tp_init */
    0,                                      /* tp_alloc */
    memoryslots_new,                        /* tp_new */
    memoryslots_free,                        /* tp_free */
    0                                       /* tp_is_gc */
};

static PyTypeObject PyMemorySlotsReadonly_Type = {
    PyVarObject_HEAD_INIT(DEFERRED_ADDRESS(&PyType_Type), 0)
    "recordclass.memoryslots.memoryslotsreadonly",          /* tp_name */
    sizeof(PyMemorySlotsObject) - sizeof(PyObject*),      /* tp_basicsize */
    sizeof(PyObject*),                              /* tp_itemsize */
    /* methods */
    (destructor)memoryslots_dealloc,        /* tp_dealloc */
    0,                                      /* tp_print */
    0,                                      /* tp_getattr */
    0,                                      /* tp_setattr */
    0,                                      /* tp_reserved */
    (reprfunc)memoryslots_repr,             /* tp_repr */
    0,                                      /* tp_as_number */
    &memoryslotsreadonly_as_sequence,               /* tp_as_sequence */
    &memoryslotsreadonly_as_mapping,                /* tp_as_mapping */
    memoryslots_hash,                       /* tp_hash */
    0,                                      /* tp_call */
    0,                                      /* tp_str */
    PyObject_GenericGetAttr,                /* tp_getattro */
    PyObject_GenericSetAttr,                /* tp_setattro */
    0,                                      /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_BASETYPE,
                                            /* tp_flags */
    memoryslots_doc,                        /* tp_doc */
    (traverseproc)memoryslots_traverse,     /* tp_traverse */
    (inquiry)memoryslots_clear,             /* tp_clear */
    memoryslots_richcompare,                /* tp_richcompare */
    0,                                      /* tp_weaklistoffset*/
    memoryslots_iter,                       /* tp_iter */
    0,                                      /* tp_iternext */
    memoryslots_methods,                    /* tp_methods */
    0,                                      /* tp_members */
    0,                                      /* tp_getset */
    0,                                      /* tp_base */
    0,                                      /* tp_memoryslots */
    0,                                      /* tp_descr_get */
    0,                                      /* tp_descr_set */
    0,                                      /* tp_memoryslotsoffset */
    0,                                      /* tp_init */
    0,                                      /* tp_alloc */
    memoryslots_new,                        /* tp_new */
    memoryslots_free,                        /* tp_free */
    0                                       /* tp_is_gc */
};

/*********************** MemorySlots Iterator **************************/

typedef struct {
    PyObject_HEAD
    Py_ssize_t it_index;
    PyTupleObject *it_seq; /* Set to NULL when iterator is exhausted */
} memoryslotsiterobject;

static void
memoryslotsiter_dealloc(memoryslotsiterobject *it)
{
    PyObject_GC_UnTrack(it);
    Py_CLEAR(it->it_seq);
    PyObject_GC_Del(it);
}

static int
memoryslotsiter_traverse(memoryslotsiterobject *it, visitproc visit, void *arg)
{
    Py_VISIT(it->it_seq);
    return 0;
}

static int
memoryslotsiter_clear(memoryslotsiterobject *it)
{
    Py_CLEAR(it->it_seq);
    return 0;
}

static PyObject *
memoryslotsiter_next(memoryslotsiterobject *it)
{
    PyTupleObject *seq;
    PyObject *item;

    assert(it != NULL);
    seq = it->it_seq;
    if (seq == NULL)
        return NULL;
    assert(PyTuple_Check(seq));

    if (it->it_index < PyTuple_GET_SIZE(seq)) {
        item = PyTuple_GET_ITEM(seq, it->it_index);
        Py_INCREF(item);
        ++it->it_index;
        return item;
    }

    Py_DECREF(seq);
    it->it_seq = NULL;
    return NULL;
}

static PyObject *
memoryslotsiter_len(memoryslotsiterobject *it)
{
    Py_ssize_t len = 0;
    if (it->it_seq)
        len = PyTuple_GET_SIZE(it->it_seq) - it->it_index;
    return PyLong_FromSsize_t(len);
}

PyDoc_STRVAR(length_hint_doc, "Private method returning an estimate of len(list(it)).");

static PyObject *
memoryslotsiter_reduce(memoryslotsiterobject *it)
{
    if (it->it_seq)
        return Py_BuildValue("N(O)n", _PyObject_GetBuiltin("iter"),
                             it->it_seq, it->it_index);
    else
        return Py_BuildValue("N(())", _PyObject_GetBuiltin("iter"));
}

PyDoc_STRVAR(memoryslotsiter_reduce_doc, "D.__reduce__()");


static PyObject *
memoryslotsiter_setstate(memoryslotsiterobject *it, PyObject *state)
{
    Py_ssize_t index;

#if PY_MAJOR_VERSION >= 3    
    index = PyLong_AsSsize_t(state);
#else
    index = PyNumber_AsSsize_t(state, NULL);
#endif
    if (index == -1 && PyErr_Occurred())
        return NULL;
    if (it->it_seq != NULL) {
        if (index < 0)
            index = 0;
        else if (index > PyTuple_GET_SIZE(it->it_seq))
            index = PyTuple_GET_SIZE(it->it_seq); /* exhausted iterator */
        it->it_index = index;
    }
    Py_RETURN_NONE;
}

PyDoc_STRVAR(setstate_doc, "Set state information for unpickling.");


static PyMethodDef memoryslotsiter_methods[] = {
    {"__length_hint__", (PyCFunction)memoryslotsiter_len, METH_NOARGS, length_hint_doc},
    {"__reduce__",      (PyCFunction)memoryslotsiter_reduce, METH_NOARGS, memoryslotsiter_reduce_doc},
    {"__setstate__",    (PyCFunction)memoryslotsiter_setstate, METH_O, setstate_doc},
    {NULL,              NULL}           /* sentinel */
};

PyTypeObject PyMemorySlotsIter_Type = {
    PyVarObject_HEAD_INIT(DEFERRED_ADDRESS(&PyType_Type), 0)
    "recordclass.memoryslots.memoryslots_iterator",                           /* tp_name */
    sizeof(memoryslotsiterobject),                    /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)memoryslotsiter_dealloc,              /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,    /* tp_flags */
    0,                                          /* tp_doc */
    (traverseproc)memoryslotsiter_traverse,     /* tp_traverse */
    (inquiry)memoryslotsiter_clear,             /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    PyObject_SelfIter,                          /* tp_iter */
    (iternextfunc)memoryslotsiter_next,         /* tp_iternext */
    memoryslotsiter_methods,                    /* tp_methods */
    0,
};

static PyObject *
memoryslots_iter(PyObject *seq)
{
    memoryslotsiterobject *it;

    it = PyObject_GC_New(memoryslotsiterobject, &PyMemorySlotsIter_Type);
    if (it == NULL)
        return NULL;
    it->it_index = 0;
    it->it_seq = (PyTupleObject *)seq;
    Py_INCREF(seq);
    PyObject_GC_Track(it);
    return (PyObject *)it;
}

struct itemgetset_object {
  PyObject_HEAD
  Py_ssize_t i;
};

/*static PyTypeObject ItemGetSet_Type;*/

static PyMethodDef itemgetset_methods[] = {
  {0, 0, 0, 0}
};

static PyObject* itemgetset_new(PyTypeObject *t, PyObject *args, PyObject *k) {    
    PyObject *ob;
    PyObject *item;
    Py_ssize_t i;

    ob = (PyObject*) PyBaseObject_Type.tp_new(t, PyTuple_New(0), 0);    
    if (ob == NULL)
        return NULL;
        
    item = PyTuple_GET_ITEM(args, 0);

    i = PyNumber_AsSsize_t(item, PyExc_IndexError);
    if (i == -1 && PyErr_Occurred()) {
        Py_DECREF(ob);
        return NULL;
    }

    ((struct itemgetset_object*)ob)->i = i;
    return ob;
}

static void itemgetset_dealloc(PyObject *o) {
    PyObject_Del(o);
}

static PyObject* itemgetset_get(PyObject *self, PyObject *obj, PyObject *type) {
    //Py_ssize_t i;
    PyObject *v;
    
    if (obj == NULL || obj == Py_None) {
        Py_INCREF(self);
        return self;
    }
    v = PyTuple_GET_ITEM(obj, IGS_GET_INDEX(self));
    Py_INCREF(v);
    return v;
}

static int itemgetset_set(PyObject *self, PyObject *obj, PyObject *value) {
    Py_ssize_t i;
    PyObject *v;

    if (value == NULL) {
        PyErr_SetString(PyExc_NotImplementedError, "__delete__");
        return -1;
    }
    if (obj == NULL || obj == Py_None)
        return 0;
        
    i = IGS_GET_INDEX(self);
    v = PyTuple_GET_ITEM(obj, i);
    Py_XDECREF(v);
    PyTuple_SET_ITEM(obj, i, value);
    Py_INCREF(value);
    return 0;
}

static PyTypeObject ItemGetSet_Type = {
    PyVarObject_HEAD_INIT(DEFERRED_ADDRESS(&PyType_Type), 0)
    "recordclass.memoryslots.itemgetset", /*tp_name*/
    sizeof(struct itemgetset_object), /*tp_basicsize*/
    0, /*tp_itemsize*/
    itemgetset_dealloc, /*tp_dealloc*/
    0, /*tp_print*/
    0, /*tp_getattr*/
    0, /*tp_setattr*/
    0, /*reserved*/
    0, /*tp_repr*/
    0, /*tp_as_number*/
    0, /*tp_as_sequence*/
    0, /*tp_as_mapping*/
    0, /*tp_hash*/
    0, /*tp_call*/
    0, /*tp_str*/
    0, /*tp_getattro*/
    0, /*tp_setattro*/
    0, /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE, /*tp_flags*/
    0, /*tp_doc*/
    0, /*tp_traverse*/
    0, /*tp_clear*/
    0, /*tp_richcompare*/
    0, /*tp_weaklistoffset*/
    0, /*tp_iter*/
    0, /*tp_iternext*/
    itemgetset_methods, /*tp_methods*/
    0, /*tp_members*/
    0, /*tp_getset*/
    0, /*tp_base*/
    0, /*tp_dict*/
    itemgetset_get, /*tp_descr_get*/
    itemgetset_set, /*tp_descr_set*/
    0, /*tp_dictoffset*/
    0, /*tp_init*/
    0, /*tp_alloc*/
    itemgetset_new, /*tp_new*/
    0, /*tp_free*/
    0, /*tp_is_gc*/
};

static PyTypeObject ItemGet_Type = {
    PyVarObject_HEAD_INIT(DEFERRED_ADDRESS(&PyType_Type), 0)
    "recordclass.memoryslots.itemget", /*tp_name*/
    sizeof(struct itemgetset_object), /*tp_basicsize*/
    0, /*tp_itemsize*/
    itemgetset_dealloc, /*tp_dealloc*/
    0, /*tp_print*/
    0, /*tp_getattr*/
    0, /*tp_setattr*/
    0, /*reserved*/
    0, /*tp_repr*/
    0, /*tp_as_number*/
    0, /*tp_as_sequence*/
    0, /*tp_as_mapping*/
    0, /*tp_hash*/
    0, /*tp_call*/
    0, /*tp_str*/
    0, /*tp_getattro*/
    0, /*tp_setattro*/
    0, /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE, /*tp_flags*/
    0, /*tp_doc*/
    0, /*tp_traverse*/
    0, /*tp_clear*/
    0, /*tp_richcompare*/
    0, /*tp_weaklistoffset*/
    0, /*tp_iter*/
    0, /*tp_iternext*/
    itemgetset_methods, /*tp_methods*/
    0, /*tp_members*/
    0, /*tp_getset*/
    0, /*tp_base*/
    0, /*tp_dict*/
    itemgetset_get, /*tp_descr_get*/
    0,              /*tp_descr_set*/
    0, /*tp_dictoffset*/
    0, /*tp_init*/
    0, /*tp_alloc*/
    itemgetset_new, /*tp_new*/
    0, /*tp_free*/
    0, /*tp_is_gc*/
};


// static PyObject* get_item(PyObject *mod, PyObject *args) {
//     PyObject *res;
//     PyObject *obj = PyTuple_GET_ITEM(args, 0);
//     PyObject *ind = PyTuple_GET_ITEM(args, 1);
//     PyObject **ob_items = (PyObject**)((char*)obj + sizeof(PyObject));
//     Py_ssize_t i = PyNumber_AsSsize_t(ind, PyExc_IndexError);
//     if (i == -1 && PyErr_Occurred()) {
//         return NULL;
//     }
//     res = ob_items[i];
//     Py_INCREF(res);
//     return res;
// }

/* List of functions defined in the module */

PyDoc_STRVAR(memoryslotsmodule_doc,
"MemorySlots module provide mutable tuple-like type `memoryslots` and descriptor type `itemgetset`.");

// static PyObject *
// memoryslots_freeze(PyObject *module, PyObject *args)
// {
//     if (Py_SIZE(args) > 2) 
//         return NULL;
//     PyObject *ob = PyTuple_GET_ITEM(args, 0);
//     PyObject *is_copy = PyTuple_GET_ITEM(args, 1);
    
//     if (PyObject_IsInstance(&PyMemorySlotsTypeRO_Type) {
//         Py_INCREF(ob);
//         return ob;
//     }
        
//     if (PyObject_Bool(is_copy))
//         ob = memoryslots_slice(ob, 0, Py_SIZE(ob));
    
//     if (PyObject_IsInstance(&PyMemorySlotsType_Type) {
//         Py_DECREF((PyObject*)Py_TYPE(ob));
//         Py_TYPE(ob) = &PyMemorySlotsType_Type;
//         Py_INCREF((PyObject*)&PyMemorySlotsType_Type);
//     }
    
//     return memoryslots_slice(ob, 0, PyTuple_GET_SIZE(ob));
// }

#if PY_MAJOR_VERSION >= 3
static PyMethodDef memoryslotsmodule_methods[] = {
//   {"getitem", get_item,     METH_VARARGS,   "__getitem__"},
//   {"freeze", memoryslots_freeze,     METH_VARARGS,   "freeze memoryslots object (make it readonly and hashable)"},
   {0, 0, 0, 0}
};

static struct PyModuleDef memoryslotsmodule = {
  #if PY_VERSION_HEX < 0x03020000
    { PyObject_HEAD_INIT(NULL) NULL, 0, NULL },
  #else
    PyModuleDef_HEAD_INIT,
  #endif
    "recordclass.memoryslots",
    memoryslotsmodule_doc,
    -1,
    memoryslotsmodule_methods,
    NULL,
    NULL,
    NULL,
    NULL
};
#endif

#if PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC
PyInit_memoryslots(void)
{
    PyObject *m;
    
    m = PyState_FindModule(&memoryslotsmodule);
    if (m) {
        Py_INCREF(m);
        return m;
    }    

    m = PyModule_Create(&memoryslotsmodule);
    if (m == NULL)
        return NULL;

    if (PyType_Ready(&PyMemorySlots_Type) < 0)
        Py_FatalError("Can't initialize memoryslots type");

    if (PyType_Ready(&PyMemorySlotsReadonly_Type) < 0)
         Py_FatalError("Can't initialize memoryslotsreadonly type");

    if (PyType_Ready(&ItemGetSet_Type) < 0)
        Py_FatalError("Can't initialize itemgetset type");

    if (PyType_Ready(&ItemGet_Type) < 0)
        Py_FatalError("Can't initialize itemget type");

    if (PyType_Ready(&PyMemorySlotsIter_Type) < 0)
        Py_FatalError("Can't initialize memoryslots iter type");
    
    Py_INCREF(&PyMemorySlots_Type);
    PyModule_AddObject(m, "memoryslots", (PyObject *)&PyMemorySlots_Type);

    Py_INCREF(&PyMemorySlotsReadonly_Type);
    PyModule_AddObject(m, "memoryslotsreadonly", (PyObject *)&PyMemorySlotsReadonly_Type);

    Py_INCREF(&ItemGetSet_Type);
    PyModule_AddObject(m, "itemgetset", (PyObject *)&ItemGetSet_Type);

    Py_INCREF(&ItemGet_Type);
    PyModule_AddObject(m, "itemget", (PyObject *)&ItemGet_Type);
    
    Py_INCREF(&PyMemorySlotsIter_Type);    
    PyModule_AddObject(m, "memoryslotsiter", (PyObject *)&PyMemorySlotsIter_Type);
    

    return m;
}
#else
PyMODINIT_FUNC
initmemoryslots(void)
{
    PyObject *m;
    
    m = Py_InitModule3("recordclass.memoryslots", NULL, memoryslotsmodule_doc);
    if (m == NULL)
        return;
    Py_XINCREF(m);

    if (PyType_Ready(&PyMemorySlots_Type) < 0)
         Py_FatalError("Can't initialize memoryslots type");

    if (PyType_Ready(&PyMemorySlotsReadonly_Type) < 0)
         Py_FatalError("Can't initialize memoryslotsreadonly type");
    
    if (PyType_Ready(&ItemGetSet_Type) < 0)
        Py_FatalError("Can't initialize itemgetset type");

    if (PyType_Ready(&ItemGet_Type) < 0)
        Py_FatalError("Can't initialize itemget type");

    if (PyType_Ready(&PyMemorySlotsIter_Type) < 0)
        Py_FatalError("Can't initialize memoryslots iter type");

    Py_INCREF(&PyMemorySlots_Type);
    PyModule_AddObject(m, "memoryslots", (PyObject *)&PyMemorySlots_Type);

    Py_INCREF(&PyMemorySlotsReadonly_Type);
    PyModule_AddObject(m, "memoryslotsreadonly", (PyObject *)&PyMemorySlotsReadonly_Type);
        
    Py_INCREF(&ItemGetSet_Type);
    PyModule_AddObject(m, "itemgetset", (PyObject *)&ItemGetSet_Type);

    Py_INCREF(&ItemGet_Type);
    PyModule_AddObject(m, "itemget", (PyObject *)&ItemGet_Type);
    
    Py_INCREF(&PyMemorySlotsIter_Type);
    PyModule_AddObject(m, "memoryslotsiter", (PyObject *)&PyMemorySlotsIter_Type);

    return;
}
#endif
