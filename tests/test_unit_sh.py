import xml.etree.ElementTree as ET

from itoolkit import iSh


def test_sh():
    cmd = 'ls -l'
    key = 'lljqezl'

    element = ET.fromstring(iSh(key, cmd).xml_in())
    assert(element.tag == 'sh')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == 'fast')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == cmd)


def test_sh_error_on():
    cmd = 'ls -l'
    key = 'rtoiu1nqew'
    error = 'on'

    element = ET.fromstring(iSh(key, cmd, {'error': error}).xml_in())
    assert(element.tag == 'sh')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == cmd)


def test_sh_error_off():
    cmd = 'ls -l'
    key = 'lkjwernm'
    error = 'off'

    element = ET.fromstring(iSh(key, cmd, {'error': error}).xml_in())
    assert(element.tag == 'sh')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == cmd)


def test_sh_row_on():
    cmd = 'ls -l'
    key = 'rtoiu1nqew'
    row = 'on'

    element = ET.fromstring(iSh(key, cmd, {'row': row}).xml_in())
    assert(element.tag == 'sh')

    assert('row' in element.attrib)
    assert(element.attrib['row'] == row)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == cmd)


def test_sh_row_off():
    cmd = 'ls -l'
    key = 'lkjwernm'
    row = 'off'

    element = ET.fromstring(iSh(key, cmd, {'row': row}).xml_in())
    assert(element.tag == 'sh')

    assert('row' in element.attrib)
    assert(element.attrib['row'] == row)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == cmd)
