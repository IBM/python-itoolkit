from itoolkit import iToolKit, iPgm


def test_pgm_error(transport):
    """Test calling program which doesn't exist returns an error"""

    transport.set_out("""<?xml version="1.0" ?>
<xmlservice>
<pgm error="fast" name="ZZCALLNOT" var="zzcall">
    <error>*** error XMLSERVICE ZZCALLNOT</error>
    <version>XML Toolkit 1.9.9</version>
    <error>
        <errnoxml>1100016</errnoxml>
        <xmlerrmsg>XML run pgm failed</xmlerrmsg>
        <xmlhint><pgm error="fast" name="ZZCALLNOT" var="zzcall"><parm io="b</xmlhint>
    </error>
    <error>
        <errnoxml>1000005</errnoxml>
        <xmlerrmsg>PASE resolve failed</xmlerrmsg>
        <xmlhint>ZZCALLNOT</xmlhint>
    </error>
    <error>
        <errnoxml>1100016</errnoxml>
        <xmlerrmsg>XML run pgm failed</xmlerrmsg>
        <xmlhint><pgm error="fast" name="ZZCALLNOT" var="zzcall"><parm io="b</xmlhint>
    </error>
    <jobinfo>
    <jobipc>*na</jobipc>
    <jobipcskey>FFFFFFFF</jobipcskey>
    <jobname>QSQSRVR</jobname>
    <jobuser>QUSER</jobuser>
    <jobnbr>570746</jobnbr>
    <jobsts>*ACTIVE</jobsts>
    <curuser>KADLER</curuser>
    <ccsid>37</ccsid>
    <dftccsid>37</dftccsid>
    <paseccsid>819</paseccsid>
    <langid>ENU</langid>
    <cntryid>US</cntryid>
    <sbsname>QSYSWRK</sbsname>
    <sbslib>QSYS</sbslib>
    <curlib/>
    <syslibl>QSYS QSYS2 QHLPSYS QUSRSYS</syslibl>
    <usrlibl>QGPL QTEMP QDEVELOP QBLDSYS QBLDSYSR</usrlibl>
    <jobcpffind>see log scan, not error list</jobcpffind>
    </jobinfo>
</pgm>
</xmlservice>
""") # noqa E501

    tk = iToolKit()
    tk.add(iPgm('zzcallnot', 'ZZCALLNOT', {'lib': 'XMLSERVICE'}))

    tk.call(transport)

    zzcallnot = tk.dict_out('zzcallnot')

    for k, v in zzcallnot.items():
        if not k.startswith('error'):
            continue

        if 'errnoxml' not in v:
            continue

        assert(v['errnoxml'] in ('1100005', '1100016'))
