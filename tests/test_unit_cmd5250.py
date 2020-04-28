import xml.etree.ElementTree as ET

from itoolkit import iCmd5250


def test_5250():
    cmd = 'WRKACTJOB'
    key = 'lljqezl'

    element = ET.fromstring(iCmd5250(key, cmd).xml_in())
    assert(element.tag == 'sh')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == 'fast')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == "/QOpenSys/usr/bin/system WRKACTJOB")


def test_5250_error_on():
    cmd = 'WRKACTJOB'
    key = 'rtoiu1nqew'
    error = 'on'

    element = ET.fromstring(iCmd5250(key, cmd, {'error': error}).xml_in())
    assert(element.tag == 'sh')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == "/QOpenSys/usr/bin/system WRKACTJOB")


def test_5250_error_off():
    cmd = 'WRKACTJOB'
    key = 'lkjwernm'
    error = 'off'

    element = ET.fromstring(iCmd5250(key, cmd, {'error': error}).xml_in())
    assert(element.tag == 'sh')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == "/QOpenSys/usr/bin/system WRKACTJOB")


def test_5250_row_on():
    cmd = 'WRKACTJOB'
    key = 'rtoiu1nqew'
    row = 'on'

    element = ET.fromstring(iCmd5250(key, cmd, {'row': row}).xml_in())
    assert(element.tag == 'sh')

    assert('row' in element.attrib)
    assert(element.attrib['row'] == row)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == "/QOpenSys/usr/bin/system WRKACTJOB")


def test_5250_row_off():
    cmd = 'WRKACTJOB'
    key = 'lkjwernm'
    row = 'off'

    element = ET.fromstring(iCmd5250(key, cmd, {'row': row}).xml_in())
    assert(element.tag == 'sh')

    assert('row' in element.attrib)
    assert(element.attrib['row'] == row)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == "/QOpenSys/usr/bin/system WRKACTJOB")

def test_5250_space():
    cmd = 'WRKACTJOB SBS(*QINTER)'
    key = 'lknwqekrn'

    element = ET.fromstring(iCmd5250(key, cmd).xml_in())
    assert(element.tag == 'sh')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == 'fast')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == "/QOpenSys/usr/bin/system 'WRKACTJOB SBS(*QINTER)'")


def test_5250_inner_string():
    cmd = "wrklnk '/test/file'"
    key = 'znxvlkja'

    element = ET.fromstring(iCmd5250(key, cmd).xml_in())
    assert(element.tag == 'sh')

    assert('error' in element.attrib)
    assert(element.attrib['error'] == 'fast')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == """/QOpenSys/usr/bin/system 'wrklnk '"'"'/test/file'"'"''""")
