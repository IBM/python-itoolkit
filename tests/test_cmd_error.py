from itoolkit import iToolKit, iCmd


def test_cmd_error(transport):
    """Test calling a CL command with an invalid parameter returns an error"""

    transport.set_out(
        """<?xml version="1.0" ?><xmlservice><cmd error="fast" exec="cmd" var="cmderror"><error>*** error CHGLIBL LIBL(FROGLEGLONG)</error>
<error>202</error>
<version>XML Toolkit 1.9.9</version>
<error>
<status>202</status>
<errnoxml>1100012</errnoxml>
<xmlerrmsg>XML run cmd failed</xmlerrmsg>
<xmlhint>CHGLIBL LIBL(FROGLEGLONG)</xmlhint>
</error>
<error>
<status>202</status>
<errnoxml>1100012</errnoxml>
<xmlerrmsg>XML run cmd failed</xmlerrmsg>
<xmlhint>CHGLIBL LIBL(FROGLEGLONG)</xmlhint>
</error>
<jobinfo>
<jobipc>*na</jobipc>
<jobipcskey>FFFFFFFF</jobipcskey>
<jobname>QSQSRVR</jobname>
<jobuser>QUSER</jobuser>
<jobnbr>774740</jobnbr>
<jobsts>*ACTIVE</jobsts>
<curuser>KADLER</curuser>
<ccsid>37</ccsid>
<dftccsid>37</dftccsid>
<paseccsid>0</paseccsid>
<langid>ENU</langid>
<cntryid>US</cntryid>
<sbsname>QSYSWRK</sbsname>
<sbslib>QSYS</sbslib>
<curlib/>
<syslibl>QSYS QSYS2 QHLPSYS QUSRSYS</syslibl>
<usrlibl>QGPL QTEMP QDEVELOP QBLDSYS QBLDSYSR</usrlibl>
<jobcpffind>see log scan, not error list</jobcpffind>
</jobinfo>
</cmd>
</xmlservice>""") # noqa E501

    tk = iToolKit()

    tk.add(iCmd('cmderror', 'CHGLIBL LIBL(FROGLEGLONG)'))

    tk.call(transport)

    cmderror = tk.dict_out('cmderror')

    for k, v in cmderror.items():
        if not k.startswith('error'):
            continue

        item = cmderror[k]
        if 'errnoxml' not in item:
            continue

        assert(item['errnoxml'] == '1100012')
