import pytest
import sys

from itoolkit import iToolKit, TransportClosedException
from itoolkit.transport import HttpTransport

if sys.version_info >= (3, 0):
    if sys.version_info >= (3, 6):
        from urllib.parse import parse_qs
    else:
        from urllib.parse import urlencode
else:
    from urllib import urlencode

XMLIN = "<?xml version='1.0'?>\n<xmlservice></xmlservice>"


def mock_http_urlopen(mocker):
    mock_urlopen = mocker.patch('itoolkit.transport.http.urlopen')
    mock_response = mocker.Mock()
    mock_response.read.side_effect = (XMLIN.encode('utf-8'), )
    mock_urlopen.return_value = mock_response

    return mock_urlopen


def assert_urlopen_params_correct(mock_urlopen, url, uid, pwd, db2='*LOCAL',
                                  ipc='*na', ctl='*here *cdata',
                                  xmlout=str(HttpTransport.OUT_SIZE)):
    # assert_called_once only available in Python 3.6+
    if sys.version_info >= (3, 6):
        mock_urlopen.assert_called_once()

        args, kwargs = mock_urlopen.call_args

        assert len(kwargs) == 0
        assert len(args) == 2

        assert args[0] == url

        data = {key.decode('utf-8'): value[0].decode('utf-8') for (key, value)
                in parse_qs(args[1]).items()}

        exp_data = dict(
            uid=uid,
            pwd=pwd,
            db2=db2,
            ipc=ipc,
            ctl=ctl,
            xmlout=xmlout,
            xmlin=XMLIN + "\n",
        )
        assert data == exp_data
    else:
        mock_urlopen.assert_called_once_with(url, urlencode({
                'db2': db2,
                'uid': uid,
                'pwd': pwd,
                'ipc': ipc,
                'ctl': ctl,
                'xmlin': XMLIN + "\n",
                'xmlout': int(xmlout)
        }).encode("utf-8"))


def test_http_transport_minimal(mocker):
    mock_urlopen = mock_http_urlopen(mocker)

    url = 'http://example.com/cgi-bin/xmlcgi.pgm'
    user = 'dummy'
    password = 'passw0rd'

    transport = HttpTransport(url, user, password)
    tk = iToolKit()
    out = transport.call(tk)

    assert isinstance(out, (bytes, str))

    assert_urlopen_params_correct(
        mock_urlopen,
        url,
        uid=user,
        pwd=password,
    )


def test_http_transport_with_database(mocker):
    mock_urlopen = mock_http_urlopen(mocker)

    url = 'http://example.com/cgi-bin/xmlcgi.pgm'
    user = 'dummy'
    password = 'passw0rd'
    database = 'MYDB'

    transport = HttpTransport(url, user, password, database=database)
    tk = iToolKit()
    out = transport.call(tk)

    assert isinstance(out, (bytes, str))

    assert_urlopen_params_correct(
        mock_urlopen,
        url,
        uid=user,
        pwd=password,
        db2=database
    )


def test_http_transport_call_raises_when_closed(mocker):
    mock_urlopen = mock_http_urlopen(mocker)

    url = 'http://example.com/cgi-bin/xmlcgi.pgm'
    user = 'dummy'
    password = 'passw0rd'
    database = 'MYDB'

    transport = HttpTransport(url, user, password, database=database)
    transport.close()

    with pytest.raises(TransportClosedException):
        tk = iToolKit()
        out = transport.call(tk)
