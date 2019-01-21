import xml.etree.ElementTree as ET

from itoolkit import iCmd


def test_rexx():
    cmd = 'RTVJOBA USRLIBL(?) SYSLIBL(?)'
    key = 'rtvjoba'

    element = ET.fromstring(iCmd(key, cmd).xml_in())
    assert(element.tag == 'cmd')

    assert('exec' in element.attrib)
    assert(element.attrib['exec'] == 'rexx')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == 'fast')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == cmd)


def test_rexx_error_on():
    cmd = 'RTVJOBA USRLIBL(?) SYSLIBL(?)'
    key = 'rtoiu1nqew'
    error = 'on'

    element = ET.fromstring(iCmd(key, cmd, {'error': error}).xml_in())
    assert(element.tag == 'cmd')

    assert('exec' in element.attrib)
    assert(element.attrib['exec'] == 'rexx')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == cmd)


def test_rexx_error_off():
    cmd = 'RTVJOBA USRLIBL(?) SYSLIBL(?)'
    key = 'lkjwernm'
    error = 'off'

    element = ET.fromstring(iCmd(key, cmd, {'error': error}).xml_in())
    assert(element.tag == 'cmd')

    assert('exec' in element.attrib)
    assert(element.attrib['exec'] == 'rexx')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == cmd)


def test_exec():
    cmd = 'DSPSYSSTS'
    key = 'kjwlenrn'

    element = ET.fromstring(iCmd(key, cmd).xml_in())
    assert(element.tag == 'cmd')

    assert('exec' in element.attrib)
    assert(element.attrib['exec'] == 'cmd')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == 'fast')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == cmd)


def test_exec_on():
    cmd = 'DSPSYSSTS'
    key = 'pndsfnwer'
    error = 'on'

    element = ET.fromstring(iCmd(key, cmd, {'error': error}).xml_in())
    assert(element.tag == 'cmd')

    assert('exec' in element.attrib)
    assert(element.attrib['exec'] == 'cmd')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == cmd)


def test_exec_off():
    cmd = 'DSPSYSSTS'
    key = 'oiuewtrlkjgs'
    error = 'off'

    element = ET.fromstring(iCmd(key, cmd, {'error': error}).xml_in())
    assert(element.tag == 'cmd')

    assert('exec' in element.attrib)
    assert(element.attrib['exec'] == 'cmd')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == cmd)
