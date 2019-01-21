from itoolkit import iToolKit, iCmd

_xml = """<?xml version="1.0" ?>
<xmlservice>
<cmd error="fast" exec="rexx" var="rtvjoba"><success>+++ success RTVJOBA USRLIBL(?) SYSLIBL(?) CCSID(?N) OUTQ(?)</success>
    <row><data desc="USRLIBL">QGPL       QTEMP      QDEVELOP   QBLDSYS    QBLDSYSR</data></row>
    <row><data desc="SYSLIBL">QSYS       QSYS2      QHLPSYS    QUSRSYS</data></row>
    <row><data desc="CCSID">37</data></row>
    <row><data desc="OUTQ">*DEV</data></row>
</cmd>
</xmlservice>""" # noqa E501


def test_cmd_rexx_row(transport):
    """Test calling command with output parameters returns data in rows"""
    transport.set_out(_xml)

    tk = iToolKit(irow=1)
    tk.add(iCmd('rtvjoba', 'RTVJOBA USRLIBL(?) SYSLIBL(?) CCSID(?N) OUTQ(?)'))

    tk.call(transport)
    rtvjoba = tk.dict_out('rtvjoba')

    assert('success' in rtvjoba)
    assert('row' in rtvjoba)
    row = rtvjoba['row']

    assert(len(row) == 4)
    assert('USRLIBL' in row[0])
    assert('SYSLIBL' in row[1])
    assert('CCSID' in row[2])
    assert('OUTQ' in row[3])


def test_cmd_rexx_no_row(transport):
    """Test calling command with output parms and irow=0 returns data in dict"""
    transport.set_out(_xml)

    tk = iToolKit(irow=0)
    tk.add(iCmd('rtvjoba', 'RTVJOBA USRLIBL(?) SYSLIBL(?) CCSID(?N) OUTQ(?)'))

    tk.call(transport)
    rtvjoba = tk.dict_out('rtvjoba')

    assert('success' in rtvjoba)
    assert('USRLIBL' in rtvjoba)
    assert('SYSLIBL' in rtvjoba)
    assert('CCSID' in rtvjoba)
    assert('OUTQ' in rtvjoba)
