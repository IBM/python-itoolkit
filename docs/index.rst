itoolkit for Python
===================

itoolkit is a Python interface to the `XMLSERVICE`_ toolkit for the `IBM i`_ platform.

.. _XMLSERVICE: https://github.com/IBM/xmlservice
.. _IBM i: https://en.wikipedia.org/wiki/IBM_i

Usage
-----

.. code-block:: python

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

For more, check out the :ref:`Examples <examples>`.

Feature Support
---------------

- Call ILE programs & service programs
- Call CL Commands
- Call PASE shell commands

Installation
------------

You can install itoolkit simply using `pip`:

.. code-block:: bash

   python -m pip install itoolkit

Table of Contents
-----------------

.. toctree::
   :maxdepth: 1 

   api
   examples
