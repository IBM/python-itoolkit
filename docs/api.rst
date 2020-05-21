.. _api:

API Reference
=============

.. module:: itoolkit


Toolkit Object
--------------

.. autoclass:: iToolKit
   :members:
   :inherited-members:

Toolkit Operations
------------------

.. autoclass:: iPgm
   :members:
   :inherited-members:


.. autoclass:: iSrvPgm
   :members:
   :inherited-members:

.. autoclass:: iCmd
   :members:
   :inherited-members:

.. autoclass:: iCmd5250
   :members:
   :inherited-members:

.. autoclass:: iSh
   :members:
   :inherited-members:

.. autoclass:: iXml
   :members:
   :inherited-members:

.. autoclass:: iDS
   :members:
   :inherited-members:

.. autoclass:: iData
   :members:
   :inherited-members:



Transports
----------
.. module:: itoolkit.transport

.. autoclass:: XmlServiceTransport
   :members:
   :inherited-members:

HTTP Transport
~~~~~~~~~~~~~~

.. autoclass:: HttpTransport
   :members:
   :inherited-members:

Database Transport
~~~~~~~~~~~~~~~~~~

.. autoclass:: DatabaseTransport
   :members:
   :inherited-members:

SSH Transport
~~~~~~~~~~~~~~~~~~

.. autoclass:: SshTransport
   :members:
   :inherited-members:


Direct Memory Transport
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: DirectTransport
   :members:
   :inherited-members:
.. note::
   This transport will only work when run on an IBM i system. On other operating
   systems, calling it will fail with a :class:`RuntimeError`.
.. warning::
   When using a 64-bit Python, this transport will only work with XMLSERVICE
   2.0.1 or higher. When using the system XMLSERVICE in QXMLSERV, the following
   PTFs are available to fix this problem:

   - IBM i 7.4 - SI70669
   - IBM i 7.3 - SI70668
   - IBM i 7.2 - SI70667
   

Deprecated Transports
---------------------

.. module:: itoolkit.rest.irestcall
.. py:class:: iRestCall
.. deprecated:: 1.6.0
   Use :class:`itoolkit.transport.HttpTransport` instead.

.. module:: itoolkit.db2.idb2call
.. py:class:: iDB2Call
.. deprecated:: 1.6.0
   Use :class:`itoolkit.transport.DatabaseTransport` instead.

.. module:: itoolkit.lib.ilibcall
.. py:class:: iLibCall
.. deprecated:: 1.6.0
   Use :class:`itoolkit.transport.DirectTransport` instead.
