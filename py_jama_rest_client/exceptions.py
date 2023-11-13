class CoreException(Exception):
    """This is the base class for all exceptions raised by the Core"""

    def __init__(self, message, status_code=None, reason=None):
        super(CoreException, self).__init__(message)
        self.status_code = status_code
        self.reason = reason


class UnauthorizedTokenException(CoreException):
    """This exception is thrown whenever fetching the oauth token returns a 401 unauthorized response."""

    pass
