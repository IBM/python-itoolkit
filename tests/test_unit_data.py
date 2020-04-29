import xml.etree.ElementTree as ET

from itoolkit import iData


def test_data():
    key = 'lljqezl'
    datatype = '10a'
    value = 'foo'

    element = ET.fromstring(iData(key, datatype, value).xml_in())

    assert(element.tag == 'data')
    assert(element.attrib['var'] == key)
    assert(element.attrib['type'] == datatype)
    assert(element.text == value)


def test_data_non_str():
    key = 'madsn'
    datatype = '10i0'
    value = 0

    element = ET.fromstring(iData(key, datatype, value).xml_in())

    assert(element.tag == 'data')
    assert(element.attrib['var'] == key)
    assert(element.attrib['type'] == datatype)
    assert(element.text == str(value))


def test_data_and_options():
    key = 'oiujgoihs'
    datatype = '10a'
    value = 'bar'
    opts = {
        'dim': 10,
        'varying': 'on',
    }

    element = ET.fromstring(iData(key, datatype, value, opts).xml_in())
    assert(element.tag == 'data')
    assert(element.attrib['var'] == key)
    assert(element.attrib['type'] == datatype)
    for k, v in opts.items():
        assert(element.attrib[k] == str(v))
    assert(element.text == value)


def test_data_default_value():
    key = 'madsn'
    datatype = '10a'

    element = ET.fromstring(iData(key, datatype).xml_in())

    assert(element.tag == 'data')
    assert(element.attrib['var'] == key)
    assert(element.attrib['type'] == datatype)
    assert(element.text is None)
