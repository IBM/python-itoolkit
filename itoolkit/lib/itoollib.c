/*
+----------------------------------------------------------------------+
|  Licensed Materials - Property of IBM                                |
|                                                                      |
| (C) Copyright IBM Corporation 2015.                                  |
+----------------------------------------------------------------------+
| Authors: Tony 'Ranger' Cairns                                        |
|                                                                      | 
+----------------------------------------------------------------------+
*/

#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <iconv.h>
#include <as400_protos.h>

/* defining string methods */
#if  PY_MAJOR_VERSION < 3
#define StringOBJ_FromASCII(str)	PyString_FromString(str)
#define StringOBJ_FromUTF8(str)	    PyString_FromString(str)
#define PyBytes_AsString		    PyString_AsString
#define PyBytes_FromStringAndSize	PyString_FromStringAndSize
#define StringObj_Format		    PyString_Format
#define StringObj_Size			    PyString_Size
#else
#define PyInt_Check			        PyLong_Check
#define PyInt_FromLong          	PyLong_FromLong
#define PyInt_AsLong            	PyLong_AsLong
#define PyInt_AS_LONG			    PyLong_AsLong
#define StringOBJ_FromASCII(str)	PyUnicode_DecodeASCII(str, strlen(str), NULL)
#define StringOBJ_FromUTF8(str)	    PyUnicode_DecodeUTF8(str, strlen(str), NULL)
#define PyString_Check			    PyUnicode_Check
#define StringObj_Format		    PyUnicode_Format
#define StringObj_Size			    PyUnicode_GET_SIZE
#endif

#define NUM2LONG(data) PyInt_AsLong(data)
#define STR2CSTR(data) PyString_AsString(data)
#define NIL_P(ptr) (ptr == NULL)
#define ALLOC_N(type, n) PyMem_New(type, n)
#define ALLOC(type) PyMem_New(type, 1)


/* True global resources - no need for thread safety here */
#define __I_ALIGN(x, a) (((uint32)x+a-1) & ~(a-1))
#define __I_QUAD(x) (__I_ALIGN(x, 16))
#define	__I_DEFAULT_MAX 15000016
#define __I_DEFAULT_PGM_NAME "XMLSTOREDP"
#define __I_DEFAULT_LIB_ENV "XMLSERVICE"
#define __I_DEFAULT_LIB_TEST "XMLSERVICE"
#define __I_DEFAULT_LIB_IBM "QXMLSERV"
static int _i_xmlservice_active;
static char * _i_default_pgm_name = __I_DEFAULT_PGM_NAME;
static char * _i_default_lib_env = __I_DEFAULT_LIB_ENV;
static char * _i_default_lib_test = __I_DEFAULT_LIB_TEST;
static char * _i_default_lib_ibm = __I_DEFAULT_LIB_IBM;
static char  _ibm_itool_pgm_buf[40];
static char * _ibm_itool_pgm_name = (char *)&_ibm_itool_pgm_buf;

#define __I_DEFAULT_FUNC_RUNASCII "RUNASCII"
static char * _i_xmlservice_buf_runascii[256];
static union _ILEpointer* _i_xmlservice_ptr_runascii;
static char * _i_default_func_runascii = __I_DEFAULT_FUNC_RUNASCII;
static char * _ibm_itool_func_runascii;
static char * _ibm_itool_xmlout_runascii;
static int _ibm_itool_xmlout_runascii_len;

static void _ibm_itool_init_globals()
{
	int i, rc = -1, actmark = -1;
    char * find_env_lib = getenv(_i_default_lib_env);
    char * find_lib_xmlservice[] = {find_env_lib, _i_default_lib_ibm, _i_default_lib_test};
	_i_xmlservice_active = 0;
	_i_xmlservice_ptr_runascii = (union _ILEpointer *) __I_QUAD(&_i_xmlservice_buf_runascii);
    _ibm_itool_xmlout_runascii = (char *)malloc(__I_DEFAULT_MAX);
    _ibm_itool_xmlout_runascii_len = __I_DEFAULT_MAX-16;
	/* find service program (if not active) */
	if (!_i_xmlservice_active) {
        for (i=0; i < 3 & rc < 0; i++) {
            if (find_lib_xmlservice[i]) {
                memset(&_ibm_itool_pgm_buf,0,sizeof(_ibm_itool_pgm_buf));
                sprintf(_ibm_itool_pgm_name,"%s/%s",find_lib_xmlservice[i],_i_default_pgm_name);
                actmark = _ILELOAD(_ibm_itool_pgm_name, ILELOAD_LIBOBJ);
                if (actmark > -1) {
                    _ibm_itool_func_runascii = _i_default_func_runascii;
	                rc = _ILESYM(_i_xmlservice_ptr_runascii, actmark, _ibm_itool_func_runascii);
                }
            }
        }
        if (rc > -1) {
	        _i_xmlservice_active = 1;
        }
    }
}

static char * _ibm_itool_call_xmlservice(char *ipc, int ipc_len, char *ctl, int ctl_len, char *xmlin, int xmlin_len, long pase_ccsid, long ebcdic_ccsid)
{
	int i, rc = 0;
	const arg_type_t signature[] = 
  	{ ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, 
  	  ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, 
  	  ARG_END }; 
  	typedef struct ArgList 
  	{
		ILEarglist_base base; 
    	ILEpointer ppIPCSP; 
    	ILEpointer szIPCSP;
    	ILEpointer ppCtlSP; 
    	ILEpointer szCtlSP;
    	ILEpointer ppIClob;
    	ILEpointer szIClob;
    	ILEpointer ppOClob;
    	ILEpointer szOClob;
    	ILEpointer ccsidPASE;
    	ILEpointer ccsidILE;
   	    ILEpointer pIPCSP;
   	    ILEpointer pCtlSP;
   	    ILEpointer pIClob;
   	    ILEpointer pOClob;
  	} ArgList_t;
	char argumentsBuf[sizeof(ArgList_t) + 15];
	ArgList_t *arguments; 

    if (!_i_xmlservice_active) {
        return NULL;
    }

	/* make call IBM i xmlservice */
	memset(&argumentsBuf,0,sizeof(argumentsBuf));
	arguments = (ArgList_t *) __I_QUAD( argumentsBuf );

	_SETSPP(&arguments->pIPCSP, ipc);
	arguments->ppIPCSP.s.addr = (uint32) &arguments->pIPCSP;
	arguments->szIPCSP.s.addr = (uint32) &ipc_len;

	_SETSPP(&arguments->pCtlSP, ctl);
	arguments->ppCtlSP.s.addr = (uint32) &arguments->pCtlSP;
	arguments->szCtlSP.s.addr = (uint32) &ctl_len;

	_SETSPP(&arguments->pIClob, xmlin);
	arguments->ppIClob.s.addr = (uint32) &arguments->pIClob;
	arguments->szIClob.s.addr = (uint32) &xmlin_len;
	
	_SETSPP(&arguments->pOClob, _ibm_itool_xmlout_runascii);
	arguments->ppOClob.s.addr = (uint32) &arguments->pOClob;
	arguments->szOClob.s.addr = (uint32) &_ibm_itool_xmlout_runascii_len;

	if (!pase_ccsid) pase_ccsid = 1208; // Qp2paseCCSID();
	arguments->ccsidPASE.s.addr = (uint32) &pase_ccsid;
	if (!ebcdic_ccsid) ebcdic_ccsid = Qp2jobCCSID();
	arguments->ccsidILE.s.addr = (uint32) &ebcdic_ccsid;
	
	rc = _ILECALL(_i_xmlservice_ptr_runascii, &arguments->base, signature, RESULT_INT32 );
	if (rc != ILECALL_NOERROR) {
		return NULL;
	}
	rc = arguments->base.result.s_int32.r_int32;
	if (!rc) {
		return NULL;
	}

	/* return xml output */
	return _ibm_itool_xmlout_runascii;
}


static PyObject *itoolib_xmlservice(PyObject *self, PyObject *args)
{
    PyObject *py_ipc = NULL;
    PyObject *py_ctl = NULL;
    PyObject *py_xmlin = NULL;
    PyObject *py_xmlout = NULL;
	PyObject *retVal = NULL;
    int len = 0;
	char * data = NULL;
    char *ipc=NULL;
    int ipc_len=0;
    char *ctl=NULL;
    int ctl_len=0;
    char *xmlin=NULL;
    int xmlin_len=0;
    long pase_ccsid=0;
    long ebcdic_ccsid=0;

	if (!PyArg_ParseTuple(args, "sss|ll", &xmlin, &ctl, &ipc, &ebcdic_ccsid, &pase_ccsid))
		return NULL;

    ipc_len=strlen(ipc);
    ctl_len=strlen(ctl);
    xmlin_len=strlen(xmlin);
    pase_ccsid=0;
    ebcdic_ccsid=0;

    /* clear output buffer from last call */
    len = strlen(_ibm_itool_xmlout_runascii);
    if (len>0) {
        memset(_ibm_itool_xmlout_runascii,0,len);
    }

    data = _ibm_itool_call_xmlservice(ipc, ipc_len, ctl, ctl_len, xmlin, xmlin_len, pase_ccsid, ebcdic_ccsid);
	if (!pase_ccsid || pase_ccsid == 1208) {
      return StringOBJ_FromUTF8(data); /* ADC - 1.3 */
    }
    return StringOBJ_FromASCII(data);
}

/* Listing of itoolib module functions: */
static PyMethodDef methods[] = {
	{"xmlservice", (PyCFunction)itoolib_xmlservice, METH_VARARGS, "Returns XML from XMLSERVICE"},
	{NULL, NULL, 0, NULL}
};

/* Module initialization function */
#if PY_MAJOR_VERSION < 3
void inititoollib(void) {
    static char itoolib_doc[] = "IBM XMLSERVICE Driver for Python.\n";
    _ibm_itool_init_globals();
	Py_InitModule3("itoollib", methods, itoolib_doc);
}
#else
PyMODINIT_FUNC PyInit_itoollib(void) {
    static struct PyModuleDef moduledef = {
		PyModuleDef_HEAD_INIT,
		"itoollib",
		"IBM XMLSERVICE Driver for Python.",
		-1,
		methods,
	};
    _ibm_itool_init_globals();
    return PyModule_Create(&moduledef);
}
#endif


