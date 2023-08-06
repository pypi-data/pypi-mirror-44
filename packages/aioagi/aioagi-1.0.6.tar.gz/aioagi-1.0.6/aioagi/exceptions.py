from aioagi.response import AGIResponse


class AGIException(AGIResponse, Exception):
    pass


class AGIHangup(AGIException):
    status = 204


class AGIResultHangup(AGIHangup):
    pass


class AGIConnectHangup(AGIHangup):
    pass


class AGIMove(AGIException):
    verbose = 3
    status = 300

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if url:
            self.message = 'Location: {}'.format(url)


class FailureAGIError(AGIException):
    content = 'FAILURE\n'
    verbose = 3


# ############
# Client Error
# ############


class AGIBadRequest(FailureAGIError):
    status = 400


class AGINotAuthenticated(FailureAGIError):
    status = 401


class AGIPermissionDenied(FailureAGIError):
    status = 403


# Resolver exceptions
class AGIMethodNotAllowed(FailureAGIError):
    status = 405


class AGINotFound(FailureAGIError):
    status = 404


class AGIAppError(FailureAGIError):
    status = 421


class AGIUnprocessableEntityError(FailureAGIError):
    status = 422


# #############
# Server errors
# #############
class AGIInternalServerError(FailureAGIError):
    status = 500
    verbose = 2

    def __init__(self, error='', *args, **kwargs):
        self.error = error
        super().__init__(*args, **kwargs)


# Command errors
class AGIMemoryAllocationFailure(AGIInternalServerError):
    status = 503


class AGIInvalidCommand(AGIInternalServerError):
    status = 510


class AGICommandNotPermittedError(AGIInternalServerError):
    status = 511


class AGIUsageError(AGIInternalServerError):
    status = 520
