"""
This file establishes a connection to the MongoDB database and creates references to the API database,
Devices collection, and Users collection.

* cluster: The MongoDB client connection to the database.
* db: The reference to the API database.
* devices: The reference to the Devices collection in the database.
* users: The reference to the Users collection in the database.
"""

from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://Elsight:12345@devices.46b9gn2.mongodb.net/?retryWrites=true&w=majority")
db = cluster["API"]
devices = db["Devices"]
users = db["Users"]


