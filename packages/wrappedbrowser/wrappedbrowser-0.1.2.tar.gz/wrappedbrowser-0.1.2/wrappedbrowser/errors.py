"""Errors for `wrappedbrowser`"""


class BaseWrappedbrowserError(Exception):
    """The base error class.
    `wrappedbrowser` error classes should inherit from this."""

    pass


class InvalidDestinationError(BaseWrappedbrowserError):
    """The destination provided is not a valid url or list of url-s."""

    pass
