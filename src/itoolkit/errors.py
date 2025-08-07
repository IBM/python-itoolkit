# Copyright contributors to the python-itoolkit project 
# SPDX-License-Identifier: MIT
__all__ = [
    'TransportError',
    'TransportClosedException',
]

class TransportError(Exception):
    """Base exception class for all transport errors

    .. versionadded:: 1.7.1
    """
    pass

class TransportClosedException(TransportError):
    """Alias of :py:exc:`itoolkit.transport.TransportClosedError`

    .. deprecated:: 1.7.1
      Use :py:exc:`itoolkit.transport.TransportClosedError` instead.
    """
    pass
