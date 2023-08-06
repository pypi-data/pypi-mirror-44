#include "pyconfig.h"
#include "Python.h"
#include <string.h>

#define datatuple_items(type, op) (PyObject**)((char*)(op) + type->tp_basicsize)

// #define dataobject_items(type, op) (PyObject**)((char*)(op)+\
//                                    (type->tp_itemsize?sizeof(PyVarObject):sizeof(PyObject)))

#define dataobject_slots(op) (PyObject**)((char*)(op) + sizeof(PyObject))
#define datatuple_slots(op) (PyObject**)((char*)(op) + sizeof(PyVarObject))

// #define dataobject_numslots(tp) ((tp->tp_itemsize?\
//                                 (tp->tp_basicsize - sizeof(PyVarObject))/sizeof(PyObject*):\
//                                 (tp->tp_basicsize - sizeof(PyObject))/sizeof(PyObject*)) - \
//                                 (tp->tp_dictoffset?1:0) - \
//                                 (tp->tp_weaklistoffset?1:0))

#define datatuple_numslots(tp) ((tp->tp_basicsize - sizeof(PyVarObject))/sizeof(PyObject*) - \
                                (tp->tp_dictoffset?1:0) - \
                                (tp->tp_weaklistoffset?1:0))

#define dataobject_numslots(tp) ((tp->tp_basicsize - sizeof(PyObject))/sizeof(PyObject*)) - \
                                 (tp->tp_dictoffset?1:0) - \
                                 (tp->tp_weaklistoffset?1:0)

// #define dataobject_numitems(type, op) 0
#define datatuple_numitems(op) Py_SIZE(op)

#define dataobject_dictptr(type, op) ((PyObject**)((char*)(op) + type->tp_dictoffset))
#define dataobject_weaklistptr(type, op) ((PyObject**)((char*)op + type->tp_weaklistoffset))
#define dataobject_hasdict(type) (type->tp_dictoffset != 0)
#define dataobject_hasweaklist(type) (type->tp_weaklistoffset != 0)

#define DEFERRED_ADDRESS(addr) 0 

#ifndef Py_RETURN_NOTIMPLEMENTED
#define Py_RETURN_NOTIMPLEMENTED \
    return Py_INCREF(Py_NotImplemented), Py_NotImplemented
#endif

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

// static PyObject*
// getattr_from_module(const char *modname, const char *name)
// {
//     PyObject *mod, *attr;

//     mod = PyImport_ImportModule(modname);
//     if (mod == NULL)
//         return NULL;
//     attr = PyObject_GetAttrString(mod, name);
//     Py_DECREF(mod);
//     return attr;
// }

// static PyObject* find_fields(PyTypeObject* type) {
//     PyTypeObject *tp = type;
//     PyObject *fields = NULL;
    
//     while (!fields || tp != &PyType_Type) {
//         fields = PyDict_GetItemString(tp-tp_dict, "__fields__");
//         if (!fields)
//             tp = tp->base;
//     }
    
//     Py_XINCREF(fields);
//     return fields;
// }

// forward decaration
static Py_ssize_t do_getlen(PyObject *op);
static PyObject* do_getitem(PyObject *op, Py_ssize_t i);


// static PyObject *
// dataobject_alloc(PyTypeObject *type, Py_ssize_t n_items)
// {
//     PyObject *op;
//     Py_ssize_t size;

//     if (type->tp_itemsize)
//         size = _PyObject_VAR_SIZE(type, n_items);
//     else
//         size = _PyObject_SIZE(type);
        
// //     printf("size: %i basicsize: %i base_basicsize %i \n", size, type->tp_basicsize, type->tp_base->tp_basicsize);

//     if (type->tp_flags & Py_TPFLAGS_HAVE_GC)
//         op = _PyObject_GC_Malloc(size);
//     else
//         op = (PyObject *)PyObject_MALLOC(size);

//     if (op == NULL)
//         return PyErr_NoMemory();

//     memset(op, '\0', size);

//     if (type->tp_itemsize)
//         Py_SIZE(op) = n_items;

//     Py_TYPE(op) = type;
//     _Py_NewReference(op);

// //     if (type->tp_flags & Py_TPFLAGS_HEAPTYPE) {
// //         //printf("heap ");
// //         Py_INCREF(type);
// //     }
//     Py_INCREF(type);
    
//     if (type->tp_flags & Py_TPFLAGS_HAVE_GC)
//         PyObject_GC_Track(op);
    
//     //printf("refcount: %i ", Py_REFCNT(op));
    
//     return op;
// }

static PyObject *
dataobject_alloc(PyTypeObject *type, Py_ssize_t n_items)
{
    PyObject *op;
    Py_ssize_t size = _PyObject_SIZE(type);

//     printf("size: %i basicsize: %i base_basicsize %i \n", size, type->tp_basicsize, type->tp_base->tp_basicsize);

    if (type->tp_flags & Py_TPFLAGS_HAVE_GC)
        op = _PyObject_GC_Malloc(size);
    else
        op = (PyObject *)PyObject_MALLOC(size);

    if (op == NULL)
        return PyErr_NoMemory();

    memset(op, '\0', size);

    Py_TYPE(op) = type;
    _Py_NewReference(op);

//     if (type->tp_flags & Py_TPFLAGS_HEAPTYPE) {
//         //printf("heap ");
//         Py_INCREF(type);
//     }
    Py_INCREF(type);
    
    if (type->tp_flags & Py_TPFLAGS_HAVE_GC)
        PyObject_GC_Track(op);
    
    //printf("refcount: %i ", Py_REFCNT(op));
    
    return op;
}

// static int _property_set(PyObject *op, PyObject *key, PyObject *val);

// static PyObject *undefined;

static PyObject*
dataobject_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyObject *op;
    Py_ssize_t n_slots;
    PyObject *tmp;
    Py_ssize_t n_args;
    PyObject **items, **pp;
    PyObject *v;

    if (Py_TYPE(args) == &PyTuple_Type) {
        tmp = args;
        Py_INCREF(args);
    } else {
        tmp = PySequence_Tuple(args);
        if (tmp == NULL) {
            //printf("args error\n");
            return NULL;
        }
    }

    n_args = PyTuple_GET_SIZE(tmp);

    n_slots = dataobject_numslots(type);
    if (n_args > n_slots) {
//         printf("\nnslots=%i nargs=%i\n", n_slots, n_args);
//         if (!type->tp_dictoffset && kwds) {
//             PyErr_SetString(PyExc_TypeError,
//                             "keyword arguments are not allowed in argsonly mode without __dict__");
//         } else {
//             PyErr_SetString(PyExc_TypeError,
//                             "number of the arguments should not be greater than the number of the slots");
//         }
        PyErr_SetString(PyExc_TypeError,
                        "number of the arguments should not be greater than the number of the slots");
        Py_DECREF(tmp);
        return NULL;            
    }

    op = type->tp_alloc(type, 0);

    pp = ((PyTupleObject*)tmp)->ob_item;
    items = dataobject_slots(op);
    while (n_args--) {
        v = *(pp++);
        Py_INCREF(v);
        *(items++) = v;
        n_slots--;
    }
    
    while (n_slots--) {
        Py_INCREF(Py_None);
        *(items++) = Py_None;
    }

    Py_DECREF(tmp);
    
    if (kwds) {
        if (type->tp_dictoffset) {
            PyObject **dictptr = dataobject_dictptr(type, op);
            PyObject *dict;
            if (*dictptr)
                dict = *dictptr;
            else {
                dict = PyDict_New();
                *dictptr = dict;
            }

            if (PyDict_Update(dict, kwds) == -1) {
                PyErr_SetString(PyExc_TypeError, "__dict__ update is failed");
                return NULL;            
            }
        } else {
            PyErr_SetString(PyExc_TypeError, "invalid kwargs");
            return NULL;            
        }        
    }

    return op;
}

// static PyObject*
// dataobject_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
// {
//     PyObject *op;
//     Py_ssize_t n_slots, n_items, n_diff;
//     PyObject *tmp;
//     Py_ssize_t n_args;
//     PyObject **items, **pp;

//     if (Py_TYPE(args) == &PyTuple_Type) {
//         tmp = args;
//         Py_INCREF(args);
//     } else {
//         tmp = PySequence_Tuple(args);
//         if (tmp == NULL) {
//             //printf("args error\n");
//             return NULL;
//         }
//     }

//     n_args = PyTuple_GET_SIZE(tmp);

//     if (!type->tp_itemsize) {
//         n_slots = dataobject_numslots(type);
//         n_items = 0;
//         if (n_args != n_slots) {
// //             printf("\nnslots=%i nitems=%i nargs=%i\n", n_slots, n_items, n_args);
//             PyErr_SetString(PyExc_TypeError,
//                             "number of the arguments should be equal to the number of the slots");
//             Py_DECREF(tmp);
//             return NULL;            
//         }
//     } else {
//         n_slots = datatuple_numslots(type);
//         n_items = n_args - n_slots;
//         if (n_args < n_slots) {
// //             printf("\nnslots=%i nitems=%i nargs=%i\n", n_slots, n_items, n_args);
//             PyErr_SetString(PyExc_TypeError,
//                             "number of the arguments should be greater or equal than the number of slots");
//             Py_DECREF(tmp);
//             return NULL;            
//         }
//     }

//     n_diff = n_args - n_slots;

//     op = type->tp_alloc(type, n_items);

// //     printf("is_gc: %i base_is_gc %i ", PyType_IS_GC(type), PyType_IS_GC(type->tp_base));
// //     printf("allocated\n");

//     pp = ((PyTupleObject*)tmp)->ob_item;
//     items = dataobject_items(type, op);
//     if (n_slots) {
//         Py_ssize_t n = n_slots;
//         while (n-- > 0) {
//             PyObject *v;

//             v = *(pp++);
//             Py_INCREF(v);
//             *(items++) = v;
//         }
//     }

//     if (type->tp_dictoffset)
//         items++;
//     if (type->tp_weaklistoffset)
//         items++;

//     if (n_diff > 0) {
//         Py_ssize_t n = n_diff;
//         while (n-- > 0) {
//             PyObject *v;

//             v = *(pp++);
//             Py_INCREF(v);
//             *(items++) = v;
//         }
//     }

//     Py_DECREF(tmp);

//     return op;
// }

static int
dataobject_clear(PyObject *op)
{
    Py_ssize_t n_slots;
    PyObject **items;
    PyTypeObject *type = Py_TYPE(op);
    PyObject *v;
    
    n_slots = dataobject_numslots(type);

    items = dataobject_slots(op);
    while (n_slots-- > 0) {
        v = *items;
        Py_DECREF(v);
        *items = NULL;
        items++;
    }

    if (type->tp_dictoffset) {
        PyObject **dictptr = dataobject_dictptr(type, op);
        if (dictptr && *dictptr)
            Py_CLEAR(*dictptr);
    }

    if (type->tp_weaklistoffset)
        PyObject_ClearWeakRefs(op);

    return 0;
}

// static int
// dataobject_clear(PyObject *op)
// {
//     Py_ssize_t n_slots, n_items;
//     PyObject **items;
//     PyTypeObject *type = Py_TYPE(op);
    
//     if (!type->tp_itemsize) {
//         n_slots = dataobject_numslots(type);

//         items = dataobject_slots(op);
//         if (n_slots) {
//             while (n_slots-- > 0) {
//                 PyObject *v;

//                 v = *items;
//                 Py_DECREF(v);
//                 *items = NULL;
//                 items++;
//             }
//         }

//     } else {
//         n_slots = datatuple_numslots(type);

//         items = datatuple_slots(op);
//         if (n_slots) {
//             while (n_slots-- > 0) {
//                 PyObject *v;

//                 v = *items;
//                 Py_DECREF(v);
//                 *items = NULL;
//                 items++;
//             }
//         }

//         if (type->tp_dictoffset)
//             items++;
//         if (type->tp_weaklistoffset)
//             items++;        

//         n_items = Py_SIZE(op);
//         if (n_items) {
//             while (n_items-- > 0) {
//                 PyObject *v;

//                 v = *items;
//                 Py_DECREF(v);
//                 *items = NULL;
//                 items++;
//             }
//         }
//     }

//     if (type->tp_dictoffset) {
//         PyObject **dictptr = dataobject_dictptr(type, op);
//         if (dictptr && *dictptr)
//             Py_CLEAR(*dictptr);
//     }

//     if (type->tp_weaklistoffset)
//         PyObject_ClearWeakRefs(op);

//     return 0;
// }

static void
dataobject_free(void *op)
{
    PyTypeObject *type = Py_TYPE((PyObject*)op);

    Py_DECREF(type);

    if PyType_IS_GC(type)
        PyObject_GC_Del((PyObject*)op);
    else
        PyObject_Del((PyObject*)op);
}

static void
dataobject_dealloc(PyObject *op)
{
    PyTypeObject *tp = Py_TYPE(op); 

    if (PyType_IS_GC(tp)) {
        PyObject_GC_UnTrack(op);
    } else {
        dataobject_clear(op);        
    }

    tp->tp_free((PyObject *)op);
}

static int
dataobject_traverse(PyObject *op, visitproc visit, void *arg)
{
    Py_ssize_t n_slots;
    PyObject **items;
    PyTypeObject *type = Py_TYPE(op);
    PyObject *v;

    n_slots = dataobject_numslots(type);

    if (n_slots) {
        items = dataobject_slots(op);
        while (n_slots--) {
            v = *(items++);
            Py_VISIT(v);
        }
    }

    if (type->tp_dictoffset) {
        PyObject **dictptr = dataobject_dictptr(type, op);
        if (dictptr && *dictptr)
            Py_VISIT(*dictptr);
    }

    return 0;
}

// static int
// dataobject_traverse(PyObject *op, visitproc visit, void *arg)
// {
//     Py_ssize_t n_slots, n_items;
//     PyObject **items;
//     PyTypeObject *type = Py_TYPE(op);

//     n_slots = dataobject_numslots(type);
//     n_items = dataobject_numitems(type, op);

//     if (n_slots) {
//         items = dataobject_items(type, op);
//         while (n_slots--) {
//             PyObject *v;

//             v = *(items++);
//             Py_VISIT(v);
//         }
//     }

//     if (n_items) {
//         items = datatuple_items(type, op);
//         while (n_items--) {
//             PyObject *v;

//             v = *(items++);
//             Py_VISIT(v);
//         }
//     }

//     if (type->tp_dictoffset) {
//         PyObject **dictptr = dataobject_dictptr(type, op);
//         if (dictptr && *dictptr)
//             Py_VISIT(*dictptr);
//     }

//     return 0;
// }

// static PyObject *
// dataobject_item(PyObject *op, Py_ssize_t i)
// {
//     PyObject **items;
//     PyObject *v;
//     PyTypeObject *type = Py_TYPE(op);

//     Py_ssize_t n_slots = dataobject_numslots(type);
//     Py_ssize_t n_items = dataobject_numitems(type, op);
//     Py_ssize_t n = n_slots + n_items;

// //     if (i < 0)
// //         i += n;
//     if (i < 0 || i >= n) {
//         PyErr_SetString(PyExc_IndexError, "index out of range");
//         return NULL;
//     }

//     if (i >= n_slots) {
//         items = datatuple_items(type, op);
//         i -= n_slots;
//     } else {
//         items = dataobject_items(type, op);
//     }

//     v = items[i];
//     Py_INCREF(v);
//     return v;
// }


static PyObject *
dataobject_item(PyObject *op, Py_ssize_t i)
{
    PyObject **items;
    PyObject *v;
    PyTypeObject *type = Py_TYPE(op);
    
    Py_ssize_t n_slots = dataobject_numslots(type);

    if (i < 0 || i >= n_slots) {
        PyErr_SetString(PyExc_IndexError, "index out of range");
        return NULL;
    }

    items = dataobject_slots(op);
    v = items[i];
    Py_INCREF(v);
    return v;
}


// static int
// dataobject_ass_item(PyObject *op, Py_ssize_t i, PyObject *val)
// {
//     Py_ssize_t n_slots, n_items, n;
//     PyObject **items;
//     PyTypeObject *type = Py_TYPE(op);
//     PyObject* old_val;
    
//     n_slots = dataobject_numslots(type);
//     n_items = dataobject_numitems(type, op);

//     n = n_slots + n_items;

// //     if (i < 0)
// //         i += n;
//     if (i < 0 || i >= n) {
//         PyErr_SetString(PyExc_IndexError, "index out of range");
//         return -1;
//     }

//     if (i >= n_slots) {
//         items = datatuple_items(type, op);
//         i -= n_slots;
//     } else {
//         items = dataobject_items(type, op);
//     }

//     items += i;

//     old_val = *items;
//     if (old_val)
//         Py_DECREF(old_val);
//     Py_INCREF(val);
//     *items = val;
//     return 0;
// }

static int
dataobject_ass_item(PyObject *op, Py_ssize_t i, PyObject *val)
{
    PyObject **items;
    PyTypeObject *type = Py_TYPE(op);
    PyObject* old_val;
        
    Py_ssize_t n = dataobject_numslots(type);

//     if (i < 0)
//         i += n;
    if (i < 0 || i >= n) {
        PyErr_SetString(PyExc_IndexError, "index out of range");
        return -1;
    }

    items = dataobject_slots(op);

    items += i;

    old_val = *items;
    if (old_val)
        Py_DECREF(old_val);
    Py_INCREF(val);
    *items = val;
    return 0;
}


// static PyObject*
// dataobject_subscript(PyObject* op, PyObject* item)
// {
//     PyTypeObject *type = Py_TYPE(op);
//     Py_ssize_t i, n, n_slots;        
//     PyObject **items;
//     PyObject *v;

//     i = (Py_ssize_t)PyNumber_AsSsize_t(item, PyExc_IndexError);
//     if (i == -1 && PyErr_Occurred())
//         return NULL;            

//     if (!type->tp_itemsize) {
//         n_slots = (type->tp_basicsize - sizeof(PyObject))/sizeof(PyObject*);
//         if (type->tp_dictoffset)
//             n_slots--;
//         if (type->tp_weaklistoffset)
//             n_slots--;

//         if (i < 0)
//             i += n_slots;
//         if (i < 0 || i >= n_slots) goto err;
// //         printf("i=%i n=%i\n", i, n_slots);
//         items = dataobject_slots(op);
//     } else {
//         n_slots = (type->tp_basicsize - sizeof(PyVarObject))/sizeof(PyObject*);
//         if (type->tp_dictoffset)
//             n_slots--;
//         if (type->tp_weaklistoffset)
//             n_slots--;

//         n = n_slots + Py_SIZE(op);

//         if (i < 0)
//             i += n;
//         if (i < 0 || i >= n) goto err;
// //         printf("i=%i n=%i\n", i, n);
//         if (i < n_slots)
//             items = datatuple_slots(op);
//         else {
//             items = datatuple_items(type, op);
//             i -= n_slots;            
//         }
//     }

//     v = items[i];
//     Py_INCREF(v);
//     return v;

// err:
//     PyErr_SetString(PyExc_IndexError, "index out of range");
//     return NULL;
// }

static PyObject*
dataobject_subscript(PyObject* op, PyObject* item)
{
    Py_ssize_t i, n;
    PyObject **items;
    PyObject *v;
    PyTypeObject *type = Py_TYPE(op);
    
    n = dataobject_numslots(type);
    
    i = (Py_ssize_t)PyNumber_AsSsize_t(item, PyExc_IndexError);
    if (i < 0) {
        if (i == -1 && PyErr_Occurred())
            return NULL;            
        i += n;
    }
        
    if (i < 0 || i >= n) {
        PyErr_SetString(PyExc_IndexError, "index out of range");
        return NULL;
    }
    //printf("i=%i n=%i\n", i, n);
    
    items = dataobject_slots(op);
    v = items[i];
    Py_INCREF(v);
    return v;
}


// static int
// dataobject_ass_subscript(PyObject* op, PyObject* item, PyObject *val)
// {
//     Py_ssize_t i, n, n_items, n_slots;
//     PyObject **items;
//     PyTypeObject *type = Py_TYPE(op);
//     PyObject *old_val;

//     n_slots = dataobject_numslots(type);
//     n_items = dataobject_numitems(type, op);

//     n = n_slots + n_items;

//     i = (Py_ssize_t)PyNumber_AsSsize_t(item, PyExc_IndexError);
//     if (i < 0) {
//         if (i == -1 && PyErr_Occurred())
//             return -1;            
//         i += n;
//     }

//     if (i < 0 || i >= n) {
//         PyErr_SetString(PyExc_IndexError, "index out of range");
//         return -1;
//     }
//      //printf("i=%i n=%i\n", i, n);

//     if (i < n_slots) {
//         items = dataobject_items(type, op);
//     } else {
//         items = datatuple_items(type, op);
//         i -= n_slots;
//     }

//     items += i;

//     old_val = *items;
//     if (old_val)
//         Py_DECREF(old_val);
//     Py_INCREF(val);
//     *items = val;
//     return 0;
// }

static int
dataobject_ass_subscript(PyObject* op, PyObject* item, PyObject *val)
{
    Py_ssize_t i, n;
    PyObject **items;
    PyTypeObject *type = Py_TYPE(op);
    
    n = dataobject_numslots(type);
    
    i = (Py_ssize_t)PyNumber_AsSsize_t(item, PyExc_IndexError);
    if (i < 0) {
        if (i == -1 && PyErr_Occurred())
            return -1;            
        i += n;
    }
        
    if (i < 0 || i >= n) {
        PyErr_SetString(PyExc_IndexError, "index out of range");
        return -1;
    }
     //printf("i=%i n=%i\n", i, n);
    
    items = dataobject_slots(op);

    Py_INCREF(val);
    items[i] = val;
    return 0;
}


#ifndef _PyHASH_MULTIPLIER
#define _PyHASH_MULTIPLIER 1000003UL
#endif

static long
dataobject_hash(PyObject *op)
{
    unsigned long x;
    long y;
    Py_ssize_t i, len = do_getlen(op);
    long mult = _PyHASH_MULTIPLIER;
    PyObject *o;

    x = 0x345678L;
    for(i=0; i<len; i++) {
        o = do_getitem(op, i);
//         Py_INCREF(o);
        y = PyObject_Hash(o);
        Py_DECREF(o);
        if (y == -1)
            return -1;
        x = (x ^ y) * mult;
        mult += (long)(82520L + len + len);
    }

    x += 97531L;
    if (x == (unsigned long)-1)
        x = -2;
    return x;
}

static PyObject *
dataobject_richcompare(PyObject *v, PyObject *w, int op)
{
    Py_ssize_t i, k;
    Py_ssize_t vlen, wlen;
    PyObject *vv;
    PyObject *ww;
    PyObject *ret;

    if (!(Py_TYPE(v) == Py_TYPE(w)) || (!PyType_IsSubtype(Py_TYPE(w), Py_TYPE(v))))
        Py_RETURN_NOTIMPLEMENTED;

    vlen = do_getlen(v);
    wlen = do_getlen(w);

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
        vv = do_getitem(v, i);
        ww = do_getitem(w, i);
//         Py_INCREF(vv);
//         Py_INCREF(ww);
        k = PyObject_RichCompareBool(vv, ww, Py_EQ);
        Py_DECREF(vv);
        Py_DECREF(ww);
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
    vv = do_getitem(v, i);
    ww = do_getitem(w, i); 
//     Py_INCREF(vv);
//     Py_INCREF(ww);    
    ret = PyObject_RichCompare(vv, ww, op);
    Py_DECREF(vv);
    Py_DECREF(ww);

    return ret;
}

// PyDoc_STRVAR(dataobject_len_doc,
// "T.__len__() -- len of T");

static Py_ssize_t
dataobject_len(PyObject *op)
{
    PyTypeObject *type = Py_TYPE(op);
    Py_ssize_t n;

    n = dataobject_numslots(type);
    if (type->tp_itemsize)
        n += Py_SIZE(op);

    return n;
}


// static Py_ssize_t
// dataobject_len_slots(PyObject *op)
// {
//     PyTypeObject *type = Py_TYPE(op);
//     Py_ssize_t n = dataobject_numslots(type);

//     return n;
// }

// static Py_ssize_t
// dataobject_len_varsize(PyObject *op)
// {
//     Py_ssize_t n = Py_SIZE(op);

//     return n;
// }

static PySequenceMethods dataobject_as_sequence = {
    (lenfunc)dataobject_len,                          /* sq_length */
    0,                                              /* sq_concat */
    0,                                              /* sq_repeat */
    (ssizeargfunc)dataobject_item,                    /* sq_item */
    0,                                              /* sq_slice */
    (ssizeobjargproc)dataobject_ass_item,             /* sq_ass_item */
    0,                                              /* sq_ass_slice */
    0,                                              /* sq_contains */
};

// PySequenceMethods dataobject_as_sequence_slots = {
//     (lenfunc)dataobject_len_slots,                          /* sq_length */
//     0,                                              /* sq_concat */
//     0,                                              /* sq_repeat */
//     (ssizeargfunc)dataobject_item_slots,                    /* sq_item */
//     0,                                              /* sq_slice */
//     (ssizeobjargproc)dataobject_ass_item_slots,             /* sq_ass_item */
//     0,                                              /* sq_ass_slice */
//     0,                                              /* sq_contains */
// };

static PyMappingMethods dataobject_as_mapping = {
    (lenfunc)dataobject_len,                          /* mp_len */
    (binaryfunc)dataobject_subscript,                 /* mp_subscr */
    (objobjargproc)dataobject_ass_subscript,          /* mp_ass_subscr */
};


// PyMappingMethods dataobject_as_mapping_slots = {
//     (lenfunc)dataobject_len_slots,                          /* mp_len */
//     (binaryfunc)dataobject_subscript_slots,                 /* mp_subscr */
//     (objobjargproc)dataobject_ass_subscript_slots,          /* mp_ass_subscr */
// };


PyDoc_STRVAR(dataobject_sizeof_doc,
"T.__sizeof__() -- size of T");

static PyObject *
dataobject_sizeof(PyObject *self)
{
    PyTypeObject *tp;
    Py_ssize_t res;

    tp = Py_TYPE(self);
    res = tp->tp_basicsize;
    if (tp->tp_itemsize)
        res += Py_SIZE(self) * sizeof(PyObject*);

    return PyLong_FromSsize_t(res);
}

PyDoc_STRVAR(dataobject_copy_doc,
"T.__copy__() -- copy of T");

static PyObject *
dataobject_copy(PyObject* op)
{
    PyTypeObject *type = Py_TYPE(op);

    return type->tp_new(type, op, NULL);
}

// PyDoc_STRVAR(dataobject_get_item_offset_doc,
// "T.itemoffset(index) -- get offset of the item with the index (class method)");

// static PyObject*
// dataobject_get_item_offset(PyTypeObject *type, PyObject *index)
// {
//     Py_ssize_t i, n_slots;
//     Py_ssize_t offset;
    
//     i = (Py_ssize_t)PyNumber_AsSsize_t(index, PyExc_IndexError);
//     if (i == -1 && PyErr_Occurred())
//         return NULL;            
    
//     n_slots = dataobject_numslots(type);

//     if (i < 0) goto err;

//     if (i<n_slots) {
//         if (type->tp_itemsize) 
//             offset = sizeof(PyVarObject);
//         else
//             offset = sizeof(PyObject);
//     } else {
//         if (!type->tp_itemsize) goto err;
//         offset = type->tp_basicsize;
//         i -= n_slots;
//     }
//     offset += i * sizeof(PyObject*);

//     return PyLong_FromSsize_t(offset);
    
// err:
//     PyErr_SetString(PyExc_IndexError, "index out of range");
//     return NULL;            
// }

#if PY_MAJOR_VERSION == 2

static PyObject *
dataobject_repr(PyObject *self)
{
    Py_ssize_t i, n, n_fs = 0;
    PyObject *fs;
    PyTypeObject *tp = Py_TYPE(self);
    PyObject *tp_name = PyObject_GetAttrString((PyObject*)tp, "__name__");
    PyObject *text, *t;
    PyObject *lc = PyUnicode_FromString("(");
    PyObject *rc = PyUnicode_FromString(")");
    PyObject *cc = PyUnicode_FromString(", ");
    PyObject *eq = PyUnicode_FromString("=");

    n = do_getlen(self);
    if (n == 0) {
        PyObject *s = PyUnicode_FromString("()");
        text = PyUnicode_Concat(tp_name, s);
        Py_DECREF(tp_name);
        Py_DECREF(s);

        Py_DECREF(lc);
        Py_DECREF(rc);
        Py_DECREF(cc);
        Py_DECREF(eq);

        return text;
    }

    i = Py_ReprEnter((PyObject *)self);
    if (i != 0) {
        Py_DECREF(tp_name);
        Py_DECREF(lc);
        Py_DECREF(rc);
        Py_DECREF(cc);
        Py_DECREF(eq);

        return i > 0 ? PyUnicode_FromString("(...)") : NULL;
    }

    text = PyUnicode_Concat(tp_name, lc);
    Py_DECREF(tp_name);

    fs = PyObject_GetAttrString(self, "__fields__");
    if (fs) {
        if (Py_TYPE(fs) == &PyTuple_Type) {
            n_fs = PyObject_Length(fs);
        } else {
            n_fs = (Py_ssize_t)PyNumber_AsSsize_t(fs, PyExc_IndexError);
            if (n_fs < 0) {
                Py_DECREF(fs);
                Py_DECREF(tp_name);
                Py_DECREF(lc);
                Py_DECREF(rc);
                Py_DECREF(cc);
                Py_DECREF(eq);
                return NULL;
            }
            n_fs = 0;
        }
    } else
        PyErr_Clear();

    /* Do repr() on each element. */
    for (i = 0; i < n; ++i) {
        PyObject *s, *ob;
        PyObject *fn;

        if (n_fs > 0 && i < n_fs) {
            fn = PyTuple_GET_ITEM(fs, i);

            t = text;
            text = PyUnicode_Concat(t, fn);
            Py_DECREF(t);

            t = text;
            text = PyUnicode_Concat(t, eq);
            Py_DECREF(t);
        }

        ob = do_getitem(self, i);
        if (ob == NULL)
            goto error;

        s = PyObject_Repr(ob);
        if (s == NULL) {
            Py_DECREF(ob);
            goto error;
        }

        t = text;
        text = PyUnicode_Concat(t, s);
        Py_DECREF(t);
        Py_DECREF(s);

        Py_DECREF(ob);

        if (i < n-1) {
            t = text;
            text = PyUnicode_Concat(t, cc);
            Py_DECREF(t);
        }
    }

    if (tp->tp_dictoffset) {
        PyObject *dict = PyObject_GetAttrString(self, "__dict__");
        PyObject *s;

        if (dict) {            
            if (PyObject_IsTrue(dict)) {
                PyObject *aa = PyUnicode_FromString(", **");

                t = text;
                text = PyUnicode_Concat(t, aa);
                Py_DECREF(t);

                s = PyObject_Repr(dict);
                t = text;
                text = PyUnicode_Concat(t, s);
                Py_DECREF(t);
                Py_DECREF(s);
            }
            Py_DECREF(dict);
        }
    }        
    
    t = text;
    text = PyUnicode_Concat(text, rc);
    Py_DECREF(t);

    Py_ReprLeave((PyObject *)self);

    Py_XDECREF(fs);
    
    Py_DECREF(lc);
    Py_DECREF(rc);
    Py_DECREF(cc);
    Py_DECREF(eq);

    return text;

error:
    Py_ReprLeave((PyObject *)self);

    Py_XDECREF(fs);

    Py_DECREF(lc);
    Py_DECREF(rc);
    Py_DECREF(cc);
    Py_DECREF(eq);

    return NULL;
}

#else

static PyObject *
dataobject_repr(PyObject *self)
{
    Py_ssize_t i, n, n_fs = 0;
    _PyUnicodeWriter writer;
    PyObject *fs;
    PyTypeObject *tp = Py_TYPE(self);
    PyObject *tp_name = PyObject_GetAttrString((PyObject*)tp, "__name__");
    PyObject *text;

    fs = PyObject_GetAttrString(self, "__fields__");
    if (fs) {
        if (Py_TYPE(fs) == &PyTuple_Type) {
            n_fs = PyObject_Length(fs);
        } else {
            n_fs = (Py_ssize_t)PyNumber_AsSsize_t(fs, PyExc_IndexError);
            if (n_fs < 0) {
                Py_DECREF(fs);
                Py_DECREF(tp_name);
                return NULL;
            }
            n_fs = 0;
        }
    } else
        PyErr_Clear();
//     printf("%i\n", n_fs);

    n = do_getlen(self);
    if (n == 0) {
        PyObject *s = PyUnicode_FromString("()");
        text = PyUnicode_Concat(tp_name, s);
        Py_DECREF(s);
        Py_DECREF(tp_name);
        return text;
    }

    i = Py_ReprEnter((PyObject *)self);
    if (i != 0) {
        Py_DECREF(tp_name);
        return i > 0 ? PyUnicode_FromString("(...)") : NULL;
    }

    _PyUnicodeWriter_Init(&writer);
    writer.overallocate = 1;
    if (n > 1) {
        /* "(" + "1" + ", 2" * (len - 1) + ")" */
        writer.min_length = 1 + 1 + (2 + 1) * (n-1) + 1;
    }
    else {
        /* "(1,)" */
        writer.min_length = 4;
    }

    if (_PyUnicodeWriter_WriteStr(&writer, tp_name) < 0)
        goto error;

    Py_DECREF(tp_name);

    if (_PyUnicodeWriter_WriteChar(&writer, '(') < 0)
        goto error;

    /* Do repr() on each element. */
    for (i = 0; i < n; ++i) {
        PyObject *s, *ob;
        PyObject *fn;

        if (n_fs > 0 && i < n_fs) {
            fn = PyTuple_GET_ITEM(fs, i);
            Py_INCREF(fn);
            if (_PyUnicodeWriter_WriteStr(&writer, fn) < 0) {
                Py_DECREF(fn);
                goto error;
            }
            Py_DECREF(fn);
            if (_PyUnicodeWriter_WriteChar(&writer, '=') < 0)
                goto error;
        }

        ob = do_getitem(self, i);
        if (ob == NULL)
            goto error;

        s = PyObject_Repr(ob);
        if (s == NULL) {
            Py_DECREF(ob);
            goto error;
        }

        if (_PyUnicodeWriter_WriteStr(&writer, s) < 0) {
            Py_DECREF(s);
            Py_DECREF(ob);
            goto error;
        }
        Py_DECREF(s);
        Py_DECREF(ob);

        if (i < n-1) {
            if (_PyUnicodeWriter_WriteASCIIString(&writer, ", ", 2) < 0)
                goto error;
        }
    }

    Py_XDECREF(fs);
    
    if (tp->tp_dictoffset) {
        PyObject *dict = PyObject_GetAttrString(self, "__dict__");
        PyObject *s;

        if (dict) {            
            if (PyObject_IsTrue(dict)) {
                if (_PyUnicodeWriter_WriteASCIIString(&writer, ", **", 4) < 0)
                    goto error;
                s = PyObject_Repr(dict);
                if (_PyUnicodeWriter_WriteStr(&writer, s) < 0) {
                    Py_DECREF(s);
                    Py_DECREF(dict);
                    goto error;
                }
                Py_DECREF(s);
            }
            Py_DECREF(dict);
        }
    }        
    
    writer.overallocate = 0;

    if (_PyUnicodeWriter_WriteChar(&writer, ')') < 0)
        goto error;

    Py_ReprLeave((PyObject *)self);
    return _PyUnicodeWriter_Finish(&writer);

error:
    Py_XDECREF(fs);

    _PyUnicodeWriter_Dealloc(&writer);
    Py_ReprLeave((PyObject *)self);
    return NULL;
}
#endif

PyDoc_STRVAR(dataobject_reduce_doc,
"T.__reduce__()");

static PyObject *
dataobject_reduce(PyObject *ob)
{
    PyObject *args;
    PyObject *result;
    PyTypeObject *tp = Py_TYPE(ob);
    PyObject *kw = NULL;
    PyObject **dictptr;

    args = PySequence_Tuple(ob);
    if (args == NULL)
        return NULL;

    if (tp->tp_dictoffset) {
        dictptr = dataobject_dictptr(tp, ob);
        if (dictptr) {
            kw = *dictptr;
            if (kw) Py_INCREF(kw);
        }
    }
    if (kw) {
        result = PyTuple_Pack(3, Py_TYPE(ob), args, kw);
//         Py_DECREF(kw);
    } else
        result = PyTuple_Pack(2, Py_TYPE(ob), args);
//     Py_DECREF(args);

    return result;
}

PyDoc_STRVAR(dataobject_getnewargs_doc,
"T.__getnewargs__()");

static PyObject *
dataobject_getnewargs(PyObject *ob)
{
    PyObject *args;

    args = PySequence_Tuple(ob);
    if (args == NULL)
        return NULL;

    return args;
}

PyDoc_STRVAR(dataobject_getstate_doc,
"T.__getstate__()");

static PyObject *
dataobject_getstate(PyObject *ob) {
    PyTypeObject *tp = Py_TYPE(ob);
    PyObject *kw = NULL;
    PyObject **dictptr;

    if (tp->tp_dictoffset) {
        dictptr = dataobject_dictptr(tp, ob);
        if (dictptr) {
            kw = *dictptr;
            if (kw) {
                Py_INCREF(kw);
                return kw;
            }
        }
    }

    Py_INCREF(Py_None);
    return Py_None;
}

PyDoc_STRVAR(dataobject_setstate_doc,
"T.__setstate__()");

static PyObject*
dataobject_setstate(PyObject *ob, PyObject *state) {
    PyTypeObject *tp = Py_TYPE(ob);
    PyObject **dictptr;
    PyObject *dict;

    if (!state || state == Py_None)
        return 0;

    if (tp->tp_dictoffset) {
        dictptr = dataobject_dictptr(tp, ob);
        dict = *dictptr;
        if (!dict) {
            dict = PyDict_New();
            if (!dict) {
                PyErr_SetString(PyExc_TypeError, "failed to create new dict");
                return NULL;                                    
            }
            *dictptr = dict;
        }        
        if (PyDict_Update(dict, state) < 0) {
            PyErr_SetString(PyExc_TypeError, "dict update failed");
            return NULL;                        
        }
    } else {
        PyErr_SetString(PyExc_TypeError, "object has no __dict__");
        return NULL;                                            
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef dataobject_methods[] = {
    {"__copy__", (PyCFunction)dataobject_copy, METH_NOARGS, dataobject_copy_doc},
//     {"__len__", (PyCFunction)dataobject_len, METH_NOARGS, dataobject_len_doc},
    {"__sizeof__",      (PyCFunction)dataobject_sizeof, METH_NOARGS, dataobject_sizeof_doc},
    {"__reduce__",      (PyCFunction)dataobject_reduce, METH_NOARGS, dataobject_reduce_doc},
    {"__getstate__",      (PyCFunction)dataobject_getstate, METH_NOARGS, dataobject_getstate_doc},
    {"__getnewargs__",      (PyCFunction)dataobject_getnewargs, METH_NOARGS, dataobject_getnewargs_doc},
    {"__setstate__",      (PyCFunction)dataobject_setstate, METH_O, dataobject_setstate_doc},
    {NULL}
};

PyDoc_STRVAR(dataobject_doc,
"dataobject(...) --> dataobject\n\n\
");

static PyTypeObject PyDataObject_Type = {
    PyVarObject_HEAD_INIT(DEFERRED_ADDRESS(&PyType_Type), 0)
    "recordclass.dataobject.dataobject",        /* tp_name */
    sizeof(PyObject),                       /* tp_basicsize */
    0,                                      /* tp_itemsize */
    /* methods */
    (destructor)dataobject_dealloc,           /* tp_dealloc */
    0,                                      /* tp_print */
    0,                                      /* tp_getattr */
    0,                                      /* tp_setattr */
    0,                                      /* tp_reserved */
    dataobject_repr,                           /* tp_repr */
    0,                                      /* tp_as_number */
    &dataobject_as_sequence,                  /* tp_as_sequence */
    &dataobject_as_mapping,                   /* tp_as_mapping */
    dataobject_hash,                          /* tp_hash */
    0,                                      /* tp_call */
    0,                                      /* tp_str */
    PyObject_GenericGetAttr,                /* tp_getattro */
    PyObject_GenericSetAttr,                /* tp_setattro */
    0,                                      /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
                                            /* tp_flags */
    dataobject_doc,                           /* tp_doc */
    0,                      /* tp_traverse */
    0,                         /* tp_clear */
    dataobject_richcompare,                   /* tp_richcompare */
    0,                                      /* tp_weaklistoffset*/
    0,                                      /* tp_iter */
    0,                                      /* tp_iternext */
    dataobject_methods,                       /* tp_methods */
    0,                                      /* tp_members */
    0,                                      /* tp_getset */
    0,                                      /* tp_base */
    0,                                      /* tp_dict */
    0,                                      /* tp_descr_get */
    0,                                      /* tp_descr_set */
    0,                                      /* tp_dictoffset */
    0,                                      /* tp_init */
    dataobject_alloc,                         /* tp_alloc */
    dataobject_new,                   /* tp_new */
    dataobject_free,                          /* tp_free */
    0                                       /* tp_is_gc */
};

/////////////// datatuple /////////////////////////////////

static PyObject *
datatuple_alloc(PyTypeObject *type, Py_ssize_t n_items)
{
    PyObject *op;
    Py_ssize_t size = _PyObject_VAR_SIZE(type, n_items);
        
//     printf("size: %i basicsize: %i base_basicsize %i \n", size, type->tp_basicsize, type->tp_base->tp_basicsize);

    if (type->tp_flags & Py_TPFLAGS_HAVE_GC)
        op = _PyObject_GC_Malloc(size);
    else
        op = (PyObject *)PyObject_MALLOC(size);

    if (op == NULL)
        return PyErr_NoMemory();

    memset(op, '\0', size);

    Py_SIZE(op) = n_items;
    Py_TYPE(op) = type;
    _Py_NewReference(op);

//     if (type->tp_flags & Py_TPFLAGS_HEAPTYPE) {
//         //printf("heap ");
//         Py_INCREF(type);
//     }
    Py_INCREF(type);
    
    if (type->tp_flags & Py_TPFLAGS_HAVE_GC)
        PyObject_GC_Track(op);
    
    //printf("refcount: %i ", Py_REFCNT(op));
    
    return op;
}

static PyObject*
datatuple_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyObject *op;
    Py_ssize_t n_slots, n_items;
    PyObject *tmp;
    Py_ssize_t n, n_args;
    PyObject **items, **pp;
    PyObject *v;

    if (PyTuple_CheckExact(args)) {
        tmp = args;
        Py_INCREF(args);
    } else {
        tmp = PySequence_Tuple(args);
        if (tmp == NULL) {
            //printf("args error\n");
            return NULL;
        }
    }

    n_args = PyTuple_GET_SIZE(tmp);

    n_slots = datatuple_numslots(type);
    n_items = n_args - n_slots;
    if (n_items < 0) {
//         printf("\nnslots=%i nitems=%i nargs=%i\n", n_slots, n_items, n_args);
        PyErr_SetString(PyExc_TypeError,
                        "number of the arguments should be greater or equal than the number of slots");
        Py_DECREF(tmp);
        return NULL;            
    }

    op = type->tp_alloc(type, n_items);

    pp = ((PyTupleObject*)tmp)->ob_item;
    if (n_slots) {
        n = n_slots;
        items = datatuple_slots(op);
        while (n-- > 0) {
            v = *(pp++);
            Py_INCREF(v);
            *(items++) = v;
        }
    }

    if (n_items) {
        n = n_items;
        items = datatuple_items(type, op);
        while (n-- > 0) {
            v = *(pp++);
            Py_INCREF(v);
            *(items++) = v;
        }
    }

    Py_DECREF(tmp);
    
    if (kwds) {
        if (type->tp_dictoffset) {
            PyObject **dictptr = dataobject_dictptr(type, op);
            PyObject *dict;
            if (*dictptr)
                dict = *dictptr;
            else {
                dict = PyDict_New();
                *dictptr = dict;
            }

            if (PyDict_Update(dict, kwds) == -1) {
                PyErr_SetString(PyExc_TypeError, "__dict__ update is failed");
                return NULL;            
            }
        } else {
            PyErr_SetString(PyExc_TypeError, "invalid kwargs");
            return NULL;            
        }        
    }
    

    return op;
}

static int
datatuple_clear(PyObject *op)
{
    PyTypeObject *type = Py_TYPE(op);
    Py_ssize_t n_slots, n_items;
    PyObject **items;
    
    n_slots = datatuple_numslots(type);

    items = datatuple_slots(op);
    if (n_slots) {
        while (n_slots-- > 0) {
            PyObject *v;

            v = *items;
            Py_DECREF(v);
            *items = NULL;
            items++;
        }
    }

    items = datatuple_items(type, op);
    n_items = Py_SIZE(op);
    if (n_items) {
        while (n_items-- > 0) {
            PyObject *v;

            v = *items;
            Py_DECREF(v);
            *items = NULL;
            items++;
        }
    }

    if (type->tp_dictoffset) {
        PyObject **dictptr = dataobject_dictptr(type, op);
        if (dictptr && *dictptr)
            Py_CLEAR(*dictptr);
    }

    if (type->tp_weaklistoffset)
        PyObject_ClearWeakRefs(op);

    return 0;
}

static void
datatuple_dealloc(PyObject *op)
{
    PyTypeObject *tp = Py_TYPE(op); 

    if (PyType_IS_GC(tp)) {
        PyObject_GC_UnTrack(op);
    } else {
        datatuple_clear(op);        
    }

    tp->tp_free((PyObject *)op);
}

static int
datatuple_traverse(PyObject *op, visitproc visit, void *arg)
{
    Py_ssize_t n_slots, n_items;
    PyObject **items;
    PyTypeObject *type = Py_TYPE(op);

    n_slots = datatuple_numslots(type);
    n_items = Py_SIZE(op);

    if (n_slots) {
        items = datatuple_slots(op);
        while (n_slots--) {
            PyObject *v;

            v = *(items++);
            Py_VISIT(v);
        }
    }

    if (n_items) {
        items = datatuple_items(type, op);
        while (n_items--) {
            PyObject *v;

            v = *(items++);
            Py_VISIT(v);
        }
    }

    if (type->tp_dictoffset) {
        PyObject **dictptr = dataobject_dictptr(type, op);
        if (dictptr && *dictptr)
            Py_VISIT(*dictptr);
    }

    return 0;
}

static PyObject *
datatuple_item(PyObject *op, Py_ssize_t i)
{
    PyTypeObject *type = Py_TYPE(op);
    PyObject **items;
    PyObject *v;

    Py_ssize_t n_slots = datatuple_numslots(type);
    Py_ssize_t n_items = datatuple_numitems(op);
    Py_ssize_t n = n_slots + n_items;

//     if (i < 0)
//         i += n;
    if (i < 0 || i >= n) {
        PyErr_SetString(PyExc_IndexError, "index out of range");
        return NULL;
    }

    if (i < n_slots) {
        items = datatuple_slots(op);
    } else {
        items = datatuple_items(type, op);
        i -= n_slots;
    }

    v = items[i];
    Py_INCREF(v);
    return v;
}

static int
datatuple_ass_item(PyObject *op, Py_ssize_t i, PyObject *val)
{
    Py_ssize_t n = Py_SIZE(op);
    PyObject **items;
    PyTypeObject *type = Py_TYPE(op);
    PyObject* old_val;

    Py_ssize_t n_slots = datatuple_numslots(type);
    Py_ssize_t n_items = datatuple_numitems(op);

    n = n_slots + n_items;

//     if (i < 0)
//         i += n;
    if (i < 0 || i >= n) {
        PyErr_SetString(PyExc_IndexError, "index out of range");
        return -1;
    }

    if (i < n_slots) {
        items = datatuple_slots(op);
    } else {
        items = datatuple_items(type, op);
        i -= n_slots;
    }

    items += i;

    old_val = *items;
    if (old_val)
        Py_DECREF(old_val);
    Py_INCREF(val);
    *items = val;
    return 0;
}

static PyObject*
datatuple_subscript(PyObject* op, PyObject* item)
{
    PyTypeObject *type = Py_TYPE(op);
    Py_ssize_t i, n;
    PyObject **items;
    PyObject *v;
    
    Py_ssize_t n_slots = datatuple_numslots(type);
    Py_ssize_t n_items = datatuple_numitems(op);

    n = n_slots + n_items;
    
    i = (Py_ssize_t)PyNumber_AsSsize_t(item, PyExc_IndexError);
    if (i < 0) {
        if (i == -1 && PyErr_Occurred())
            return NULL;            
        i += n;
    }
        
    if (i < 0 || i >= n) {
        PyErr_SetString(PyExc_IndexError, "index out of range");
        return NULL;
    }
    //printf("i=%i n=%i\n", i, n);
    
    if (i < n_slots) {
        items = datatuple_slots(op);
    } else {
        items = datatuple_items(type, op);
        i -= n_slots;
    }

    v = items[i];
    Py_INCREF(v);
    return v;
}

static int
datatuple_ass_subscript(PyObject* op, PyObject* item, PyObject *val)
{
    PyTypeObject *type = Py_TYPE(op);
    Py_ssize_t i, n;
    PyObject **items;
    
    Py_ssize_t n_slots = datatuple_numslots(type);
    Py_ssize_t n_items = datatuple_numitems(op);

    n = n_slots + n_items;
    
    i = (Py_ssize_t)PyNumber_AsSsize_t(item, PyExc_IndexError);
    if (i < 0) {
        if (i == -1 && PyErr_Occurred())
            return -1;            
        i += n;
    }
        
    if (i < 0 || i >= n) {
        PyErr_SetString(PyExc_IndexError, "index out of range");
        return -1;
    }
    //printf("i=%i n=%i\n", i, n);
    
    if (i < n_slots) {
        items = datatuple_slots(op);
    } else {
        items = datatuple_items(type, op);
        i -= n_slots;
    }

    Py_INCREF(val);
    items[i] = val;
    return 0;
}

// PyDoc_STRVAR(datatuple_len_doc,
// "T.__len__() -- len of T");

static Py_ssize_t
datatuple_len(PyObject *op)
{
    PyTypeObject *type = Py_TYPE(op);
    Py_ssize_t n;

    n = datatuple_numslots(type);
    if (type->tp_itemsize)
        n += Py_SIZE(op);

    return n;
}


PySequenceMethods datatuple_as_sequence = {
    (lenfunc)datatuple_len,                          /* sq_length */
    0,                                              /* sq_concat */
    0,                                              /* sq_repeat */
    (ssizeargfunc)datatuple_item,                    /* sq_item */
    0,                                              /* sq_slice */
    (ssizeobjargproc)datatuple_ass_item,             /* sq_ass_item */
    0,                                              /* sq_ass_slice */
    0,                                              /* sq_contains */
};

PyMappingMethods datatuple_as_mapping = {
    (lenfunc)datatuple_len,                          /* mp_len */
    (binaryfunc)datatuple_subscript,                 /* mp_subscr */
    (objobjargproc)datatuple_ass_subscript,          /* mp_ass_subscr */
};

static PyMethodDef datatuple_methods[] = {
    {"__copy__", (PyCFunction)dataobject_copy, METH_NOARGS, dataobject_copy_doc},
//     {"__len__", (PyCFunction)datatuple_len, METH_NOARGS, datatuple_len_doc},
    {"__sizeof__",      (PyCFunction)dataobject_sizeof, METH_NOARGS, dataobject_sizeof_doc},
    {"__reduce__",      (PyCFunction)dataobject_reduce, METH_NOARGS, dataobject_reduce_doc},
    {"__getstate__",      (PyCFunction)dataobject_getstate, METH_NOARGS, dataobject_getstate_doc},
    {"__getnewargs__",      (PyCFunction)dataobject_getnewargs, METH_NOARGS, dataobject_getnewargs_doc},
    {"__setstate__",      (PyCFunction)dataobject_setstate, METH_O, dataobject_setstate_doc},
    {NULL}
};

static PyTypeObject PyDataTuple_Type = {
    PyVarObject_HEAD_INIT(DEFERRED_ADDRESS(&PyType_Type), 0)
    "recordclass.dataobject.datatuple",        /* tp_name */
    sizeof(PyVarObject),                   /* tp_basicsize */
    sizeof(PyObject*),                    /* tp_itemsize */
    /* methods */
    (destructor)datatuple_dealloc,           /* tp_dealloc */
    0,                                      /* tp_print */
    0,                                      /* tp_getattr */
    0,                                      /* tp_setattr */
    0,                                      /* tp_reserved */
    dataobject_repr,                                      /* tp_repr */
    0,                                      /* tp_as_number */
    &datatuple_as_sequence,                  /* tp_as_sequence */
    &datatuple_as_mapping,                   /* tp_as_mapping */
    dataobject_hash,                          /* tp_hash */
    0,                                      /* tp_call */
    0,                                      /* tp_str */
    PyObject_GenericGetAttr,                /* tp_getattro */
    PyObject_GenericSetAttr,                /* tp_setattro */
    0,                                      /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
                                            /* tp_flags */
    dataobject_doc,                           /* tp_doc */
    0,                      /* tp_traverse */
    0,                         /* tp_clear */
    dataobject_richcompare,                   /* tp_richcompare */
    0,                                      /* tp_weaklistoffset*/
    0,                                      /* tp_iter */
    0,                                      /* tp_iternext */
    datatuple_methods,                       /* tp_methods */
    0,                                      /* tp_members */
    0,                                      /* tp_getset */
    &PyDataObject_Type,                                      /* tp_base */
    0,                                      /* tp_memoryslots */
    0,                                      /* tp_descr_get */
    0,                                      /* tp_descr_set */
    0,                                      /* tp_memoryslotsoffset */
    0,                                      /* tp_init */
    datatuple_alloc,                         /* tp_alloc */
    datatuple_new,                           /* tp_new */
    dataobject_free,                          /* tp_free */
    0                                       /* tp_is_gc */
};

//////////////////////////////////////////////////

static PyObject*
do_getitem(PyObject *op, Py_ssize_t i) {
    PyTypeObject *type = Py_TYPE(op);
    
    if (type->tp_itemsize)
        return datatuple_item(op, i);
    else
        return dataobject_item(op, i);
}

static Py_ssize_t
do_getlen(PyObject *op) {
    PyTypeObject *type = Py_TYPE(op);
    
    if (type->tp_itemsize)
        return datatuple_len(op);
    else
        return dataobject_len(op);

}


//////////////////////////////////////////////////

struct itemgetset_object {
    PyObject_HEAD
    Py_ssize_t offset;
    short readonly;
//     short checked;
};

PyDoc_STRVAR(itemgetset_setname_doc,
"__set_name__\n\n\
");

static PyObject*
itemgetset_setname(PyObject* op, PyObject *args) {
    PyObject* tp;
//     PyObject* *name;
    

    if (Py_SIZE(args) != 2) {
        PyErr_SetString(PyExc_TypeError, "number of arguments != 2");        
        return NULL;
    }

    tp = PyTuple_GET_ITEM(args, 0);
//     name = PyTuple_GET_ITEM(args, 1);

    if (!PyType_IsSubtype(Py_TYPE(tp), &PyDataObject_Type) || 
        !PyType_IsSubtype(Py_TYPE(tp), &PyDataTuple_Type)) {

            PyErr_SetString(PyExc_TypeError, 
                    "this itemsetter can be applied only to subclasses of dataobject or datatuple");
        return NULL;            
    }
    
    printf("*OK*\n");

    Py_RETURN_NONE;    

}

static PyMethodDef itemgetset_methods[] = {
  {"__set_name__", itemgetset_setname, METH_VARARGS, itemgetset_setname_doc},
  {0, 0, 0, 0}
};

static PyObject* itemgetset_new(PyTypeObject *t, PyObject *args, PyObject *k) {    
    struct itemgetset_object *ob;
    PyObject *item;
    Py_ssize_t len, offset;
    int readonly;

    ob = (struct itemgetset_object*)PyBaseObject_Type.tp_new(t, PyTuple_New(0), 0);    
    if (ob == NULL)
        return NULL;

    len = Py_SIZE(args);
    if (len == 0 || len > 2) {
        PyErr_SetString(PyExc_TypeError, "number of args is 1 or 2");
        return NULL;        
    }

    item = PyTuple_GET_ITEM(args, 0);
    if (len == 2)
        readonly = PyObject_IsTrue(PyTuple_GET_ITEM(args, 1));
    else
        readonly = 0;

    offset = PyNumber_AsSsize_t(item, PyExc_IndexError);
    if (offset == -1 && PyErr_Occurred()) {
        Py_DECREF(ob);
        return NULL;
    }

    ob->readonly = readonly;
    ob->offset = offset;
//     ob->checked = 0;
    return (PyObject*)ob;
}

static void itemgetset_dealloc(PyObject *o) {
    PyObject_Del(o);
}

#define dataobject_item_by_offset(op, offset) (*((PyObject**)((char*)op + offset)))
#define dataobject_ass_item_by_offset(op, offset, val) (*((PyObject**)((char*)op + offset))=val)

#define self_igs ((struct itemgetset_object *)self)

static PyObject* itemgetset_get(PyObject *self, PyObject *obj, PyObject *type) {
    //Py_ssize_t offset;
    PyObject *v;

    if (obj == NULL || obj == Py_None) {
        Py_INCREF(self);
        return self;
    }

//     if (!self_igs->checked) {
//             self_igs->checked = 1;
// //         if ((Py_TYPE(obj) == &PyDataObject_Type) || PyType_IsSubtype(Py_TYPE(obj), &PyDataObject_Type))
// //             self_igs->checked = 1;
// //         else {
// //             PyErr_SetString(PyExc_TypeError, "this itemgetter can be applied only to subclasses of dataobject");
// //             return NULL;            
// //         }
//     }

    v = dataobject_item_by_offset(obj, self_igs->offset);
    Py_INCREF(v);
    return v;
}

static int itemgetset_set(PyObject *self, PyObject *obj, PyObject *value) {
    PyObject *v;

    if (value == NULL) {
        PyErr_SetString(PyExc_NotImplementedError, "__delete__");
        return -1;
    }

    if (obj == NULL || obj == Py_None)
        return 0;

//     if (!self_igs->checked) {
//         self_igs->checked = 1;
// //         if ((Py_TYPE(obj) == &PyDataObject_Type) || PyType_IsSubtype(Py_TYPE(obj), &PyDataObject_Type))
// //             self_igs->checked = 1;
// //         else {
// //             PyErr_SetString(PyExc_TypeError, "this itemsetter can be applied only to subclasses of dataobject");
// //             return -1;            
// //         }
//     }

    if (self_igs->readonly) {
        PyErr_SetString(PyExc_TypeError, "item is readonly");
        return -1;
    }

    v = dataobject_item_by_offset(obj, self_igs->offset);
    Py_DECREF(v);
    
    dataobject_ass_item_by_offset(obj, self_igs->offset, value);
    
    Py_INCREF(value);
    return 0;
}

static PyObject*
itemgetset_offset(PyObject *self)
{
    return PyLong_FromSsize_t(((struct itemgetset_object*)self)->offset);
}

static PyObject*
itemgetset_readonly(PyObject *self)
{
    return PyBool_FromLong((long)(((struct itemgetset_object*)self)->offset));
}

static PyGetSetDef itemgetset_getsets[] = {
    {"offset", (getter)itemgetset_offset, NULL, NULL},
    {"readonly", (getter)itemgetset_readonly, NULL, NULL},
    //{"__text_signature__", (getter)type_get_text_signature, NULL, NULL},
    {0}
};

static PyObject* dataobject_iter(PyObject *seq);

static PyTypeObject PyDataObjectItemGetSet_Type = {
    PyVarObject_HEAD_INIT(DEFERRED_ADDRESS(&PyType_Type), 0)
    "recordclass.dataobject.itemgetset", /*tp_name*/
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
    dataobject_iter, /*tp_iter*/
    0, /*tp_iternext*/
    itemgetset_methods, /*tp_methods*/
    0, /*tp_members*/
    itemgetset_getsets, /*tp_getset*/
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

//////////////////////////////////////////////////

/*********************** MemorySlots Iterator **************************/

typedef struct {
    PyObject_HEAD
    Py_ssize_t it_index, it_len;
    PyObject *it_seq; /* Set to NULL when iterator is exhausted */
} dataobjectiterobject;

static void
dataobjectiter_dealloc(dataobjectiterobject *it)
{
    Py_CLEAR(it->it_seq);
    PyObject_Del(it);
}

// static int
// dataobjectiter_traverse(dataobjectiterobject *it, visitproc visit, void *arg)
// {
//     Py_VISIT(it->it_seq);
//     return 0;
// }

// static int
// dataobjectiter_clear(dataobjectiterobject *it)
// {
//     Py_CLEAR(it->it_seq);
//     return 0;
// }

static PyObject *
dataobjectiter_next(dataobjectiterobject *it)
{
    PyObject *item;
    
    if (it->it_index < it->it_len) {
        item = dataobject_item(it->it_seq, it->it_index);
        it->it_index++;
        return item;
    }

    Py_DECREF(it->it_seq);
    it->it_seq = NULL;
    return NULL;
}

static PyObject *
dataobjectiter_len(dataobjectiterobject *it)
{
    Py_ssize_t len = 0;
    if (it->it_seq)
        len = it->it_len - it->it_index;
    return PyLong_FromSsize_t(len);
}

PyDoc_STRVAR(length_hint_doc, "Private method returning an estimate of len(list(it)).");

static PyObject *
dataobjectiter_reduce(dataobjectiterobject *it)
{
    if (it->it_seq)
        return Py_BuildValue("N(O)n", _PyObject_GetBuiltin("iter"),
                             it->it_seq, it->it_index);
    else
        return Py_BuildValue("N(())", _PyObject_GetBuiltin("iter"));
}

PyDoc_STRVAR(dataobjectiter_reduce_doc, "D.__reduce__()");


static PyObject *
dataobjectiter_setstate(dataobjectiterobject *it, PyObject *state)
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
        else if (index > it->it_len)
            index = it->it_len; /* exhausted iterator */
        it->it_index = index;
    }
    Py_RETURN_NONE;
}

PyDoc_STRVAR(setstate_doc, "Set state information for unpickling.");


static PyMethodDef dataobjectiter_methods[] = {
    {"__length_hint__", (PyCFunction)dataobjectiter_len, METH_NOARGS, length_hint_doc},
    {"__reduce__",      (PyCFunction)dataobjectiter_reduce, METH_NOARGS, dataobjectiter_reduce_doc},
    {"__setstate__",    (PyCFunction)dataobjectiter_setstate, METH_O, setstate_doc},
    {NULL,              NULL}           /* sentinel */
};

PyTypeObject PyDataObjectIter_Type = {
    PyVarObject_HEAD_INIT(DEFERRED_ADDRESS(&PyType_Type), 0)
    "recordclass.dataobject.dataobject_iterator",                           /* tp_name */
    sizeof(dataobjectiterobject),                    /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)dataobjectiter_dealloc,              /* tp_dealloc */
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
    Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE,                         /* tp_flags */
    0,                                          /* tp_doc */
    0,     /* tp_traverse */
    0,             /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    PyObject_SelfIter,                          /* tp_iter */
    (iternextfunc)dataobjectiter_next,         /* tp_iternext */
    dataobjectiter_methods,                    /* tp_methods */
    0,
};

static PyObject *
dataobject_iter(PyObject *seq)
{
    dataobjectiterobject *it;

    it = PyObject_New(dataobjectiterobject, &PyDataObjectIter_Type);
    if (it == NULL)
        return NULL;
    it->it_index = 0;
    it->it_seq = seq;
    it->it_len = dataobject_len(seq);
    Py_INCREF(seq);
    return (PyObject *)it;
}

//////////////////////////////////////////////////

PyDoc_STRVAR(sequence_protocol_doc,
"Setup sequence_protocol");

static PyObject*
sequence_protocol(PyObject *module, PyObject *args) {
    PyTypeObject *tp;
    PyTypeObject *tp_base;
    int state, readonly;

    if (Py_SIZE(args) != 3) {
        PyErr_SetString(PyExc_TypeError, "number of arguments != 3");
        return NULL;
    }

    tp = (PyTypeObject*)PyTuple_GET_ITEM(args, 0);
    state = PyObject_IsTrue(PyTuple_GET_ITEM(args, 1));
    readonly = PyObject_IsTrue(PyTuple_GET_ITEM(args, 2));
    
    tp_base = tp->tp_base;

    if (state) {
        tp->tp_as_sequence->sq_item = tp_base->tp_as_sequence->sq_item;
        if (readonly)
           tp->tp_as_sequence->sq_ass_item = NULL;
        else
           tp->tp_as_sequence->sq_ass_item = tp_base->tp_as_sequence->sq_ass_item;

        tp->tp_as_mapping->mp_subscript = tp_base->tp_as_mapping->mp_subscript;
        if (readonly)
           tp->tp_as_mapping->mp_ass_subscript = NULL;
        else
           tp->tp_as_mapping->mp_ass_subscript = tp_base->tp_as_mapping->mp_ass_subscript;
    } else {
        tp->tp_as_sequence->sq_item = NULL;
        tp->tp_as_sequence->sq_ass_item = NULL;
        tp->tp_as_mapping->mp_subscript = NULL;
        tp->tp_as_mapping->mp_ass_subscript = NULL;
    }
    
    Py_RETURN_NONE;
}


PyDoc_STRVAR(set_hash_doc,
"Setup hash support");

static PyObject*
set_hash(PyObject *module, PyObject *args) {
    PyTypeObject *tp;
    int state;
    
    
    if (Py_SIZE(args) != 2) {
        PyErr_SetString(PyExc_TypeError, "number of arguments != 2");
        return NULL;
    }

    tp = (PyTypeObject*)PyTuple_GET_ITEM(args, 0);
    state = PyObject_IsTrue(PyTuple_GET_ITEM(args, 1));
    

    if (state)
        tp->tp_hash = tp->tp_base->tp_hash;
    else
        tp->tp_hash = NULL;

    Py_RETURN_NONE;
}

static PyObject*
_fix_type(PyObject *module, PyObject *args) {
    PyObject *tp;
    PyTypeObject *meta;
    PyObject *val;
    
    tp = PyTuple_GET_ITEM(args, 0);
    meta = (PyTypeObject*)PyTuple_GET_ITEM(args, 1);
    
    
    if (tp->ob_type != meta) {
        val = (PyObject*)tp->ob_type;
        Py_XDECREF(val);
        tp->ob_type = meta;
        Py_INCREF(meta);
        PyType_Modified((PyTypeObject*)tp);
    }     
    Py_RETURN_NONE;
}

PyDoc_STRVAR(set_dictoffset_doc,
"Set tp_dictoffset");


static PyObject*
set_dictoffset(PyObject *module, PyObject *args) {
    PyTypeObject *tp;
    PyObject *ob;
    int state;

    if (Py_SIZE(args) == 0) {
        PyErr_SetString(PyExc_TypeError, "missing arguments");        
        return NULL;
    }

    tp = (PyTypeObject*)PyTuple_GET_ITEM(args, 0);
//     if (!PyObject_IsSubclass((PyObject*)tp, (PyObject*)&PyType_Type)) {
//         PyErr_SetString(PyExc_TypeError, "argument is not a subtype of the type");        
//         return NULL;
//     }
    
    if (Py_SIZE(args) == 1)
        state = 0;
    else {
        ob = PyTuple_GET_ITEM(args, 1);
        state = PyObject_IsTrue(ob);
    }
    
    
    tp->tp_dictoffset = 0;
    if (state) {
        tp->tp_dictoffset = tp->tp_basicsize;
        tp->tp_basicsize += sizeof(PyObject*);
    }
        
    Py_RETURN_NONE;
}
 
PyDoc_STRVAR(set_weaklistoffset_doc,
"Set tp_weaklistoffset");


static PyObject*
set_weaklistoffset(PyObject *module, PyObject *args) {
    PyTypeObject *tp;
    PyObject *ob;
    int state;

    if (Py_SIZE(args) == 0) {
        PyErr_SetString(PyExc_TypeError, "missing arguments");        
        return NULL;
    }

    tp = (PyTypeObject*)PyTuple_GET_ITEM(args, 0);
//     if (!PyObject_IsSubclass((PyObject*)tp, (PyObject*)&PyType_Type)) {
//         PyErr_SetString(PyExc_TypeError, "argument is not a subtype of the type");        
//         return NULL;
//     }
    
    if (Py_SIZE(args) == 1)
        state = 0;
    else {
        ob = PyTuple_GET_ITEM(args, 1);
        state = PyObject_IsTrue(ob);
    }

    tp->tp_weaklistoffset = 0;
    if (state) {
        tp->tp_weaklistoffset = tp->tp_basicsize;
        tp->tp_basicsize += sizeof(PyObject*);
    }

    Py_RETURN_NONE;
}


PyDoc_STRVAR(number_of_dataslots_doc,
"Number of dataslots");

static PyObject*
number_of_dataslots(PyObject *module, PyObject *args) {
    PyTypeObject* tp;
    Py_ssize_t ret;
    
    if (Py_SIZE(args) != 1) {
        PyErr_SetString(PyExc_TypeError, "number of arguments != 1");        
        return NULL;
    }

    tp = (PyTypeObject*)PyTuple_GET_ITEM(args, 0);
//     if (!PyType_IsSubtype(tp, &PyType_Type)) {
//         PyErr_SetString(PyExc_TypeError, "argument is not a subtype of the type");        
//         return NULL;
//     }

    ret = tp->tp_basicsize;

    if (tp->tp_itemsize)
        ret -= sizeof(PyVarObject);
    else
        ret -= sizeof(PyObject);

    if (tp->tp_dictoffset)
        ret -= sizeof(PyObject*);
    if (tp->tp_weaklistoffset)
        ret -= sizeof(PyObject*);

    ret /= sizeof(PyObject*);
    return PyLong_FromSsize_t(ret);
}

PyDoc_STRVAR(dataslot_offset_doc,
"Offset of dataslot value");

static PyObject*
dataslot_offset(PyObject *module, PyObject *args) {
    PyTypeObject *tp;
    PyObject *index;
    Py_ssize_t i, n_fields;
    Py_ssize_t offset;
    
    if (Py_SIZE(args) != 2) {
        PyErr_SetString(PyExc_TypeError, "number of arguments != 2");        
        return NULL;
    }
    

    tp = (PyTypeObject*)PyTuple_GET_ITEM(args, 0);
    index = PyTuple_GET_ITEM(args, 1);


    i = PyNumber_AsSsize_t(index, PyExc_IndexError);
    if (i < 0) {
        if (i == -1 && PyErr_Occurred())
            return NULL;        
        PyErr_SetString(PyExc_IndexError, "index < 0");
        return NULL;
    }

    if (tp->tp_itemsize) {
        n_fields = (tp->tp_basicsize - sizeof(PyVarObject)) / sizeof(PyObject*);
        offset = sizeof(PyVarObject);
    } else {
        n_fields = (tp->tp_basicsize - sizeof(PyObject)) / sizeof(PyObject*);
        offset = sizeof(PyObject);
    }

    if (tp->tp_dictoffset)
        n_fields -= 1;
    if (tp->tp_weaklistoffset)
        n_fields -= 1;

    if (i >= n_fields) {
        PyErr_SetString(PyExc_IndexError, "index out of range");
        return NULL;
    }

    offset += i * sizeof(PyObject*);

    return PyLong_FromSsize_t(offset);

}


PyDoc_STRVAR(dataobject_type_init_doc,
"Initialize dataobject subclass");

static PyObject* 
dataobject_type_init(PyObject *module, PyObject *args) {
    Py_ssize_t n;
    PyObject *cls;
    PyObject *n_fields;
    PyObject *varsize;
    PyObject *has_fields;

    PyTypeObject *tp;
    PyTypeObject *tp_base;

    if (Py_SIZE(args) != 4) {
        PyErr_SetString(PyExc_TypeError, "number of arguments != 4");        
        return NULL;
    }

    cls = PyTuple_GET_ITEM(args, 0);
    n_fields = PyTuple_GET_ITEM(args, 1);
    varsize = PyTuple_GET_ITEM(args, 2);
    has_fields = PyTuple_GET_ITEM(args, 3);
    
    tp = (PyTypeObject*)cls;
    tp_base = tp->tp_base;

    if (!PyObject_IsSubclass((PyObject*)tp_base, (PyObject*)&PyDataObject_Type) &&
        !PyObject_IsSubclass((PyObject*)tp_base, (PyObject*)&PyDataTuple_Type)) {
            PyErr_SetString(PyExc_TypeError, "common base class should be dataobject or subclass");        
            return NULL;
    }

    tp->tp_itemsize = tp_base->tp_itemsize;
    if (PyObject_IsTrue(varsize) || tp_base->tp_itemsize)
            tp->tp_basicsize = sizeof(PyVarObject);
    else
            tp->tp_basicsize = sizeof(PyObject);

    n = PyNumber_AsSsize_t(n_fields, NULL);
    if (n > 0)
        tp->tp_basicsize += n * sizeof(PyObject*);
    

    if (PyObject_Not(has_fields)) {
            tp->tp_alloc = tp_base->tp_alloc;
            tp->tp_new = tp_base->tp_new;
    }

    tp->tp_dealloc = tp_base->tp_dealloc;
    tp->tp_free = tp_base->tp_free;    
    tp->tp_init = NULL;

    tp->tp_flags |= Py_TPFLAGS_HEAPTYPE;
    
    if (tp->tp_flags & Py_TPFLAGS_HAVE_GC)
        tp->tp_flags &= ~Py_TPFLAGS_HAVE_GC;

    tp->tp_traverse = NULL;
    tp->tp_clear = NULL;
    tp->tp_is_gc = NULL;

    Py_RETURN_NONE;
}


PyDoc_STRVAR(enable_gc_doc,
"Enable GC for specified (var)dataobject class");

static PyObject *
dataobject_enable_gc(PyObject *module, PyObject *args)
{
    PyObject *cls;
    PyTypeObject *type;

    if (Py_SIZE(args) > 1) {
        PyErr_SetString(PyExc_TypeError, "too many arguments");        
        return NULL;
    }

    cls = PyTuple_GET_ITEM(args, 0);
    
    if (!PyObject_IsInstance(cls, (PyObject*)&PyType_Type)) {
        PyErr_SetString(PyExc_TypeError, "Argument have to be an instance of type");        
        return NULL;
    }

    type = (PyTypeObject*)cls;
    type->tp_flags |= Py_TPFLAGS_HAVE_GC;
    if (type->tp_itemsize) {
        type->tp_traverse = datatuple_traverse;
        type->tp_clear = datatuple_clear;
    } else {
        type->tp_traverse = dataobject_traverse;
        type->tp_clear = dataobject_clear;
    }
    
    Py_INCREF(cls);
    return cls;
}

//////////////////////////////////////////////////

PyDoc_STRVAR(dataobjectmodule_doc,
"dataobject module provide `dataobject` class.");

static PyMethodDef dataobjectmodule_methods[] = {
    {"enable_gc", dataobject_enable_gc, METH_VARARGS, enable_gc_doc},
    {"dataobject_type_init", dataobject_type_init, METH_VARARGS, dataobject_type_init_doc},
    {"dataslot_offset", dataslot_offset, METH_VARARGS, dataslot_offset_doc},
    {"set_dict", set_dictoffset, METH_VARARGS, set_dictoffset_doc},
    {"set_hash", set_hash, METH_VARARGS, set_hash_doc},
    {"set_weakref", set_weaklistoffset, METH_VARARGS, set_weaklistoffset_doc},
    {"number_of_dataslots", number_of_dataslots, METH_VARARGS, number_of_dataslots_doc},
    {"sequence_protocol", sequence_protocol, METH_VARARGS, sequence_protocol_doc},
    {"_fix_type", _fix_type, METH_VARARGS, ""},    
    {0, 0, 0, 0}
};


#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef dataobjectmodule = {
  #if PY_VERSION_HEX < 0x03020000
    { PyObject_HEAD_INIT(NULL) NULL, 0, NULL },
  #else
    PyModuleDef_HEAD_INIT,
  #endif
    "recordclass.dataobject",
    dataobjectmodule_doc,
    -1,
    dataobjectmodule_methods,
    NULL,
    NULL,
    NULL,
    NULL
};
#endif

#if PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC
PyInit_dataobject(void)
{
    PyObject *m;
    
    m = PyState_FindModule(&dataobjectmodule);
    if (m) {
        Py_INCREF(m);
        return m;
    }    

    m = PyModule_Create(&dataobjectmodule);
    if (m == NULL)
        return NULL;
    
    if (PyType_Ready(&PyDataObject_Type) < 0)
        Py_FatalError("Can't initialize dataobject type");
    if (PyType_Ready(&PyDataTuple_Type) < 0)
        Py_FatalError("Can't initialize datatuple type");

    if (PyType_Ready(&PyDataObjectItemGetSet_Type) < 0)
        Py_FatalError("Can't initialize itemgetset_dataobject type");

    if (PyType_Ready(&PyDataObjectIter_Type) < 0)
        Py_FatalError("Can't initialize dataobjectiter type");
    
    Py_INCREF(&PyDataObject_Type);
    PyModule_AddObject(m, "dataobject", (PyObject *)&PyDataObject_Type);    
    Py_INCREF(&PyDataTuple_Type);
    PyModule_AddObject(m, "datatuple", (PyObject *)&PyDataTuple_Type);    

    Py_INCREF(&PyDataObjectItemGetSet_Type);
    PyModule_AddObject(m, "itemgetset", (PyObject *)&PyDataObjectItemGetSet_Type);    

    Py_INCREF(&PyDataObjectIter_Type);
    PyModule_AddObject(m, "dataobject_iterator", (PyObject *)&PyDataObjectIter_Type);
    
//     undefined = PyBaseObject_Type.tp_alloc(&PyBaseObject_Type, 0);
//     PyModule_AddObject(m, "undef", undefined);
//     Py_INCREF(undefined);
    

    return m;
}
#else
PyMODINIT_FUNC
initdataobject(void)
{
    PyObject *m;

    m = Py_InitModule3("recordclass.dataobject", dataobjectmodule_methods, dataobjectmodule_doc);
    if (m == NULL)
        return;
    Py_XINCREF(m);

    if (PyType_Ready(&PyDataObject_Type) < 0)
         Py_FatalError("Can't initialize dataobject type");
    if (PyType_Ready(&PyDataTuple_Type) < 0)
        Py_FatalError("Can't initialize datatuple type");

    if (PyType_Ready(&PyDataObjectItemGetSet_Type) < 0)
        Py_FatalError("Can't initialize itemgetset_dataobject type");

    if (PyType_Ready(&PyDataObjectIter_Type) < 0)
        Py_FatalError("Can't initialize dataobjectiter type");
    
    Py_INCREF(&PyDataObject_Type);
    PyModule_AddObject(m, "dataobject", (PyObject *)&PyDataObject_Type);
    Py_INCREF(&PyDataTuple_Type);
    PyModule_AddObject(m, "datatuple", (PyObject *)&PyDataTuple_Type);    

    Py_INCREF(&PyDataObjectItemGetSet_Type);
    PyModule_AddObject(m, "itemgetset", (PyObject *)&PyDataObjectItemGetSet_Type);    

    Py_INCREF(&PyDataObjectIter_Type);
    PyModule_AddObject(m, "dataobject_iterator", (PyObject *)&PyDataObjectIter_Type);
    
//     undefined = PyBaseObject_Type.tp_alloc(&PyBaseObject_Type, 0);
//     PyModule_AddObject(m, "undef", undefined);
//     Py_INCREF(undefined);

    return;
}
#endif
