import os

from ctypes import c_int, c_uint, c_int16, c_ulonglong, c_void_p, c_char_p, \
                   CDLL, DEFAULT_MODE, POINTER, Structure, addressof, sizeof, \
                   create_string_buffer

RTLD_MEMBER = 0x00040000


class ILEPointer(Structure):
    "An ILE pointer type"
    _pack_ = 16
    _fields_ = [
        ("hi", c_ulonglong),
        ("lo", c_ulonglong)
    ]


try:
    _LIBC = CDLL("/QOpenSys/usr/lib/libc.a(shr_64.o)",
                 DEFAULT_MODE | RTLD_MEMBER)

    _SETSPP = _LIBC._SETSPP
    _SETSPP.argtypes = [POINTER(ILEPointer), c_void_p]

    _ILELOADX = _LIBC._ILELOADX
    _ILELOADX.argtypes = [c_char_p, c_uint]
    _ILELOADX.restype = c_ulonglong

    _ILESYMX = _LIBC._ILESYMX
    _ILESYMX.argtypes = [POINTER(ILEPointer), c_ulonglong, c_char_p]

    _ILECALLX = _LIBC._ILECALLX
    _ILECALLX.argtypes = [
        POINTER(ILEPointer),
        c_void_p,
        POINTER(c_int16),
        c_int16,
        c_int
    ]
except OSError:
    # Either we couldn't load libc or we couldn't find the necessary syscalls
    # exported from libc. Either way, this platform is unsupported so we raise
    # an import error to prevent it from being used.
    raise ImportError

ILELOAD_LIBOBJ = 0x00000001
ILESYM_PROCEDURE = 1

RESULT_VOID = 0
RESULT_INT8 = -1
RESULT_UINT8 = -2
RESULT_INT16 = -3
RESULT_UINT16 = -4
RESULT_INT32 = -5
RESULT_UINT32 = -6
RESULT_INT64 = -7
RESULT_UINT64 = -8
RESULT_FLOAT64 = -10
RESULT_FLOAT128 = -18

ARG_END = 0
ARG_MEMPTR = -11


class MemPointer(ILEPointer):
    "An ILE pointer type to be used with ARG_MEMPTR"
    _pack_ = 16

    def __init__(self, addr=0):
        super(MemPointer, self).__int__()
        self.hi = 0
        self.lo = addr

    @property
    def addr(self):
        return self.lo

    @addr.setter
    def addr(self, addr):
        self.lo = addr


class ILEArglistBase(Structure):
    "ILECALL argument list base member"
    _pack_ = 16
    _fields_ = [
        ('descriptor', ILEPointer),
        ('result', ILEPointer),
    ]


class RunASCIIArglist(Structure):
    "Argument list definition for the RUNASCII procedure"
    _pack_ = 16
    _fields_ = [
        ('base', ILEArglistBase),
        ('ipc', MemPointer),
        ('ipc_len', MemPointer),
        ('ctl', MemPointer),
        ('ctl_len', MemPointer),
        ('xmlin', MemPointer),
        ('xmlin_len', MemPointer),
        ('xmlout', MemPointer),
        ('xmlout_len', MemPointer),
        ('pase_ccsid', MemPointer),
        ('ile_ccsid', MemPointer),
    ]


RunASCIISignature = c_int16 * 11

_SIGNATURE = RunASCIISignature(
        ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR,
        ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR, ARG_MEMPTR,
        ARG_END
)


class _XMLSERVICE:
    def __init__(self, library):
        self.library = library

        path = "{library}/XMLSTOREDP".format(library=library)
        actgrp = _ILELOADX(path.encode(), ILELOAD_LIBOBJ)
        if actgrp == 0xffffffffffffffff:
            raise OSError("{path} not found".format(path=path))

        self._RUNASCII = ILEPointer()
        if _ILESYMX(self._RUNASCII, actgrp, b"RUNASCII") != ILESYM_PROCEDURE:
            raise OSError("RUNASCII procedure not found in {path}"
                          .format(path=path))

    def __call__(self, xmlin, ipc, ctl):
        ipc = c_char_p(ipc.encode())
        ipc_len = c_int(len(ipc.value))

        ctl = c_char_p(ctl.encode())
        ctl_len = c_int(len(ctl.value))

        xmlin = c_char_p(xmlin.encode())
        xmlin_len = c_int(len(xmlin.value))

        xmlout = create_string_buffer(0x1000000)  # 16MiB
        xmlout_len = c_int(sizeof(xmlout))

        pase_ccsid = c_int(1208)
        ile_ccsid = c_int(0)

        # RUNASCII doesn't just take ILE pointers, it takes ILE pointers to ILE
        # pointers, so we first copy the PASE pointer in to a space pointer for
        # each pointer parameter... *except* for the integer parameters, which
        # are just pointers to integers for some reason...
        ipc_spp = ILEPointer()
        ctl_spp = ILEPointer()
        xmlin_spp = ILEPointer()
        xmlout_spp = ILEPointer()

        _SETSPP(ipc_spp, ipc)
        _SETSPP(ctl_spp, ctl)
        _SETSPP(xmlin_spp, xmlin)
        _SETSPP(xmlout_spp, xmlout)

        arglist = RunASCIIArglist()
        arglist.ipc.addr = addressof(ipc_spp)
        arglist.ipc_len.addr = addressof(ipc_len)
        arglist.ctl.addr = addressof(ctl_spp)
        arglist.ctl_len.addr = addressof(ctl_len)
        arglist.xmlin.addr = addressof(xmlin_spp)
        arglist.xmlin_len.addr = addressof(xmlin_len)
        arglist.xmlout.addr = addressof(xmlout_spp)
        arglist.xmlout_len.addr = addressof(xmlout_len)
        arglist.pase_ccsid.addr = addressof(pase_ccsid)
        arglist.ile_ccsid.addr = addressof(ile_ccsid)

        if _ILECALLX(self._RUNASCII, addressof(arglist), _SIGNATURE,
                     RESULT_INT32, 0):
            raise RuntimeError("Failed to call XMLSERVICE with _ILECALL")

        if arglist.base.result.lo & 0xffffffff:
            raise RuntimeError("XMLSERVICE returned an error")

        return xmlout.value


def xmlservice(xmlin, ipc, ctl):
    # If we haven't yet initialized XMLSERVICE, do that now
    if not hasattr(xmlservice, 'cached_obj'):

        libraries = [os.getenv("XMLSERVICE"), "QXMLSERV", "XMLSERVICE"]

        found = False
        for library in libraries:
            if not library:
                continue

            try:
                xmlservice.cached_obj = _XMLSERVICE(library)
                found = True
            except OSError:
                continue

        if not found:
            # TODO: Message string
            raise OSError("Couldn't load RUNASCII function from XMLSERVICE")

    return xmlservice.cached_obj(xmlin, ipc, ctl)
