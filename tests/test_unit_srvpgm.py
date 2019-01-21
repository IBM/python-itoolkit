import xml.etree.ElementTree as ET

from itoolkit import iSrvPgm


def test_pgm():
    key = 'lljqezl'
    pgm = 'MYPGM'
    func = 'printf'

    element = ET.fromstring(iSrvPgm(key, pgm, func).xml_in())
    assert(element.tag == 'pgm')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert('name' in element.attrib)
    assert(element.attrib['name'] == pgm)

    assert('func' in element.attrib)
    assert(element.attrib['func'] == func)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == 'fast')


def test_pgm_error_on():
    key = 'rtoiu1nqew'
    pgm = 'MYPGM'
    func = 'printf'
    error = 'on'

    element = ET.fromstring(iSrvPgm(key, pgm, func, {'error': error}).xml_in())
    assert(element.tag == 'pgm')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert('name' in element.attrib)
    assert(element.attrib['name'] == pgm)

    assert('func' in element.attrib)
    assert(element.attrib['func'] == func)

    assert('lib' not in element.attrib)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)


def test_pgm_error_off():
    key = 'lkjwernm'
    pgm = 'MYPGM'
    func = 'printf'
    error = 'off'

    element = ET.fromstring(iSrvPgm(key, pgm, func, {'error': error}).xml_in())
    assert(element.tag == 'pgm')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert('name' in element.attrib)
    assert(element.attrib['name'] == pgm)

    assert('func' in element.attrib)
    assert(element.attrib['func'] == func)

    assert('lib' not in element.attrib)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)


def test_pgm_lib():
    key = 'rtoiu1nqew'
    pgm = 'MYPGM'
    func = 'printf'
    lib = 'MYLIB'

    element = ET.fromstring(iSrvPgm(key, pgm, func, {'lib': lib}).xml_in())
    assert(element.tag == 'pgm')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert('name' in element.attrib)
    assert(element.attrib['name'] == pgm)

    assert('func' in element.attrib)
    assert(element.attrib['func'] == func)

    assert('lib' in element.attrib)
    assert(element.attrib['lib'] == lib)
