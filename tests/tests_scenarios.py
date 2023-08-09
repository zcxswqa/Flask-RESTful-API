"""
This file contains the invalid requests scenarios for the tests.py file.
"""

valid_json = {"Name": "device_1", "Serial Number": 1, "Is Active": True, "Description": "all good"}

invalid_headers = {"invalid token": {"Authorization": "Bearer invalid_token"},
                   "No bearer prefix": {"Authorization": "invalid_token"},
                   "Wrong authorization key": {"Auth": "Bearer invalid_token"},
                   "No token": {"Authorization": ""},
                   }

invalid_signup_jsons = {"User already exist:": {"Username": "testing", "Password": "password123"},
                        "non-alphanumeric:": {"Username": "user_123", "Password": "password123"},
                        "Username is empty:": {"Username": "", "Password": "password123"},
                        "Short password:": {"Username": "user123", "Password": "1234567"},
                        "Password is empty:": {"Username": "user123", "Password": ""},
                        "Wrong 'Username' field name:": {"UserName": "user123", "Password": "password123"},
                        "Wrong 'Password' field name:": {"Username": "user123", "PassWord": "password123"},
                        "No 'Password' field:": {"Username": "user123"},
                        "No 'Username' field:": {"Password": "password123"},
                        "Empty request:": {}
                        }

invalid_signin_jsons = {"Non existing user:": {"Username": "nope", "Password": "password123"},
                        "Wrong password:": {"Username": "testing", "Password": "nope"},
                        "Username is empty:": {"Username": "", "Password": "password123"},
                        "Password is empty:": {"Username": "testing", "Password": ""},
                        "Wrong 'Username' field name:": {"UserName": "user123", "Password": "password123"},
                        "Wrong 'Password' field name:": {"Username": "user123", "PassWord": "password123"},
                        "No 'Password' field:": {"Username": "user123"},
                        "No 'Username' field:": {"Password": "password123"},
                        "Empty request:": {}
                        }

invalid_post_jsons = {"No 'Name' field:": {"Serial Number": 1, "Is Active": True, "Description": "noName"},
                      "No 'Serial Number' field:": {"Name": "noSerial", "Is Active": True, "Description": "noSerial"},
                      "No 'Is Active' field:": {"Name": "noActive", "Serial Number": 1, "Description": "noActive"},

                      "Wrong 'Name' field name:": {"name": "device_1", "Serial Number": 1, "Is Active": True},
                      "Wrong 'Serial Number' field name:": {"Name": "device_1", "serialNumber": 1, "Is Active": True},
                      "Wrong 'Is Active' field name:": {"Name": "device_1", "Serial Number": 1, "isActive": True},
                      "Wrong 'Description' field name:": {"Name": "device_1", "Serial Number": 1, "Is Active": True,
                                                          "description": "wrongDescription"},

                      "Wrong 'Name' type:": {"Name": 1, "Serial Number": 1, "Is Active": True, "Description": "abc"},
                      "Wrong 'Serial Number' type:": {"Name": "device_1", "Serial Number": "1", "Is Active": True,
                                                      "Description": "abc"},
                      "Wrong 'Is Active' type:": {"Name": "device_1", "Serial Number": 1, "Is Active": "True",
                                                  "Description": "abc"},
                      "Wrong 'Description' type:": {"Name": "device_1", "Serial Number": 1, "Is Active": True,
                                                    "Description": True},

                      "Serial Number already exist:": {"Name": "device_1", "Serial Number": 123, "Is Active": True},
                      "Empty request:": {}
                      }

invalid_get_arguments = {"Wrong argument field:": "?name=device_1",
                         "Two argument fields:": "?Name=device_1&?_id=1",
                         "Device ID does not exist:": "?_id=1",
                         "Device name does not exist:": "?Name=DoesNotExist",
                         "Database is empty:": "",
                         "Faulty request:": "ID="
                         }

invalid_put_jsons = {"No 'Name' field:": {"Serial Number": 1, "Is Active": True, "Description": "noName"},
                     "No 'Serial Number' field:": {"Name": "noSerial", "Is Active": True, "Description": "noSerial"},
                     "No 'Is Active' field:": {"Name": "noActive", "Serial Number": 1, "Description": "noActive"},

                     "Wrong 'Name' field name:": {"name": "device_1", "Serial Number": 1, "Is Active": True},
                     "Wrong 'Serial Number' field name:": {"Name": "device_1", "serialNumber": 1, "Is Active": True},
                     "Wrong 'Is Active' field name:": {"Name": "device_1", "Serial Number": 1, "isActive": True},
                     "Wrong 'Description' field name:": {"Name": "device_1", "Serial Number": 1, "Is Active": True,
                                                         "description": "wrongDescription"},

                     "Wrong 'Name' type:": {"Name": 1, "Serial Number": 1, "Is Active": True, "Description": "abc"},
                     "Wrong 'Serial Number' type:": {"Name": "device_1", "Serial Number": "1", "Is Active": True,
                                                     "Description": "abc"},
                     "Wrong 'Is Active' type:": {"Name": "device_1", "Serial Number": 1, "Is Active": "True",
                                                 "Description": "abc"},
                     "Wrong 'Description' type:": {"Name": "device_1", "Serial Number": 1, "Is Active": True,
                                                   "Description": True},

                     "Empty request:": {}
                     }

invalid_general_arguments = {"Wrong id field name:": "?ID=123",
                             "Device id doesnt exist:": "?_id=11111111",
                             "Empty request:": "",
                             "Faulty request:": "ID="
                             }
