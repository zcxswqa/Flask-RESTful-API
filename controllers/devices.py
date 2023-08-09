"""
This file contains the implementation of API endpoint related to device operations. It defines the Device resource,
which handles CRUD operations for devices.
"""

from flask import request, jsonify, make_response
from flask_restful import reqparse, Resource

import datetime
import uuid

from models.data_base import devices
from controllers.authentication import authenticate
import controllers.devices_validations as validate
from controllers.custom_exceptions import handle_exceptions, ServerError



def no_conversion_type(value):
    """
    A function used in reqparse.add_argument to ignore its default type modification.
    """
    return value


# device_args: Request parser to validate and parse the input arguments for device creation and update.
device_args = reqparse.RequestParser(bundle_errors=True)

device_args.add_argument("Name", help="Name of device is required.",
                         required=True, type=no_conversion_type)

device_args.add_argument("Serial Number", help="Serial number of device is required.",
                         required=True, type=no_conversion_type)

device_args.add_argument("Is Active", help="Activity of device is required.",
                         required=True, type=no_conversion_type)

device_args.add_argument("Description", help="Description of device.",
                         required=False, type=no_conversion_type)

device_args.add_argument("_id", help="Device ID",
                         required=False, type=no_conversion_type)


class Device(Resource):
    """
    This resource handles device-related operations, including GET, POST, PUT, and DELETE.

    * GET: Retrieves a list of devices or a specific device based on query parameters like name or id.
    * POST: Creates a new device with provided information.
    * PUT: Updates an existing device based on the id provided.
    * DELETE: Deletes a device based on the id provided.
    """
    @handle_exceptions
    @authenticate
    def post(self):
        """
        Create a new device in the database, after validation of user input.

        * Device data: delivered as a json object.

        :return: HTTP response with success message and status code.
        """
        validate.args_fields("POST")
        args = device_args.parse_args(strict=True)

        validate.type_validation(args)
        validate.serial_available(args["Serial Number"])

        args["_id"] = str(uuid.uuid1())
        while devices.find_one({"_id": args["_id"]}):
            args["_id"] = str(uuid.uuid1())
        if not args["Description"]:
            args["Description"] = None
        args["Created at"] = datetime.datetime.now()
        args["Updated at"] = datetime.datetime.now()

        devices.insert_one(args)
        return make_response(jsonify("Device inserted successfully.\n"), 201)

    @handle_exceptions
    @authenticate
    def get(self):
        """
        Get device or devices information from the database based on device name or id, after validation of user input.

        * Device name or ID: delivered in the request arguments.

        :return: HTTP response with device or devices information and a status code.
        """
        validate.args_fields("GET")
        projection = {"Name": 1,
                      "Serial Number": 1,
                      "Is Active": 1,
                      "Description": 1,
                      "Created at": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S.%LZ", "date": "$Created at"}},
                      "Updated at": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S.%LZ", "date": "$Updated at"}}}

        if "Name" in request.args:
            name = request.args.get("Name")
            validate.name_exist(name)
            return make_response(jsonify(list(devices.find({"Name": name}, projection))), 200)

        elif "_id" in request.args:
            id = request.args.get("_id")
            validate.id_exist(id)
            return make_response(jsonify(devices.find_one({"_id": id}, projection)), 200)

        elif len(request.args) == 0:
            validate.database_not_empty()
            return make_response(jsonify(list(devices.find({}, projection))), 200)

        else:
            raise ServerError

    @handle_exceptions
    @authenticate
    def put(self):
        """
        Update a device in the database based on device's ID.

        * Device ID: delivered in the request arguments.
        * Device new data: delivered as a json object.


        :return: HTTP response with success message and status code.
        """
        validate.args_fields("PUT")
        args = device_args.parse_args(strict=True)
        validate.id_exist(args["_id"])
        validate.type_validation(args)
        validate.serial_available_update(args["_id"], args["Serial Number"])

        if not args["Description"]:
            args["Description"] = None
        devices.update_one({"_id": args["_id"]}, {"$set": args})
        devices.update_one({"_id": args["_id"]}, {"$set": {"Updated at": datetime.datetime.now()}})

        return make_response(jsonify("Device updated successfully.\n"), 200)

    @handle_exceptions
    @authenticate
    def delete(self):
        """
        Delete a device from database based on device's ID, after validation of user input.

        * Device ID: delivered in the request arguments.

        :return: HTTP response with success message and status code.
        """
        validate.args_fields("DELETE")
        id = request.args.get("_id")
        validate.id_exist(id)
        devices.delete_one({"_id": id})

        return make_response(jsonify("Device deleted successfully.\n"), 200)


