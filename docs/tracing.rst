.. _tracing:

Tracing
=======

When diagnosing itoolkit issues, it may be helpful to trace the call to XMLSERVICE.
To facilitate this, :func:`iToolKit.call()`, will trace out the following info:

- XMLSERVICE ipc and ctl options and any transport-specific options
- The generated input XML before sending to XMLSERVICE
- The output XML received from XMLSERVICE

If the received XML fails to parse, it will also be dumped in hex.


Capturing Trace Output
----------------------

Since itoolkit version 2.0, tracing data is logged via the standard Python
`logging <https://docs.python.org/3/howto/logging.html>`_ framework using the
``itoolkit-trace`` logger and all trace records are logged at ``INFO`` level.

There are many ways to capture the logs, though a standard way is to write them
to a file. For more ways to capture the logs, refer to `Python's built-in
loggers <https://docs.python.org/3/howto/logging.html#useful-handlers>`_.


Basic File Trace Example
~~~~~~~~~~~~~~~~~~~~~~~~

This is a simple example which outputs the trace messages to a file with no
other metadata.

.. code-block:: python

  import logging
  logger = logging.getLogger('itoolkit-trace')
  logger.setLevel(logging.INFO)
  logger.addHandler(logging.FileHandler('itoolkit.log'))

  tk.call(transport)

Advanced File Trace Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example, each trace message is preceded by the time it was logged along
with the process id and thread id where it was logged. This is more useful in
multi-threaded Python server applications.

.. code-block:: python

  import logging

  # Log the time, process id, and thread id along with the message
  formatter = logging.Formatter(fmt='%(asctime)s %(process)d %(thread)d %(message)s')

  handler = logging.FileHandler('itoolkit.log')
  handler.setFormatter(formatter)

  logger = logging.getLogger('itoolkit-trace')
  logger.setLevel(logging.INFO)
  logger.addHandler(handler)

  tk.call(transport)

