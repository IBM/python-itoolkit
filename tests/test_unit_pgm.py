import xml.etree.ElementTree as ET

from itoolkit import iPgm


def test_pgm():
    pgm = 'MYPGM'
    key = 'lljqezl'

    element = ET.fromstring(iPgm(key, pgm).xml_in())
    assert(element.tag == 'pgm')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert('name' in element.attrib)
    assert(element.attrib['name'] == pgm)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == 'fast')


def test_pgm_error_on():
    pgm = 'MYPGM'
    key = 'rtoiu1nqew'
    error = 'on'

    element = ET.fromstring(iPgm(key, pgm, {'error': error}).xml_in())
    assert(element.tag == 'pgm')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert('name' in element.attrib)
    assert(element.attrib['name'] == pgm)

    assert('lib' not in element.attrib)
    assert('func' not in element.attrib)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)


def test_pgm_error_off():
    pgm = 'MYPGM'
    key = 'lkjwernm'
    error = 'off'

    element = ET.fromstring(iPgm(key, pgm, {'error': error}).xml_in())
    assert(element.tag == 'pgm')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert('name' in element.attrib)
    assert(element.attrib['name'] == pgm)

    assert('lib' not in element.attrib)
    assert('func' not in element.attrib)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)


def test_pgm_lib():
    pgm = 'MYPGM'
    key = 'rtoiu1nqew'
    lib = 'MYLIB'

    element = ET.fromstring(iPgm(key, pgm, {'lib': lib}).xml_in())
    assert(element.tag == 'pgm')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert('name' in element.attrib)
    assert(element.attrib['name'] == pgm)

    assert('lib' in element.attrib)
    assert(element.attrib['lib'] == lib)

    assert('func' not in element.attrib)
