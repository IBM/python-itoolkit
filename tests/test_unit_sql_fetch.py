import xml.etree.ElementTree as ET

from itoolkit import iSqlFetch


def test_sql_fetch():
    key = 'mulblnxo'

    element = ET.fromstring(iSqlFetch(key).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'fetch')

    assert(len(element.attrib) == 3)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == 'fast')

    assert('block' in element.attrib)
    assert(element.attrib['block'] == 'all')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_fetch_error_on():
    key = 'opaffdjr'
    error = 'on'

    element = ET.fromstring(iSqlFetch(key, {'error': error}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'fetch')

    assert(len(element.attrib) == 3)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_fetch_error_off():
    key = 'ysdifjyx'
    error = 'off'

    element = ET.fromstring(iSqlFetch(key, {'error': error}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'fetch')

    assert(len(element.attrib) == 3)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_fetch_block_set():
    key = 'ojaxupoq'
    block = '10'

    element = ET.fromstring(iSqlFetch(key, {'block': block}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'fetch')

    assert(len(element.attrib) == 3)

    assert('block' in element.attrib)
    assert(element.attrib['block'] == block)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_fetch_desc_on():
    key = 'sefufeoq'
    describe = 'on'

    element = ET.fromstring(iSqlFetch(key, {'desc': describe}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'fetch')

    assert(len(element.attrib) == 4)

    assert('desc' in element.attrib)
    assert(element.attrib['desc'] == describe)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_fetch_desc_off():
    key = 'jtucgypy'
    describe = 'off'

    element = ET.fromstring(iSqlFetch(key, {'desc': describe}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'fetch')

    assert(len(element.attrib) == 4)

    assert('desc' in element.attrib)
    assert(element.attrib['desc'] == describe)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_fetch_stmt_set():
    key = 'slkgfrav'
    stmt = 'stmt-label'

    element = ET.fromstring(iSqlFetch(key, {'stmt': stmt}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'fetch')

    assert(len(element.attrib) == 4)

    assert('stmt' in element.attrib)
    assert(element.attrib['stmt'] == stmt)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_fetch_rec_set():
    key = 'slkgfrav'
    records = '10'

    element = ET.fromstring(iSqlFetch(key, {'rec': records}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'fetch')

    assert(len(element.attrib) == 4)

    assert('rec' in element.attrib)
    assert(element.attrib['rec'] == records)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)
