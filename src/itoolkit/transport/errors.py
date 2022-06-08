from ..errors import TransportClosedException

class TransportClosedError(TransportClosedException):
    """Raised when an operation is performed on a closed transport

    .. versionadded:: 1.7.1
    """
    # TODO: When TransportClosedException is removed, rebase this class on
    # TransportError
    pass

