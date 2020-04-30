import pytest
import sys

from itoolkit import iToolKit
from itoolkit.transport import DirectTransport
import itoolkit.transport.direct

XMLIN = "<?xml version='1.0'?>\n<xmlservice></xmlservice>"


def mock_direct(mocker):
    "Mock transport.direct"
    itoolkit.transport.direct._available = True

    mock_direct = mocker.patch('itoolkit.transport.direct._direct', create=True)

    mock_xmlsevice = mocker.Mock()
    mock_xmlsevice.return_value = XMLIN.encode('utf-8')

    mock_direct._xmlservice = mock_xmlsevice

    return mock_direct


def assert_xmlservice_params_correct(mock_direct, ipc='*na',
                                     ctl='*here *cdata'):
    mock_xmlservice = mock_direct._xmlservice

    xml = XMLIN + "\n"

    # assert_called_once only available in Python 3.6+
    if sys.version_info >= (3, 6):
        mock_xmlservice.assert_called_once()

        args, kwargs = mock_xmlservice.call_args

        assert len(kwargs) == 0
        assert len(args) == 3

        assert args[0] == xml
        assert args[1] == ctl
        assert args[2] == ipc
    else:
        mock_xmlservice.assert_called_once_with(xml, ctl, ipc)


def test_direct_transport_unsupported(mocker):
    "Test that we get an error running on an unsupported platform"
    itoolkit.transport.direct._available = False

    transport = DirectTransport()
    tk = iToolKit()
    with pytest.raises(RuntimeError):
        transport.call(tk)


def test_direct_transport(mocker):
    mock = mock_direct(mocker)

    transport = DirectTransport()
    tk = iToolKit()
    out = transport.call(tk)

    assert_xmlservice_params_correct(mock)
    assert isinstance(out, (bytes, str))
