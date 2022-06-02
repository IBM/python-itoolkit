__all__ = [
    'TransportError',
    'TransportClosedException',
]

class TransportError(Exception):
    """Base exception class for all transport errors"""
    pass

class TransportClosedException(TransportError):
    """Deprecated alias of :py:exc:`itoolkit.transport.TransportClosedError`"""
    pass
