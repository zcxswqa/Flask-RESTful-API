"""
This file is a menu based request sender to manually send requests to the api.
"""

import requests


def login():
    while True:
        print("Sign in or sign up?")
        print("1. Sign in.")
        print("2. Sign up")
        choice = input()
        if choice == "1":
            sign_in_username = input("Username:\n")
            sign_in_password = input("Password:\n")
            response = requests.get(Users, json={"Username": sign_in_username, "Password": sign_in_password})
            if response.status_code == 200:
                token = response.json()["token"]
                headers = {"Authorization": f"Bearer {token}"}
                print("\nHello " + sign_in_username + ", welcome back." + "\n")
                return headers
            else:
                print(response.json())

        elif choice == "2":
            sign_up_username = input("Choose a username (only letters and numbers are allowed):")
            sign_up_password = input("Choose a password (must contain at least 8 characters):")
            response = requests.post(Users, json={"Username": sign_up_username, "Password": sign_up_password})
            print(response.json())
        else:
            print("\nInvalid input, try again...\n")


def menu():
    headers = login()
    while True:
        print("What would you like to do?")
        print("1. Insert a new device.")
        print("2. Get a device.")
        print("3. Update a device by ID.")
        print("4. Delete a device by ID.")
        print("5. Log out.")
        choice = input()
        if choice == "1":
            name = input("What is the device name?\n")
            serial = input("What is the device serial number?\n")
            print("Is the device active?")
            print("1. Yes.")
            print("2. No.")
            active = input()
            description = input("What is device description?\n")
            if active == "1":
                active = True
            elif active == "0":
                active = False
            else:
                print("\nDevice activation status is illegal.\n")
                continue
            package = {"Name": name, "Serial Number": int(serial), "Is Active": active, "Description": description}
            response = requests.post(Devices, json=package, headers=headers)
            print(response.json())
        elif choice == "2":
            print("One device by name, by ID or all devices?")
            print("1. Name.")
            print("2. ID.")
            print("3. All.")
            choice = input()
            if choice == "1":
                name = input("What is device name?\n")
                response = requests.get(Devices + "?Name=" + name, headers=headers)
                if len(response.json()) == 1:
                    print(response.json())
                else:
                    for i in response.json():
                        print(i)
            elif choice == "2":
                id = input("What is device ID?\n")
                response = requests.get(Devices + "?_id=" + id, headers=headers)
                print(response.json())
            elif choice == "3":
                response = requests.get(Devices, headers=headers)
                if len(response.json()) == 1:
                    print(response.json())
                else:
                    for i in response.json():
                        print(i)
            else:
                print("\nInvalid input, try again...\n")
        elif choice == "3":
            id = input("Please insert an ID of device for updating:\n")
            name = input("Please insert the new device name:\n")
            serial = input("Please insert new device serial number:\n")
            active = input("Is the device active? 1=YES, 0=NO\n")
            description = input("What is device description?\n")
            if active == "1":
                active = True
            elif active == "0":
                active = False
            else:
                print("\nDevice activation status is illegal.\n")
            package = {"Name": name, "Serial Number": int(serial), "Is Active": active, "Description": description}
            response = requests.put(Devices + "?_id=" + id, json=package, headers=headers)
            print(response.json())
        elif choice == "4":
            id = input("Please insert an ID of device for deletion:\n")
            response = requests.delete(Devices + "?_id=" + id, headers=headers)
            print(response.json())
        elif choice == "5":
            print("\nGoodbye!\n\n")
            headers = login()


Devices = "http://127.0.0.1:5000/Api/V1/Devices/"
Users = "http://127.0.0.1:5000/Api/V1/Authentication/"

menu()
