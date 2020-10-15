import xml.etree.ElementTree as ET

from itoolkit import iSqlFree


def test_sql_free():
    key = 'ifaovjuf'

    element = ET.fromstring(iSqlFree(key).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'free')

    assert(len(element.attrib) == 2)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == 'fast')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_free_error_on():
    key = 'nkcfhgwf'
    error = 'on'

    element = ET.fromstring(iSqlFree(key, {'error': error}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'free')

    assert(len(element.attrib) == 2)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_free_error_off():
    key = 'vzumvoan'
    error = 'off'

    element = ET.fromstring(iSqlFree(key, {'error': error}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'free')

    assert(len(element.attrib) == 2)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_free_conn_set():
    key = 'igqywtcq'
    conn = 'conn-label'

    element = ET.fromstring(iSqlFree(key, {'conn': conn}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'free')

    assert(len(element.attrib) == 3)

    assert('conn' in element.attrib)
    assert(element.attrib['conn'] == conn)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_free_stmt_set():
    key = 'tofzlwxz'
    stmt = 'stmt-label'

    element = ET.fromstring(iSqlFree(key, {'stmt': stmt}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'free')

    assert(len(element.attrib) == 3)

    assert('stmt' in element.attrib)
    assert(element.attrib['stmt'] == stmt)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_free_options_set():
    key = 'poraowkq'
    options = 'options-label'

    element = ET.fromstring(iSqlFree(key, {'options': options}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'free')

    assert(len(element.attrib) == 3)

    assert('options' in element.attrib)
    assert(element.attrib['options'] == options)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)
