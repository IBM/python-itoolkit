__all__ = [
    'TransportClosedException',
]


class TransportClosedException(Exception):
    """Raised when an operation is performed on a closed transport"""
    pass
