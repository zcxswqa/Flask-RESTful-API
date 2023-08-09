"""
This file contains data validation functions related to users authentication.
It uses custom exception for specific error scenarios.
"""

import jwt
import bcrypt
from flask import request
from flask_restful import reqparse
from werkzeug.exceptions import BadRequest

from controllers.custom_exceptions import UnauthorizedError, SignUpError, SignInError, ArgsFieldsError
from models.data_base import users


def token():
    """
    Raises a custom UnauthorizedError for the following cases:

    * Authentication token does not exist.
    * Authentication token does not start with "Bearer ".
    * Authentication token expired.
    * Authentication token is invalid.
    * Authentication token does not relate to any user.
    """
    from main import app
    if "Authorization" not in request.headers:
        raise UnauthorizedError(message="'Authorization' header key is missing or invalid.")
    else:
        authentication_token = request.headers.get("Authorization")
    if not authentication_token:
        raise UnauthorizedError(message="Authorization token is missing.")
    elif not authentication_token.startswith("Bearer "):
        raise UnauthorizedError(message="Authorization token is missing 'Bearer' prefix.")
    authentication_token = authentication_token.split(" ")[1]
    try:
        data = jwt.decode(authentication_token, app.config["SECRET_KEY"], algorithms="HS256")
        if not users.find_one({"Username": data["Username"]}):
            raise UnauthorizedError(message="Authorization token has no user related to it.")
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError(message="Authorization token has expired.")
    except jwt.InvalidTokenError:
        raise UnauthorizedError(message="Authorization token is invalid.")


def username(provided_username):
    """
    Raises a custom SignUpError if username already exist ot contains a non-alphanumeric character.
    """
    if len(provided_username) == 0:
        raise SignUpError(message="Username is empty.")
    elif not provided_username.isalnum():
        raise SignUpError(message=f"Username: '{provided_username}' contain a non alphanumeric character.")
    elif users.find_one({"Username": provided_username}):
        raise SignUpError(message=f"Username: '{provided_username}' is already taken.")


def password(provided_password):
    """
    Raises a custom SignUpError if password is shorter than 8 characters.
    """
    if len(provided_password) == 0:
        raise SignUpError(message="Password is empty.")
    elif len(provided_password) < 8:
        raise SignUpError(message="Password is too short, password needs to be at least 8 characters long.")


def user_exist(provided_username):
    """
    Raises a custom SignInError if username does not exist.
    """
    if len(provided_username) == 0:
        raise SignInError(message="Username is empty.")
    elif not users.find_one({"Username": provided_username}):
        raise SignInError(error="404 Not Found", message="Username does not exist.", status_code=404)


def check_password(provided_password, stored_password):
    """
    Raises a custom SignInError if password is wrong.
    """
    if len(provided_password) == 0:
        raise SignInError(message="Password is empty.")
    elif not bcrypt.checkpw(provided_password.encode("utf-8"), stored_password):
        raise SignInError(message="Password is wrong.")


def args_fields():
    """
    Raises a custom ArgsFieldsError if user request arguments fields are invalid.
    """
    args = reqparse.RequestParser()
    args.add_argument("Username", required=True)
    args.add_argument("Password", required=True)
    try:
        args.parse_args(strict=True)
    except BadRequest:
        raise ArgsFieldsError(message="Some of user args fields names are missing or invalid.")