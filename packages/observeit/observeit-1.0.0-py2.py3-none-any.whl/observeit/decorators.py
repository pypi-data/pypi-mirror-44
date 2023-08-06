from observeit.clients.observeit_login_client import ObserveITLoginClient
from observeit.exceptions import IncompatibleAuth


def login_auth_only(func):
    """Endpoint only supports JWT tokens from logins, not OAuth"""
    def function_wrapper(*args, **kwargs):
        client = args[0]
        if not isinstance(client, ObserveITLoginClient):
            # OAuth Client not supported
            raise IncompatibleAuth()
        return func(*args, **kwargs)
    return function_wrapper
