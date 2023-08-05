"""
https://curl.haxx.se/libcurl/c/libcurl-errors.html
"""
#import pycurl
#
#from .pycurl_error import PYCURL_ERRNO_TAG


class IowebError(Exception):
    pass


class NetworkError(IowebError):
    """
    NetworkError instance stores original transport-specific error
    in `transport_error` attribute.
    """
    def __init__(self, *args):
        self.errmsg = None
        self.transport_error = None
        if len(args) > 0:
            self.errmsg = args[0]
        if len(args) > 1:
            self.transport_error = args[1]

    def get_tag(self):
        #if isinstance(self.transport_error, pycurl.error):
        #    errno = self.transport_error.args[0]
        #    errmsg = self.transport_error.args[1]
        #    if (
        #            errno == 28 and (
        #                'Connection time-out' in errmsg
        #                or 'Connection timed out' in errmsg
        #            )
        #        ):
        #        return 'connection-timed-out'
        #    else:
        #        return PYCURL_ERRNO_TAG[errno]
        #else:
        return self.transport_error.__class__.__name__.lower()


class DataWriteError(NetworkError):
    """
    CURLE_WRITE_ERROR (23)

    An error occurred when writing received data to a local file,
    or an error was returned to libcurl from a write callback.
    """


class OperationTimeoutError(NetworkError):
    """
    CURLE_OPERATION_TIMEDOUT (28)

    Operation timeout. The specified time-out period was reached
    according to the conditions.
    """


class ConnectError(NetworkError):
    """
    CURLE_COULDNT_CONNECT (7)

    Failed to connect() to host or proxy.
    """


class AuthError(NetworkError):
    """
    CURLE_LOGIN_DENIED (67)

    The remote server denied curl to login (Added in 7.13.1)
    """


class TooManyRedirectsError(NetworkError):
    """
    CURLE_TOO_MANY_REDIRECTS (47)

    Too many redirects. When following redirects, libcurl hit the
    maximum amount. Set your limit with CURLOPT_MAXREDIRS.
    """


class ResolveHostError(NetworkError):
    """
    CURLE_COULDNT_RESOLVE_HOST (6)

    Couldn't resolve host. The given remote host was not resolved.
    """


class InvalidUrlError(NetworkError):
    """
    CURLE_URL_MALFORMAT (3)

    The URL was not properly formatted.
    """


class MalformedResponseError(NetworkError):
    """
    Raised when parser fails to parse response HTTP headers
    """


ERRNO_CLASS_MAPPING = {
    3: InvalidUrlError,
    6: ResolveHostError,
    7: ConnectError,
    23: DataWriteError,
    28: OperationTimeoutError,
    47: TooManyRedirectsError,
    67: AuthError,
}


#def build_network_error(errno, errmsg):
#    cls = ERRNO_CLASS_MAPPING.get(errno, NetworkError)
#    return cls(errmsg, pycurl.error(errno, errmsg))
