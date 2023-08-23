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


def order_for_db_dict(order, paid_date):

    order_for_db = {
        "id": order["id"],
        "created_at": order["createdAt"],
        "paid_created_at": paid_date,
        "shipped_created_at": "",
        "number": int(order["number"]),
        "status": order["status"],
        "email": order["email"],
        "priceExcl": order["priceExcl"],
        "priceIncl": order["priceIncl"],
        "firstname": order["firstname"],
        "lastname": order["lastname"],
        "mobile": order["mobile"],

        "companyName": order["companyName"],
        "companyVatNumber": order["companyVatNumber"],
        "addressBillingName": order["addressBillingName"],
        "addressBillingStreet": order["addressBillingStreet"],
        "addressBillingNumber": order["addressBillingNumber"],
        "addressBillingExtension": order["addressBillingExtension"],
        "addressBillingZipcode": order["addressBillingZipcode"],
        "addressBillingCity": order["addressBillingCity"],
        "addressBillingCountry": order["addressBillingCountry"]["title"],

        "addressShippingCompany": order["addressShippingCompany"],
        "addressShippingName": order["addressShippingName"],
        "addressShippingStreet": order["addressShippingStreet"],
        "addressShippingNumber": order["addressShippingNumber"],
        "addressShippingExtension": order["addressShippingExtension"],
        "addressShippingZipcode": order["addressShippingZipcode"],
        "addressShippingCity": order["addressShippingCity"],
        "addressShippingCountry": order["addressShippingCountry"]["title"],

        "shipmentTitle": order["shipmentTitle"],
        "comment": order["comment"],

        "flagPrinted": False,
        "flagCustomDownloaded": False,
        "products": [],
        "orderNumberExact": "",
    }

    product_list = order["products"]["resource"]["embedded"]

    product_list_for_db = []

    for prod in product_list:
        product = {
            "articleCode": prod["articleCode"],
            "productTitle": prod["productTitle"],
            "variantTitle": prod["variantTitle"],
            "quantityOrdered": prod["quantityOrdered"],
            "priceExcl": prod["priceExcl"],
            "priceIncl": prod["priceIncl"],
            "customizationString": "",
            "customizationId": "",
            "customizationToken": "",
            "pdfFileName": "",
            "jpgFileName": "",
            "magazijnPositie": "",
            "productie_inst_1": "",
            "productie_inst_2": "",
        }

        if prod["customFields"] != False:

            for field in prod["customFields"]:
                if "id" in field.values() and field["values"][0]["value"] != False and field["values"][0]["value"] != None:
                    product["customizationString"] = field["values"][0]["value"]
                    product["customizationId"] = product["customizationString"].split(".")[
                        0]
                    product["customizationToken"] = product["customizationString"].split(".")[
                        1]
                    formatted_1 = product["productTitle"].replace(" ", "-")
                    formatted_product_title = formatted_1.replace("'", "-")

                    product["pdfFileName"] = f"{order['number']}-{product['customizationId']}-{formatted_product_title}.pdf"
                    product["jpgFileName"] = f"{order['number']}-{product['customizationId']}-{formatted_product_title}.jpg"

        product_list_for_db.append(product)

    order_for_db["products"] = product_list_for_db

    return order_for_db


def remove_old_orders(num):
    order_collection.delete_many({"number": {"$lte": num}})


def save_order_in_db(order, paid_date):
    new_last_order = order["id"]
    new_last_order_number = int(order["number"])
    objInstance = ObjectId("644cd093f9bc46bd8da4f580")
    # last_order_collection.update_one(
    #     {"_id": objInstance}, {"$set": {"lastOrder": new_last_order}})

    order_for_db = order_for_db_dict(order, paid_date)
    order_collection.insert_one(order_for_db)

    # remove_old_orders(new_last_order_number-NUMBER_OF_ORDERS_TO_KEEP)

    print("SAVED TO DB", "new last order =", new_last_order)

# UPDATE ORDER SHIPPED OR CANCELLED


def update_order_shipped(order, shipping_date):
    order_number = int(order["number"])
    new_status = order["status"]

    shipped = shipping_date
    print(order_number, new_status, shipped, 3)

    # order_collection.update_one({"number": order_number}, {
    #                             "$set": [{"shipped_created_at": shipped}, {"status": new_status}]})
    # order_collection.update_one({"number": order_number}, {"$set": {"shipped_created_at": shipped}, "$set": {"status": new_status}})

    order_collection.update_one({"number": order_number}, {
                                "$set": {"shipped_created_at": shipped, "status": new_status}})


def update_order_paid(order, paid_date):
    order_number = int(order["number"])
    new_status = order["status"]

    paid = paid_date
    print(order_number, new_status, paid, 4)

    # order_collection.update_one({"number": order_number}, {
    #                             "$set": [{"shipped_created_at": shipped}, {"status": new_status}]})
    # order_collection.update_one({"number": order_number}, {"$set": {"shipped_created_at": shipped}, "$set": {"status": new_status}})

    order_collection.update_one({"number": order_number}, {
                                "$set": {"paid_created_at": paid, "status": new_status}})


if __name__ == "__main__":
    print(__name__, ": VAN FETCH LIFGTSPEED")
    # fetch_and_save_lsorders(last_order)
