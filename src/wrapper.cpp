#define PY_SSIZE_T_CLEAN
#include <python3.7m/Python.h>
#include <stdint.h>
#include "host.h"

/*
Here module name :  tool
static Pyobject *MyFunction(Pyobject *self, Pyobject *args);
static Pyobject *MyFunctionwithkeywords(Pyobject *self, Pyobject *args, Pyobject *kw);
static Pyobject *MyFunctionwithNoArgs(Pyobject *self);
struct PyMethodDef {
    char         *ml_name;       // function name when presents in python script
    PyCFunction  ml_meth;        // address of function- recommend name: 
                                 // modulename_functionname, here is tool_spird....
    int          ml_flags;       // tell python interpreter arguments : 
                                 // METH_VARARGS; METH_KEYWORDS; METH_NOARGS 
    char         *ml_doc;        // Optional description, nothing is NULL
};
*/
/*
 PyArg_ParseTuple:  extract the arguments from the one PyObject pointer passed into your C function
 syntax :
        int PyArg_ParseTuple(PyObject *tuple, char *format,....)   : return 0- error
 code :      c(char)             : a python string of length 1 becomes a C char
             d(double)           : a python float becomes a C double
             f(float)            : a python float becomes a C float
             i(int)              : a python int becomes a C int
             l(long)             : a python int becomes a C long
             L(long long)        : a python int becomes a C long long
             O(PyObject*)        : gets non-NULL borrowed reference to Python argument
             s(char*)            : Python string without embedded nulls to C char*
             s#(char*+int)       : Any python string to C address and length
             t#(char*+int)       : Read-only single-segment buffer to C address and length
             u(Py_UNICODE*)      : Python Unicode without embedded nulls to C
             u#(Py_UNICODE*+int) : any python unicode C address and length
             w#(char*+int)       : read/write single-segment buffer to C address and length
             z(char*)            : like s, also accepts none(set C char* to NULL)
             z#(char*+int)       : like s#, also accepts none(set C char* to NULL)
             (...) as per...     : A python sequence is treated as one argument per item
             |                   : the following arguments are optional
             :                   : format end, followed by function name for error messages
             ;                   : format end, followed by entire error message text   

*/

/*
   Py_BuildValue : like above, Instead of passing in the addresses of the values you are building,
                   you pass in the actual values.
   Syntax:
         PyObject* Py_BuildValue(char *format)
   code: 
         c(char)                 : A C char becomes a Python string of length 1
         d(double)               : A C double becomes a Python float
         f(float)                : A C float becomes a Python float
         i(int)                  : A C int becomes a Python int
         l(long)                 : A C long becomes a Python int
         N(PyObject*)            : Passes a Python object and steals a reference
         O(PyObject*)            : Passes a Python object and INCREFs it as normal
         O&(convert+void*)       : Arbitrary conversion
         s(char*)                : C 0-terminated char* to Python string, or NULL to None
         s#(char*+int)           : C char* and length to Python string, or NULL to none
         u(Py_UNICODE*)          : C-wide, null-terminated string to Python Unicode, or NULL to none
         u#(Py_UNICODE*+int)     : C-wide string and length to Python Unicode, or NULL to none
         w#(char*+int)           : Read/Write single-segment buffer to C address and length
         z(char*)                : Like s, also accepts None(set C char* to NULL)
         z#(char*+int)           : Like s#, also accepts none(set C char* to NULL)
         (...) as per...         : Builds Python tuple from C values
         [...] as per...         : Builds Python list from C values
         {...} as per...         : Builds Python dictionary from C values, alternating keys and values
         For example, Py_BuildValue("{issi}",23,"zig","zag",42) return a dictionary like Python's
         {23:'zig','zag':42}
    eg:
         Py_BuildValue("")                        None
         Py_BuildValue("i", 123)                  123
         Py_BuildValue("iii", 123, 456, 789)      (123, 456, 789)
         Py_BuildValue("s", "hello")              'hello'
         Py_BuildValue("y", "hello")              b'hello'
         Py_BuildValue("ss", "hello", "world")    ('hello', 'world')
         Py_BuildValue("s#", "hello", 4)          'hell'
         Py_BuildValue("y#", "hello", 4)          b'hell'
         Py_BuildValue("()")                      ()
         Py_BuildValue("(i)", 123)                (123,)
         Py_BuildValue("(ii)", 123, 456)          (123, 456)
         Py_BuildValue("(i,i)", 123, 456)         (123, 456)
         Py_BuildValue("[i,i]", 123, 456)         [123, 456]
         Py_BuildValue("{s:i,s:i}",
                       "abc", 123, "def", 456)    {'abc': 123, 'def': 456}
         Py_BuildValue("((ii)(ii)) (ii)",
                       1, 2, 3, 4, 5, 6)          (((1, 2), (3, 4)), (5, 6))
*/
/*
   Exceptions: raise Pythonn exceptions from your C extension module, use 3 functions
   PyErr_SetString(PyObject *type, const char *message)
   PyErr_Format   (PyObject *type, const char *format)
   PyErr_SetObject(PyObject *type, PyObject *value)
   eg:    if(strlen(str) < 10){
       PyErr_SetString(PyExc_ValueError, "String length must be greater than 10");
       return NULL;
   }
*/
static PyObject *tool_spird(PyObject *self, PyObject *args)
{
    uint64_t spi_address;
    uint32_t rd_data;
    // int bytecount = 0xFF;
    
    if (!PyArg_ParseTuple(args,"l", &spi_address))
        return NULL;
    // call C function here to get data back properly
    host tp;
    tp.spi_rd(spi_address, &rd_data);
    return Py_BuildValue("i",rd_data);

    // Py_RETURN_NONE;
}
// static PyObject *tool_spiwr(PyObject *self, PyObject *args)
// {
//     Py_RETURN_NONE;
// }

// static PyObject *tool_hbmrd(PyObject *self, PyObject *args)
// {
//     Py_RETURN_NONE;
// }
// static PyObject *tool_hbmwr(PyObject *self, PyObject *args)
// {
//     Py_RETURN_NONE;
// }

// static PyObject *tool_dfdrd(PyObject *self, PyObject *args)
// {
//     Py_RETURN_NONE;
// }
// static PyObject *tool_dfdwr(PyObject *self, PyObject *args)
// {
//     Py_RETURN_NONE;
// }

static PyMethodDef tool_funcs[] = {
    {"spird", (PyCFunction)tool_spird, METH_VARARGS, NULL},
    // {"spiwr", (PyCFunction)tool_spiwr, METH_VARARGS, NULL},
    // {"hbmrd", (PyCFunction)tool_hbmrd, METH_VARARGS, NULL},
    // {"hbmwr", (PyCFunction)tool_hbmwr, METH_VARARGS, NULL},
    // {"dfdrd", (PyCFunction)tool_dfdrd, METH_VARARGS, NULL},
    // {"dfdwr", (PyCFunction)tool_dfdwr, METH_VARARGS, NULL},
    {NULL,NULL,0,NULL}
};

static struct PyModuleDef toolmodule = {
    PyModuleDef_HEAD_INIT,
    "tool",                   /*name of module */
    NULL  ,                   /*doc string     */
    -1,                       /* size of per-interpreter state or -1 */
    tool_funcs                /* method table */
};

PyMODINIT_FUNC PyInit_tool(void)
{
    return PyModule_Create(&toolmodule);
}