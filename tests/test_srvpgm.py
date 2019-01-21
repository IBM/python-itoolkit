from itoolkit import iToolKit, iSrvPgm, iData, iDS


def test_srvpgm(transport):
    """Test calling ZZARRAY in ZZSSRV
    https://bitbucket.org/inext/xmlservice-rpg/src/master/test.rpg/zzsrv.rpgle
    """

    max_return = 4
    name = 'Ranger'

    transport.set_out("""<?xml version="1.0" ?>
<xmlservice>
<pgm error="fast" func="ZZARRAY" name="ZZSRV" lib="XMLSERVICE" var="zzarray">
    <parm io="both" var="p1">
        <data type="10a" var="myName">{0}</data>
    </parm>
    <parm io="both" var="p2">
        <data type="10i0" var="myMax">{1}</data>
    </parm>
    <parm io="both" var="p3">
        <data enddo="mycnt" type="10i0" var="myCount">{1}</data>
    </parm>
    <return var="r4">
        <ds dim="999" dou="mycnt" var="dcRec_t">
            <data type="10a" var="dcMyName">{0}1</data>
            <data type="4096a" var="dcMyJob">Test 101</data>
            <data type="10i0" var="dcMyRank">11</data>
            <data type="12p2" var="dcMyPay">13.42</data>
        </ds>
        <ds dim="999" dou="mycnt" var="dcRec_t">
            <data type="10a" var="dcMyName">{0}2</data>
            <data type="4096a" var="dcMyJob">Test 102</data>
            <data type="10i0" var="dcMyRank">12</data>
            <data type="12p2" var="dcMyPay">26.84</data>
        </ds>
        <ds dim="999" dou="mycnt" var="dcRec_t">
            <data type="10a" var="dcMyName">{0}3</data>
            <data type="4096a" var="dcMyJob">Test 103</data>
            <data type="10i0" var="dcMyRank">13</data>
            <data type="12p2" var="dcMyPay">40.26</data>
        </ds>
        <ds dim="999" dou="mycnt" var="dcRec_t">
            <data type="10a" var="dcMyName">{0}4</data>
            <data type="4096a" var="dcMyJob">Test 104</data>
            <data type="10i0" var="dcMyRank">14</data>
            <data type="12p2" var="dcMyPay">53.68</data>
        </ds>
    </return>
    <success>+++ success XMLSERVICE ZZSRV ZZARRAY</success>
</pgm>
</xmlservice>""".format(name, max_return))

    tk = iToolKit()
    tk.add(iSrvPgm('zzarray', 'ZZSRV', 'ZZARRAY', {'lib': 'XMLSERVICE'})
           .addParm(iData('myName', '10a', name))
           .addParm(iData('myMax', '10i0', max_return))
           .addParm(iData('myCount', '10i0', '', {'enddo': 'mycnt'}))
           .addRet(iDS('dcRec_t', {'dim': '999', 'dou': 'mycnt'})
                   .addData(iData('dcMyName', '10a', ''))
                   .addData(iData('dcMyJob', '4096a', ''))
                   .addData(iData('dcMyRank', '10i0', ''))
                   .addData(iData('dcMyPay', '12p2', ''))
                   )
           )
    tk.call(transport)

    zzarray = tk.dict_out('zzarray')
    assert('success' in zzarray)

    assert(zzarray['myName'] == name)
    assert(zzarray['myMax'] == str(max_return))
    assert(zzarray['myCount'] == str(max_return))

    for i, rec in enumerate(zzarray['dcRec_t'], start=1):
        assert(i <= max_return)

        assert(rec['dcMyName'] == name + str(i))
        assert(rec['dcMyJob'] == "Test 10" + str(i))
        assert(int(rec['dcMyRank']) == 10 + i)
        assert(float(rec['dcMyPay']) == 13.42 * i)
