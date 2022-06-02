from ..errors import TransportClosedException

class TransportClosedError(TransportClosedException):
    """Raised when an operation is performed on a closed transport"""
    # TODO: When TransportClosedException is removed, rebase this class on
    # TransportError
    pass

