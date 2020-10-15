import xml.etree.ElementTree as ET

from itoolkit import iSqlQuery

QUERY = "SELECT * FROM QIWS.QCUSTCDT"


def test_sql_query():
    key = 'dmmyeozq'

    element = ET.fromstring(iSqlQuery(key, QUERY).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'query')
    assert(element.text == QUERY)

    assert(len(element.attrib) == 2)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == 'fast')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_prepare_error_on():
    key = 'zbutinao'
    error = 'on'

    element = ET.fromstring(iSqlQuery(key, QUERY, {'error': error}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'query')
    assert(element.text == QUERY)

    assert(len(element.attrib) == 2)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_prepare_error_off():
    key = 'vqsjrnkv'
    error = 'off'

    element = ET.fromstring(iSqlQuery(key, QUERY, {'error': error}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'query')
    assert(element.text == QUERY)

    assert(len(element.attrib) == 2)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_execute_conn_set():
    key = 'jrntesje'
    conn = 'conn-label'

    element = ET.fromstring(iSqlQuery(key, QUERY, {'conn': conn}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'query')
    assert(element.text == QUERY)

    assert(len(element.attrib) == 3)

    assert('conn' in element.attrib)
    assert(element.attrib['conn'] == conn)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_execute_stmt_set():
    key = 'miecefin'
    stmt = 'stmt-label'

    element = ET.fromstring(iSqlQuery(key, QUERY, {'stmt': stmt}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'query')
    assert(element.text == QUERY)

    assert(len(element.attrib) == 3)

    assert('stmt' in element.attrib)
    assert(element.attrib['stmt'] == stmt)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_execute_options_set():
    key = 'qeficmfx'
    options = 'options-label'

    element = ET.fromstring(iSqlQuery(key, QUERY,
                            {'options': options}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'query')
    assert(element.text == QUERY)

    assert(len(element.attrib) == 3)

    assert('options' in element.attrib)
    assert(element.attrib['options'] == options)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)
