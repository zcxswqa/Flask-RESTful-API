"""
This file serves as the entry point for the Flask API.
It creates a Flask application, sets up the API routes, and configures the authentication secret key.

* app: The Flask application object.
* api: The Flask-RESTful API object.
* app.config["SECRET_KEY"]: A secret key used for JWT authentication.

API Routes

* /Api/V1/Devices/: This route handles device-related CRUD operations.
* /Api/V1/Authentication/: This route handles user authentication using JWT.
    It includes GET (Generate JWT token to registered users) and POST (User registration).
"""

from flask import Flask
from flask_restful import Api

import secrets

from controllers.devices import Device
from controllers.authentication import Authentication
from controllers.custom_exceptions import handle_exceptions, InvalidURLError


app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"] = secrets.token_hex(32)

api.add_resource(Device, "/Api/V1/Devices/")
api.add_resource(Authentication, "/Api/V1/Authentication/")


@app.errorhandler(404)
@handle_exceptions
def not_found_error(error):
    raise InvalidURLError


if __name__ == "__main__":
    app.run(debug=True)
