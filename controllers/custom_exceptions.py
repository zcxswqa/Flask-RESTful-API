"""
This file contains a decorator function handle_exceptions, which catches custom exceptions
and returns appropriate HTTP responses with error messages and status codes.
It also defines the custom exception classes mentioned above.
"""

from flask import jsonify, make_response


def handle_exceptions(func):
    """
    A decorator that catches the custom exceptions and returns appropriate HTTP responses with error messages
    and status code.
    """
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except (SignUpError, SignInError, ArgsFieldsError,
                DeviceNotFoundError, DeviceConflictError, DataTypeError,
                InvalidURLError) as e:

            return make_response(jsonify({e.error: str(e)}), e.status_code)

        except UnauthorizedError as e:
            response = make_response(jsonify({e.error: str(e)}), e.status_code)
            response.headers["WWW-Authenticate"] = 'Bearer realm = "Devices",' \
                                                   'error = "Invalid token",' \
                                                   'error_description = "Token is invalid or non existing"'
            return response

        except Exception as e:
            return make_response(jsonify({"ERROR": str(e)}), 500)
    return decorate


class DeviceNotFoundError(Exception):
    """
    Raised when a device with a given id or name is not found in the database.
    """
    def __init__(self, error="404 Not Found", message="Device was not found in the database.", status_code=404):
        self.error = error
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DeviceConflictError(Exception):
    """
    Raised when a device with a given serial number already exist in the database.
    """
    def __init__(self, error="409 Conflict", message="Device conflict.", status_code=409):
        self.error = error
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DataTypeError(Exception):
    """
    Raised when incorrect data types are provided for device attributes.
    """
    def __init__(self, error="400 Bad request", message="Data type is wrong.", status_code=400):
        self.error = error
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UnauthorizedError(Exception):
    """
    Raised when incorrect data types are provided for device attributes.
    """
    def __init__(self, error="401 Unauthorized", message="Access denied.", status_code=401):
        self.error = error
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
     
        
class SignUpError(Exception):
    """
    Raised when there are issues with user registration (e.g., illegal username or short password).
    """
    def __init__(self, error="400 Bad request", message="Username or password are illegal.", status_code=400):
        self.error = error
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
        
        
class SignInError(Exception):
    """
    Raised when login credentials are incorrect.
    """
    def __init__(self, error="400 Bad request", message="Username or password are wrong.", status_code=400):
        self.error = error
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ArgsFieldsError(Exception):
    """
    Raised when request arguments fields are invalid.
    """
    def __init__(self, error="400 Bad request", message="Some of request arguments fields names are missing or invalid.", status_code=400):
        self.error = error
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ServerError(Exception):
    """
    Raised when an unexpected error occurred.
    """
    def __init__(self, error="500 Internal Server Error", message="An unexpected error occurred.", status_code=500):
        self.error = error
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class InvalidURLError(Exception):
    """
    Raised when reaching to an invalid URL.
    """
    def __init__(self, error="404 Not Found",
                 message="The requested URL was not found on the server. "
                         "If you entered the URL manually please check your spelling and try again.",
                         status_code=404):
        self.error = error
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
