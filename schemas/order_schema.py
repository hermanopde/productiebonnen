from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import sys
from datetime import datetime as dt
import time

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://herman:{password}@production.4d02xna.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(connection_string)
printer = pprint.PrettyPrinter()


packinglist_db = client.packinglist
# lsorders = packinglist_db.lsorders
order_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Orders Object Validation",
        "required": ["number", "email",],
        "properties": {
            "name": {
                "bsonType": "string",

                "description": "'name' must be a string and is required"
            },
            "year": {
                "bsonType": "int",
                "minimum": 2017,
                "maximum": 3017,
                "description": "'year' must be an integer in [ 2017, 3017 ] and is required"
            },
            "gpa": {
                "bsonType": ["double"],
                "description": "'gpa' must be a double if the field exists"
            },
            "number": {
                "bsonType": "int",
            },
            "email": {
                "bsonType": "string",

            },
        }
    }
}

# try:
#     packinglist_db.create_collection("test_orders",)
# except Exception as e:
#     print(e)

# packinglist_db.command("collMod", "test_orders", validator=order_validator)


def insert_test_order(order):
    try:
        test_order_collection = packinglist_db.test_orders
        id = test_order_collection.insert_one(order).inserted_id
        print(id)
    except Exception as e:
        print("iets niet goed")
        print(e)


order_1 = {
    "name": "order5",
    "year": 2023,
    "number": 346505,
    "email": "werre@",
    "gpa": 3.6,


}

insert_test_order(order_1)

# print(dt.today().day, dt.today().month, dt.today().year, dt.today().minute)
# time.sleep(3)
# print(dt.today().day, dt.today().month, dt.today().year, dt.today().minute)
