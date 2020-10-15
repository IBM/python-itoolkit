import xml.etree.ElementTree as ET

from itoolkit import iSqlExecute, iSqlParm


def test_sql_execute():
    key = 'khnusoyh'

    element = ET.fromstring(iSqlExecute(key).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'execute')

    assert(len(element.attrib) == 2)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == 'fast')

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_execute_error_on():
    key = 'zteaevna'
    error = 'on'

    element = ET.fromstring(iSqlExecute(key, {'error': error}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'execute')

    assert(len(element.attrib) == 2)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_execute_error_off():
    key = 'xewyhrda'
    error = 'off'

    element = ET.fromstring(iSqlExecute(key, {'error': error}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'execute')

    assert(len(element.attrib) == 2)

    assert('error' in element.attrib)
    assert(element.attrib['error'] == error)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_execute_conn_set():
    key = 'oshcnxve'
    conn = 'conn-label'

    element = ET.fromstring(iSqlExecute(key, {'conn': conn}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'execute')

    assert(len(element.attrib) == 3)

    assert('conn' in element.attrib)
    assert(element.attrib['conn'] == conn)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_execute_stmt_set():
    key = 'oftjocui'
    stmt = 'stmt-label'

    element = ET.fromstring(iSqlExecute(key, {'stmt': stmt}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'execute')

    assert(len(element.attrib) == 3)

    assert('stmt' in element.attrib)
    assert(element.attrib['stmt'] == stmt)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_execute_options_set():
    key = 'dikeaunc'
    options = 'options-label'

    element = ET.fromstring(iSqlExecute(key, {'options': options}).xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'execute')

    assert(len(element.attrib) == 3)

    assert('options' in element.attrib)
    assert(element.attrib['options'] == options)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)


def test_sql_execute_add_one_parm():
    key = 'gibksybk'
    parm = 'foo'

    action = iSqlExecute(key)
    action.addParm(iSqlParm(parm, parm))

    element = ET.fromstring(action.xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'execute')

    assert(len(element.attrib) == 2)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    children = tuple(iter(element))
    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'parm')
    assert(element.text == parm)


def test_sql_execute_add_two_parms():
    key = 'yuwhcsed'
    parm1 = 'foo'
    parm2 = 'bar'

    action = iSqlExecute(key)
    action.addParm(iSqlParm(parm1, parm1))
    action.addParm(iSqlParm(parm2, parm2))

    element = ET.fromstring(action.xml_in())
    assert(element.tag == 'sql')

    assert(len(element.attrib) == 1)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    assert(element.text == '\n')

    children = tuple(iter(element))

    assert(len(children) == 1)
    element = children[0]

    assert(element.tag == 'execute')

    assert(len(element.attrib) == 2)

    assert('var' in element.attrib)
    assert(element.attrib['var'] == key)

    children = tuple(iter(element))
    assert(len(children) == 2)

    element = children[0]
    assert(element.tag == 'parm')
    assert(element.text == parm1)

    element = children[1]
    assert(element.tag == 'parm')
    assert(element.text == parm2)
