import asyncio


class AGIClientError(Exception):
    """Base class for client connection errors."""


class AGIInvalidURL(AGIClientError, ValueError):
    """Invalid URL.

    URL used for fetching is malformed, e.g. it doesn't contains host
    part."""

    # Derive from ValueError for backward compatibility

    def __init__(self, url):
        super().__init__(url)

    @property
    def url(self):
        return self.args[0]

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.url)


class AGIInvalidMethod(AGIClientError, ValueError):
    pass


class AGIClientConnectionError(AGIClientError):
    """Base class for client socket errors."""


class AGIServerConnectionError(AGIClientConnectionError):
    """Server connection errors."""


class AGIServerTimeoutError(AGIServerConnectionError, asyncio.TimeoutError):
    """Server timeout error."""
