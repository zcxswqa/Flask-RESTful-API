"""
This file is a menu based tester, it includes functions for testing some invalid requests.
"""

import requests

from tests_scenarios import *

Devices = "http://127.0.0.1:5000/Api/V1/Devices/"
Users = "http://127.0.0.1:5000/Api/V1/Authentication/"


def testings():
    headers = generate_testing_headers()
    if not headers:
        print("An unexpected error has occurred when trying to create a testing user. please try again.")
        return
    delete_all_devices(headers)
    choice = None
    while choice != "8":
        print("\n\n\nWhat would you like to do?")
        print("1. Run all tests.")
        print("2. Run users signup tests.")
        print("3. Run users signin tests.")
        print("4. Run devices POST tests.")
        print("5. Run devices GET tests.")
        print("6. Run devices PUT tests.")
        print("7. Run devices DELETE tests.")
        print("8. Exit.")
        choice = input()
        if choice == "1":
            signup_tests()

            signin_tests()

            device_post_tests(headers)
            delete_all_devices(headers)

            device_get_tests(headers)

            device_put_tests(headers)
            delete_all_devices(headers)

            device_delete_tests(headers)

        elif choice == "2":
            signup_tests()

        elif choice == "3":
            signin_tests()

        elif choice == "4":
            device_post_tests(headers)
            delete_all_devices(headers)

        elif choice == "5":
            device_get_tests(headers)

        elif choice == "6":
            device_put_tests(headers)
            delete_all_devices(headers)

        elif choice == "7":
            device_delete_tests(headers)

        elif choice == "8":
            print("Goodbye.")

        else:
            print("\nInvalid input, try again...\n")


def menu():
    choice = None
    while choice != "2":
        print("\n\n\nSTARTING AUTOMATED TESTINGS WILL REMOVE ALL DATA IN THE DATABASE, are you sure?")
        print("1. Yes.")
        print("2. No.")
        choice = input()
        if choice == "1":
            testings()

        elif choice == "2":
            print("Goodbye.")
            return

        else:
            print("\nInvalid input, try again...\n")


def generate_testing_headers():
    print("\n\n\nGenerating a user for testing...")
    testing_user = {"Username": "testing", "Password": "test1234"}
    requests.post(Users, json=testing_user)

    response = requests.get(Users, json=testing_user)
    if response.status_code == 200:
        token = response.json()["token"]
        testing_headers = {"Authorization": f"Bearer {token}"}
    else:
        print(response.json())
        testing_headers = None
    return testing_headers


def delete_all_devices(testing_headers):
    print("\n\n\nDeleting all devices from database...")
    response = requests.get(Devices, headers=testing_headers)
    if response.status_code != 200:
        print(response.json())
    for device in response.json():
        if type(device) is dict:
            delete = requests.delete(Devices + "?_id=" + device["_id"], headers=testing_headers)
            if delete.status_code != 200:
                print(response.json())


def signup_tests():
    print("\n\n\nRunning signup tests...\n")
    for scenario in invalid_signup_jsons.keys():
        print(scenario)
        response = requests.post(Users, json=invalid_signup_jsons[scenario])
        print(response.json())
        print()


def signin_tests():
    print("\n\n\nRunning signin tests...\n")
    for scenario in invalid_signin_jsons.keys():
        print(scenario)
        response = requests.get(Users, json=invalid_signin_jsons[scenario])
        print(response.json())
        print()


def device_post_tests(testing_headers):
    requests.post(Devices, json={"Name": "testing", "Serial Number": 123, "Is Active": True},
                  headers=testing_headers)

    print("\n\n\nRunning POST tests...\n")
    for scenario in invalid_post_jsons.keys():
        print(scenario)
        response = requests.post(Devices, json=invalid_post_jsons[scenario], headers=testing_headers)
        print(response.json())
        print()

    for scenario in invalid_headers.keys():
        print(scenario)
        response = requests.post(Devices, json=valid_json, headers=invalid_headers[scenario])
        print(response.json())
        print()


def device_get_tests(testing_headers):
    print("\n\n\nRunning GET tests...\n")
    for scenario in invalid_get_arguments.keys():
        print(scenario)
        response = requests.get(Devices + invalid_get_arguments[scenario], headers=testing_headers)
        if len(response.json()) == 1:
            print(response.json())
        else:
            for i in response.json():
                print(i)
        print()

    for scenario in invalid_headers.keys():
        print(scenario)
        response = requests.get(Devices, json=valid_json, headers=invalid_headers[scenario])
        print(response.json())
        print()


def device_put_tests(testing_headers):
    requests.post(Devices, json={"Name": "testing", "Serial Number": 123456789, "Is Active": True},
                  headers=testing_headers)
    response = requests.get(Devices + "?Name=testing", headers=testing_headers)
    testing_device = response.json()[0]

    print("\n\n\nRunning PUT tests...\n")
    for scenario in invalid_put_jsons.keys():
        print(scenario)
        response = requests.put(Devices + "?_id=" + testing_device["_id"], json=invalid_put_jsons[scenario],
                                headers=testing_headers)
        print(response.json())
        print()

    for scenario in invalid_general_arguments.keys():
        print(scenario)
        response = requests.put(Devices + invalid_general_arguments[scenario], json=valid_json, headers=testing_headers)
        print(response.json())
        print()

    for scenario in invalid_headers.keys():
        print(scenario)
        response = requests.put(Devices, json=valid_json, headers=invalid_headers[scenario])
        print(response.json())
        print()


def device_delete_tests(testing_headers):
    print("\n\n\nRunning DELETE tests...\n")
    for scenario in invalid_general_arguments:
        print(scenario)
        response = requests.delete(Devices + invalid_general_arguments[scenario], headers=testing_headers)
        print(response.json())
        print()

    for scenario in invalid_headers.keys():
        print(scenario)
        response = requests.delete(Devices, json=valid_json, headers=invalid_headers[scenario])
        print(response.json())
        print()


menu()
