from dotenv import load_dotenv, find_dotenv
import os
import requests
import sys
import time
from pymongo import MongoClient
from datetime import datetime

from bson.objectid import ObjectId
# print(sys.path)

load_dotenv(find_dotenv())


api_key_ls = os.environ.get("API_KEY_LS")
api_secret_key_ls = os.environ.get("API_SECRET_KEY_LS")
password_mg_db = os.environ.get("MONGODB_PWD")

NUMBER_OF_ORDERS_TO_KEEP = 2000

# connection_string = f"mongodb+srv://herman:{password}@production.4d02xna.mongodb.net/?retryWrites=true&w=majority"
connection_string = f"mongodb+srv://herman:{password_mg_db}@production.4d02xna.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(connection_string)
# dbs = client.list_database_names()
# print(dbs)
db = client.packinglist
order_collection = db.lsorders
last_order_collection = db.lastorder
exact_products_collection = db.exact_producten


def undo_flag_printed(van, tot):
    list = []
    for x in range(van, tot+1):
        list.append(x)
    print(list)

    for order in list:
        order_collection.update_one({"number": order}, {
            "$set": {"flagPrinted": False}})


def find_ordeders_test():
    gevonden_orders = order_collection.find({"$and": [{"flagPrinted": False}, {"$or": [
        {"status": "processing_awaiting_shipment"}, {"status": "processing_awaiting_pickup"}]}]}).sort("paid_created_at", -1).limit(10)
    print(gevonden_orders)


if __name__ == "__main__":
    # undo_flag_printed(355231, 355245)
    find_ordeders_test()

    print("FLAG")
