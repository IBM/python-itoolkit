import xml.etree.ElementTree as ET

from itoolkit import iSqlParm

DATA = "Hello, world!"


def test_sql_query():
    key = 'dmmyeozq'

    element = ET.fromstring(iSqlParm(key, DATA).xml_in())
    assert(element.tag == 'parm')
    assert(element.text == DATA)

    assert(len(element.attrib) == 2)

    assert('io' in element.attrib)
    assert(element.attrib['io'] == 'both')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_prepare_io_in():
    key = 'zbutinao'
    io = 'in'

    element = ET.fromstring(iSqlParm(key, DATA, {'io': io}).xml_in())
    assert(element.tag == 'parm')
    assert(element.text == DATA)

    assert(len(element.attrib) == 2)

    assert('io' in element.attrib)
    assert(element.attrib['io'] == io)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_prepare_io_out():
    key = 'vqsjrnkv'
    io = 'out'

    element = ET.fromstring(iSqlParm(key, DATA, {'io': io}).xml_in())
    assert(element.tag == 'parm')
    assert(element.text == DATA)

    assert(len(element.attrib) == 2)

    assert('io' in element.attrib)
    assert(element.attrib['io'] == io)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_execute_conn_set():
    key = 'jrntesje'
    conn = 'conn-label'

    element = ET.fromstring(iSqlParm(key, DATA, {'conn': conn}).xml_in())
    assert(element.tag == 'parm')
    assert(element.text == DATA)

    assert(len(element.attrib) == 3)

    assert('conn' in element.attrib)
    assert(element.attrib['conn'] == conn)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_execute_stmt_set():
    key = 'miecefin'
    stmt = 'stmt-label'

    element = ET.fromstring(iSqlParm(key, DATA, {'stmt': stmt}).xml_in())
    assert(element.tag == 'parm')
    assert(element.text == DATA)

    assert(len(element.attrib) == 3)

    assert('stmt' in element.attrib)
    assert(element.attrib['stmt'] == stmt)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_execute_options_set():
    key = 'qeficmfx'
    options = 'options-label'

    element = ET.fromstring(iSqlParm(key, DATA, {'options': options}).xml_in())
    assert(element.tag == 'parm')
    assert(element.text == DATA)

    assert(len(element.attrib) == 3)

    assert('options' in element.attrib)
    assert(element.attrib['options'] == options)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)
