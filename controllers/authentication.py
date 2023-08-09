"""
This file contains the implementation of API endpoint related to users authentication.
It defines the Authentication resource, which handles creation and authentications of users.
"""

import datetime

from flask import request, jsonify, make_response
from flask_restful import reqparse, Resource
from models.data_base import users
import jwt
import bcrypt

import controllers.authentication_validations as validate
from controllers.custom_exceptions import handle_exceptions

# authentication_args: Request parser to validate and parse the input arguments for users creation and authentication.
authentication_args = reqparse.RequestParser()
authentication_args.add_argument("Username", type=str, required=True)
authentication_args.add_argument("Password", type=str, required=True)


def authenticate(func):
    """
    Decorator function to authenticate API endpoints.

    It checks the provided JWT token in the request headers to validate user authentication.
    """
    def decorate(*args, **kwargs):
        validate.token()
        return func(*args, **kwargs)
    return decorate


def verify(func):
    """
    Decorator function to validate username and password.

    It checks the provided username and password in the request arguments to validate their syntax and availability.
    """
    def decorate(*args, **kwargs):
        validate.args_fields()
        user_args = authentication_args.parse_args()
        validate.username(user_args["Username"])
        validate.password(user_args["Password"])
        return func(*args, **kwargs)
    return decorate


class Authentication(Resource):
    """
        This resource handles users-related operations, including GET and POST.

        * GET: Retrieves a token for authentication on the protected endpoints.
        * POST: Creates a new user with provided username and password.
        """
    @handle_exceptions
    @verify
    def post(self):
        """
        Create a new user in the database, after validation of username and password, hashing and salting.

        * Username and password: delivered as json object.

        :return: HTTP response with success message and status code.
        """
        user_args = authentication_args.parse_args()

        salt = bcrypt.gensalt()
        user_args["Password"] = bcrypt.hashpw(user_args["Password"].encode("utf-8"), salt)

        users.insert_one(user_args)

        return make_response(jsonify("User created successfully.\n"), 201)

    @handle_exceptions
    def get(self):
        """
        Get a JWT authentication token if username and password are correct.

        * Username and password: delivered as json object.

        :return: HTTP response with authentication token and status code.
        """
        from main import app

        validate.args_fields()
        provided_user = authentication_args.parse_args()
        validate.user_exist(provided_user["Username"])

        stored_user = users.find_one({"Username": provided_user["Username"]})
        validate.check_password(provided_user["Password"], stored_user["Password"])

        token = jwt.encode({"Username": provided_user["Username"],
                            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config["SECRET_KEY"],
                           algorithm="HS256")

        return make_response(jsonify({"token": token}), 200)


