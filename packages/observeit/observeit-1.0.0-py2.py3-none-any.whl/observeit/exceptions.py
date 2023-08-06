"""ObserveIT Exceptions"""


class ObserveITException(Exception):
    """Base Exception class for ObserveIT Exceptions"""
    pass


class IncompatibleAuth(ObserveITException):
    """The Authentication Client used isn't compatible with this API feature"""
    pass


class UnexpectedContentType(ObserveITException):
    """Content Type returned by API is not valid for this API"""
    pass
