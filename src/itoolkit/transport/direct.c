/*
+----------------------------------------------------------------------+
|  Licensed Materials - Property of IBM                                |
|                                                                      |
| (C) Copyright IBM Corporation 2015, 2018.                            |
+----------------------------------------------------------------------+
| Authors: Tony 'Ranger' Cairns                                        |
|          Kevin Adler                                                 | 
+----------------------------------------------------------------------+
*/

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __PASE__
#include <as400_protos.h>

static int available = 0;
static ILEpointer runascii_fp __attribute__ ((aligned (16)));

static int load_xmlservice(const char* library) {
    char srvpgm[22];
    sprintf(srvpgm, "%s/XMLSTOREDP", library);
    
    unsigned long long actmark = _ILELOADX(srvpgm, ILELOAD_LIBOBJ);
    
    if (actmark == (unsigned long long)-1) return 0;
    
    return _ILESYMX(&runascii_fp, actmark, "RUNASCII") == 1;
}

static int make_available(void) {
    /* find service program (if not active) */
    if (available) {
        return available;
    }
    
    const char* envvar = getenv("XMLSERVICE");
    if(envvar && strlen(envvar) <= 10) {
        available = load_xmlservice(envvar);
        if(available) return available;
    }
    
    available = load_xmlservice("QXMLSERV");
    if(available) return available;
    
    available = load_xmlservice("XMLSERVICE");
    if(available) return available;
    
    return available;
}

static PyObject *itoolib_xmlservice(PyObject *self, PyObject *args)
{
    char *xmlin;
    char *ctl;
    char *ipc;
    Py_ssize_t xmlin_size;
    Py_ssize_t ctl_size;
    Py_ssize_t ipc_size;
    // These used to be passed in, but were later over-written and forced to
    // be these values. Instead of passing in, I'm just forcing them to be
    // this for now
    int ile_ccsid = 0;
    int pase_ccsid = 1208;

    if (!PyArg_ParseTuple(args, "s#s#s#",
        &xmlin, &xmlin_size,
        &ctl, &ctl_size,
        &ipc, &ipc_size)) {
        return NULL;
    }
    
    if(!make_available()) {
        PyErr_SetString(PyExc_RuntimeError,
                        "Couldn't load RUNASCII function from XMLSERVICE");
        return NULL;
    }
    
    int xmlin_len = (int) xmlin_size;
    int ctl_len = (int) ctl_size;
    int ipc_len = (int) ipc_size;
    int xmlout_len = (16 * 1024 * 1024);
    char* xmlout = (char*) PyMem_Malloc(xmlout_len);
    int rc;

    const arg_type_t signature[] = {
        ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR,
        ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR,
        ARG_END
    };
    
    struct {
        ILEarglist_base base;
        ILEpointer ipc;
        ILEpointer ipc_len;
        ILEpointer ctl;
        ILEpointer ctl_len;
        ILEpointer xmlin;
        ILEpointer xmlin_len;
        ILEpointer xmlout;
        ILEpointer xmlout_len;
        ILEpointer pase_ccsid;
        ILEpointer ile_ccsid;
    } arglist __attribute__ ((aligned (16)));
    
    // RUNASCII doesn't just take ILE pointers, it takes
    // ILE pointers to ILE pointers, so we first copy
    // the PASE pointer in to a space pointer for each
    // pointer parameter... *except* for the integer
    // parameters, which are just pointers to integers
    // for some reason...
    ILEpointer ipc_spp __attribute__ ((aligned (16)));
    ILEpointer ctl_spp __attribute__ ((aligned (16)));
    ILEpointer xmlin_spp __attribute__ ((aligned (16)));
    ILEpointer xmlout_spp __attribute__ ((aligned (16)));
    
    _SETSPP(&ipc_spp, ipc);
    _SETSPP(&ctl_spp, ctl);
    _SETSPP(&xmlin_spp, xmlin);
    _SETSPP(&xmlout_spp, xmlout);
    
    arglist.ipc.s.addr        = (address64_t)(intptr_t) &ipc_spp;
    arglist.ipc_len.s.addr    = (address64_t)(intptr_t) &ipc_len;
    arglist.ctl.s.addr        = (address64_t)(intptr_t) &ctl_spp;
    arglist.ctl_len.s.addr    = (address64_t)(intptr_t) &ctl_len;
    arglist.xmlin.s.addr      = (address64_t)(intptr_t) &xmlin_spp;
    arglist.xmlin_len.s.addr  = (address64_t)(intptr_t) &xmlin_len;
    arglist.xmlout.s.addr     = (address64_t)(intptr_t) &xmlout_spp;
    arglist.xmlout_len.s.addr = (address64_t)(intptr_t) &xmlout_len;
    arglist.pase_ccsid.s.addr = (address64_t)(intptr_t) &pase_ccsid;
    arglist.ile_ccsid.s.addr  = (address64_t)(intptr_t) &ile_ccsid;
    
    rc = _ILECALL(&runascii_fp, &arglist.base, signature, RESULT_INT32);
    
    PyObject* ret = NULL;
    if (rc != ILECALL_NOERROR) {
        PyErr_SetString(PyExc_RuntimeError,
                        "Failed to call XMLSERVICE with _ILECALL");
        goto end;
    }
    if (!arglist.base.result.s_int32.r_int32) {
        PyErr_SetString(PyExc_RuntimeError,
                        "XMLSERVICE returned an error");
        goto end;
    }
    
    ret = PyBytes_FromString(xmlout);
    
end:
    PyMem_Free(xmlout);
    
    return ret;
}
#endif

static PyMethodDef methods[] = {
#ifdef __PASE__
    {"_xmlservice", (PyCFunction)itoolib_xmlservice, METH_VARARGS, "Calls XMLSERVICE via _ILECALL"},
#endif
    {NULL, NULL, 0, NULL}
};

#define docstring "Internal _ILECALL wrapper for XMLSERVICE"

#if PY_MAJOR_VERSION < 3
void init_direct(void) {
    Py_InitModule3("_direct", methods, docstring);
}
#else
PyMODINIT_FUNC PyInit__direct(void) {
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "_direct",
        docstring,
        -1,
        methods,
        NULL,
        NULL,
        NULL,
        NULL
    };
    
    return PyModule_Create(&moduledef);
}
#endif
