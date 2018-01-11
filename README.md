# README #

### Python Toolkit ###
The Python is a Python wrapper over the XMLSERVICE open source project from IBM. 
This python .whl/.egg is now jointly maintained by IBM and the KrengelTech Litmis team. 
All future work will be done in this repo.

###Documentation###
* [doc](http://python-itoolkit.readthedocs.io/en/latest)
* [YiPs documentation](http://yips.idevcloud.com/wiki/index.php/XMLSERVICE/Python)

###New whl/egg (laptop, etc.)###
* http://yips.idevcloud.com/wiki/index.php/XMLSERVICE/Python


###Installation###

```
=====
IBM pythons (PTF)
=====
examples:
pip3 uninstall itoolkit
pip3 install dist/itoolkit*34m-os400*.whl

pip2 uninstall itoolkit
pip2 install dist/itoolkit*27m-os400*.whl


======
perzl pythons
======
examples:
rm  -R /opt/freeware/lib/python2.6/site-packages/itoolkit*
easy_install dist/itoolkit*2.6-os400*.egg

rm  -R /opt/freeware/lib/python2.7/site-packages/itoolkit*
easy_install-2.7 dist/itoolkit*2.7-os400*.egg


======
laptop/remote pythons
======
examples:
pip uninstall itoolkit
pip install dist/itoolkit-lite*py2-none*.whl
-- or --
easy_install dist/itoolkit-lite*2.7.egg

```

###python3 UnicodeDecodeError: ascii codec ###

python3 only. Please use test fix  python3-itoolkit-1.3.zip at Yips.

* [YIPs python3-itoolkit-1.3.zip]( http://yips.idevcloud.com/wiki/index.php/XMLSERVICE/Python) - Download .whl (test only).

```
pip3 install dist/*cp34m*.whl
```

Example issue:

```
Traceback (most recent call last):
  File "italy.py", line 16, in <module>
  File "/QOpenSys/QIBM/ProdData/OPS/Python3.4/lib/python3.4/site-packages/itoolkit/itoolkit.py", line 1099, in call
    itrans.call(self)
  File "/QOpenSys/QIBM/ProdData/OPS/Python3.4/lib/python3.4/site-packages/itoolkit/lib/ilibcall.py", line 88, in call
    return itoolkit.itoollib.xmlservice(itool.xml_in(),self.ctl,self.ipc,self.ebcdic_ccsid,self.pase_ccsid)
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 44: ordinal not in range(128)
```



###Builder Notes:###
```
=======
Builder:
=======
./make-whl.sh [34|27|26|34-lite|27-lite|26-lite]
./make-egg.sh [34|27|26|34-lite|27-lite|26-lite]

examples:
./make-whl.sh 34 27 34-lite 27-lite
./make-egg.sh 34 27 34-lite 27-lite

make doc:
> python make_doc.py

remember versions change:
> setup.py
version='x.x' to 'n.n'
> setup-lite.py
version='x.x' to 'n.n'
> itoolkit/__init__.py
__version__ = "x.x" to "n.n"

Can be problem for egg builds.

unable to execute '/QOpenSys/python/lib/python3.4/config/ld_so_aix': No such file or directory
error: command '/QOpenSys/python/lib/python3.4/config/ld_so_aix' failed with exit status 1
ln -s /QOpenSys/QIBM/ProdData/OPS/Python3.4/lib/python3.4/config-3.4m /QOpenSys/QIBM/ProdData/OPS/Python3.4/lib/python3.4/config

/QOpenSys/ranger/home/RANGER/python
/QOpenSys/ranger2/home/ranger2/python
```

#License
MIT.  View [`LICENSE`](https://bitbucket.org/litmis/python-itoolkit/src) file.
