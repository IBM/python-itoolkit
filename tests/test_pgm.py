from itoolkit import iToolKit, iPgm, iDS, iData


def test_pgm(transport):
    """Test calling ZZCALL
    https://bitbucket.org/inext/xmlservice-rpg/src/master/test.rpg/zzcall.rpgle
    """

    transport.set_out("""<?xml version="1.0" ?>
<xmlservice>
    <pgm error="fast" lib="XMLSERVICE" name="ZZCALL" var="zzcall">
        <parm io="both" var="p1">
            <data type="1a" var="INCHARA">C</data>
        </parm>
        <parm io="both" var="p2">
            <data type="1a" var="INCHARB">D</data>
        </parm>
        <parm io="both" var="p3">
            <data type="7p4" var="INDEC1">321.1234</data>
        </parm>
        <parm io="both" var="p4">
            <data type="12p2" var="INDEC2">1234567890.12</data>
        </parm>
        <parm io="both" var="p5">
            <ds var="INDS1">
                <data type="1a" var="DSCHARA">E</data>
                <data type="1a" var="DSCHARB">F</data>
                <data type="7p4" var="DSDEC1">333.3330</data>
                <data type="12p2" var="DSDEC2">4444444444.44</data>
            </ds>
        </parm>
        <success>+++ success XMLSERVICE ZZCALL </success>
    </pgm>
</xmlservice>
""")

    tk = iToolKit()
    tk.add(
        iPgm('zzcall', 'ZZCALL', {'lib': 'XMLSERVICE'})
        .addParm(iData('INCHARA', '1a', 'a'))
        .addParm(iData('INCHARB', '1a', 'b'))
        .addParm(iData('INDEC1', '7p4', '32.1234'))
        .addParm(iData('INDEC2', '12p2', '33.33'))
        .addParm(iDS('INDS1')
                 .addData(iData('DSCHARA', '1a', 'a'))
                 .addData(iData('DSCHARB', '1a', 'b'))
                 .addData(iData('DSDEC1', '7p4', '32.1234'))
                 .addData(iData('DSDEC2', '12p2', '33.33'))
                 )
    )
    tk.call(transport)

    zzcall = tk.dict_out('zzcall')

    assert('success' in zzcall)

    assert(zzcall['INCHARA'] == 'C')
    assert(zzcall['INCHARB'] == 'D')
    assert(zzcall['INDEC1'] == '321.1234')
    assert(zzcall['INDEC2'] == '1234567890.12')
    assert(zzcall['INDS1']['DSCHARA'] == 'E')
    assert(zzcall['INDS1']['DSCHARB'] == 'F')
    assert(zzcall['INDS1']['DSDEC1'] == '333.3330')
    assert(zzcall['INDS1']['DSDEC2'] == '4444444444.44')
