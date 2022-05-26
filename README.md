Python XMLSERVICE Toolkit
=========================

[![Build Status](https://github.com/IBM/python-itoolkit/actions/workflows/build.yml/badge.svg?branch=main&event=push)](https://github.com/IBM/python-itoolkit/actions/workflows/build.yml)
[![Latest version released on PyPi](https://img.shields.io/pypi/v/itoolkit.svg)](https://pypi.python.org/pypi/itoolkit)
[![](https://img.shields.io/pypi/pyversions/itoolkit.svg)](https://pypi.org/project/itoolkit/)
[![Documentation Status](https://readthedocs.org/projects/python-itoolkit/badge/?version=latest)](https://python-itoolkit.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/IBM/python-itoolkit/branch/master/graph/badge.svg)](https://codecov.io/gh/IBM/python-itoolkit)


itoolkit is a Python interface to the
[XMLSERVICE](https://github.com/IBM/xmlservice) toolkit for the
[IBM i](https://en.wikipedia.org/wiki/IBM_i) platform.

```python
from itoolkit import *
from itoolkit.transport import DatabaseTransport
import ibm_db_dbi

conn = ibm_db_dbi.connect()
itransport = DatabaseTransport(conn)
itool = iToolKit()

itool.add(iCmd5250('wrkactjob', 'WRKACTJOB'))
itool.call(itransport)
wrkactjob = itool.dict_out('wrkactjob')

print(wrkactjob)
```

For more, check out the [samples](samples).

Feature Support
---------------

- Call ILE programs & service programs
- Call CL Commands
- Call PASE shell commands

Documentation
-------------

The docs can be found at <http://python-itoolkit.readthedocs.io/en/latest>

Installation
------------

You can install itoolkit simply using `pip`:

```bash
python -m pip install itoolkit
```

Tests
-----

To test the installed itoolkit

```bash
python -m pytest
```

To test the local code:

```bash
PYTHONPATH=src python -m pytest
```

Contributing
------------

Please read the [contribution guidelines](CONTRIBUTING.md).

Releasing a New Version
-----------------------

Run the following commands

```
# checkout and pull the latest code from master
git checkout master
git pull

# bump to a release version (a tag and commit are made)
bumpversion release

# build the new distribution and upload to PyPI
poetry publish --build

# bump to the new dev version (a commit is made)
bumpversion --no-tag patch

# push the new tag and commits
git push origin master --tags
```

License
-------

MIT - See [LICENSE](LICENSE)
