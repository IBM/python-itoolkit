Python XMLSERVICE Toolkit
=========================

itoolkit is a Python interface to the [XMLSERVICE](https://bitbucket.org/inext/xmlservice-rpg) toolkit for the [IBM i](https://en.wikipedia.org/wiki/IBM_i) platform.

```python
from itoolkit import *
from itoolkit.db2.idb2call import *

itransport = iDB2Call()
itool = iToolKit()

itool.add(iCmd5250('wrkactjob', 'WRKACTJOB'))
itool.call(itransport)
wrkactjob = itool.dict_out('wrkactjob')

print(wrkactjob)
```

For more, check out the [samples](samples/icmd_rtvjoba.py).

Feature Support
---------------

- Call ILE srograms & service programs
- Call CL Commands
- Call PASE shell commands

iLibCall and 64-bit Support
---------------------------

:rotating_light: WARNING WARNING WARNING :rotating_light:

Due to limitations in XMLSERVICE, using iLibCall in a 64-bit process results in failure. See [this bug](https://bitbucket.org/litmis/python-itoolkit/issues/17/ilibcall-fails-on-64-bt-python-versions) for more info.

Documentation
-------------

The docs can be found at <http://python-itoolkit.readthedocs.io/en/latest>

Installation
------------

You can install itoolkit simply using `pip`:

```bash
python3 -m pip install itoolkit
```

License
-------

MIT - See [LICENSE](LICENSE)
