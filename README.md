# README #

### Python Toolkit ###
The Python is a Python wrapper over the XMLSERVICE open source project from IBM. 
This python .whl/.egg is now jointly maintained by IBM and the KrengelTech Litmis team. 
All future work will be done in this repo.

###Documentation###
* [doc](https://bitbucket.org/litmis/python-itoolkit/src/master/itoolkit/doc) directory in this repo
* [http://yips.idevcloud.com/wiki/index.php/XMLSERVICE/Python](YiPs documentation)

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