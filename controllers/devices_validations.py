"""
This file contains data validation functions related to device operations.
It uses custom exception for specific error scenarios.
"""

from flask import request
from flask_restful import reqparse
from werkzeug.exceptions import BadRequest

from controllers.custom_exceptions import DeviceNotFoundError, DeviceConflictError, DataTypeError, ArgsFieldsError, ServerError
from models.data_base import devices


def id_exist(device_id):
    """
    Raises a custom DeviceNotFoundError if no device with the given device id is not found in the database.
    """
    if not devices.find_one({"_id": device_id}):
        raise DeviceNotFoundError(message=f"Device with id: '{device_id}' does not exist.")


def serial_available(device_serial):
    """
    Raises a custom DeviceConflictError if a device with the given device serial number is found in the database.
    """
    if devices.find_one({"Serial Number": device_serial}):
        raise DeviceConflictError(message=f"Device with serial number: '{str(device_serial)}' already exist.")


def serial_available_update(device_id, device_serial):
    """
    Raises a custom DeviceConflictError if a device with the given device serial number is found in the database,
    and is not the device to be updated.
    """
    if devices.find_one({"_id": device_id}) == devices.find_one({"Serial Number": device_serial}):
        return
    elif devices.find_one({"Serial Number": device_serial}):
        raise DeviceConflictError(message=f"Device with serial number: '{str(device_serial)}' already exist.")
    else:
        return


def name_exist(device_name):
    """
    Raises a custom DeviceNotFoundError if no device with the given name is not found in the database.
    """
    if not devices.find_one({"Name": device_name}):
        raise DeviceNotFoundError(message=f"Device name: '{device_name}' doesn't exist.")


def database_not_empty():
    """
    Raises a custom DeviceNotFoundError if no device is not found in the database.
    """
    if len(list(devices.find())) == 0:
        raise DeviceNotFoundError(message="No devices exist in the database.")


def type_validation(args):
    """
    Raises a custom DataTypeError if device arguments are not in the right type.

    * Device Name: string.
    * Device Serial Number: int.
    * Device Activation status: bool.
    * Device Description: string ot None
    """
    name = args["Name"]
    serial = args["Serial Number"]
    activation = args["Is Active"]
    description = args["Description"]

    if not isinstance(name, str):
        raise DataTypeError(message=f"Name must be a string, but was sent as: {str(type(name))}")

    elif not isinstance(serial, int) or isinstance(serial, bool):
        raise DataTypeError(message=f"Serial Number must be an int, but was sent as: {str(type(serial))}")

    elif not isinstance(activation, bool):
        raise DataTypeError(message=f"Activation Status must be a boolean, but was sent as: {str(type(activation))}")

    elif not isinstance(description, str) and description is not None:
        raise DataTypeError(message=f"Description must be a string, but was sent as: {str(type(description))}")


def args_fields(method):
    """
    Raises a custom ArgsFieldsError if device request arguments fields are invalid.
    """
    if method == "GET":
        if "Name" not in request.args and "_id" not in request.args and len(request.args) > 0:
            raise ArgsFieldsError(message="Request should be formatted as '?_id=' or '?Name='")
        elif len(request.args) > 1:
            raise ArgsFieldsError(message="Request should contain either id or name field.")

        else:
            return
    elif method == "PUT" or method == "POST":
        args = reqparse.RequestParser()
        args.add_argument("Name", required=True)
        args.add_argument("Serial Number", required=True)
        args.add_argument("Is Active", required=True)
        args.add_argument("Description", required=False)
        if method == "PUT":
            args.add_argument("_id", required=False)
    elif method == "DELETE":
        if len(request.args) > 1:
            raise ArgsFieldsError(message="Request should only contain device id field.")
        elif len(request.args) == 0:
            raise ArgsFieldsError(message="Request is empty.")
        elif "_id" not in request.args:
            raise ArgsFieldsError(message="Request should be formatted as '?_id='")
        else:
            return
    else:
        raise ServerError

    try:
        args.parse_args(strict=True)
    except BadRequest:
        raise ArgsFieldsError(message="Some of device arguments fields names are missing or invalid.")