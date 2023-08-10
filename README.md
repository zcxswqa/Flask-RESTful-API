# Flask-RESTful-API
This project is a RESTful API for managing devices. It allows clients to sign in or sign up and then to create, retrieve, update, and delete devices through HTTP requests.
Additionally, it includes a testing suite to ensure the functionality and integrity of the API.

## Table of Contents
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)

### Prerequisites
- Python 3.x
- Flask (installed via requirements.txt)
- Requests (installed via requirements.txt)
- bcrypt (installed via requirements.txt)
- Flask (installed via requirements.txt)
- Flask-RESTful (installed via requirements.txt)
- PyJWT (installed via requirements.txt)
- pymongo (installed via requirements.txt)
- requests (installed via requirements.txt)
- Werkzeug (installed via requirements.txt)
  

### Installation
1. Clone the repository: `git clone https://github.com/zcxswqa/Flask-RESTful-API.git`
2. Navigate to the project directory: `cd Flask-RESTful-API`
3. Install the required dependencies: `pip install -r requirements.txt`

## Usage

The API provides endpoints for various users operations:

- `POST /Api/V1/Authentication/`: Sign up a new user.
- `GET /Api/V1/Authentication/`: Sign in an existing user and retrive an authorization token.

The API provides endpoints for various device management tasks:

- `POST /Api/V1/Devices/`: Create a new device.
- `GET /Api/V1/Devices/`: Retrieve devices by name, ID, or all devices.
- `PUT /Api/V1/Devices/`: Update a device by ID.
- `DELETE /Api/V1/Devices/`: Delete a device by ID.

To use the API:
1. run `python main.py` in order to activate the server.
2. run `python tests/request_sernder.py` and follow the menu-based interface to interact with the API. OR send http request in other means.

## Testing

The API includes a comprehensive testing suite to ensure its functionality. To run the tests, navigate to the `tests` directory and execute the following command:

`python tests/test.py`

The tests cover scenarios like invalid user signup and signin, invalid requests, and more.
