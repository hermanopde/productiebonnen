from dotenv import load_dotenv, find_dotenv
import os
import requests
import sys
import time
from pymongo import MongoClient
from datetime import datetime

from bson.objectid import ObjectId

load_dotenv(find_dotenv())


api_key_ls = os.environ.get("API_KEY_LS")
api_secret_key_ls = os.environ.get("API_SECRET_KEY_LS")
password_mg_db = os.environ.get("MONGODB_PWD")


# connection_string = f"mongodb+srv://herman:{password}@production.4d02xna.mongodb.net/?retryWrites=true&w=majority"
connection_string = f"mongodb+srv://herman:{password_mg_db}@production.4d02xna.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(connection_string)
# dbs = client.list_database_names()
# print(dbs)
db = client.packinglist
products_collection = db.products

# FETCH PRODUCTS : 50 PRODUCTS PER PAGE


def fetch_products():

    url_ls_products = f"https://{api_key_ls}:{api_secret_key_ls}@api.webshopapp.com/nl/products.json?page=11"

    respons_lightspeed = requests.get(url_ls_products)
    data_lightspeed = respons_lightspeed.json()

    product_list = data_lightspeed["products"]

    products_list_for_db = []
    for product in product_list:
        product_for_db = {
            "id": product["id"],
            "visibility": product["visibility"],
            "machine1": "",
            "machine2": "",
            "data01": product["data01"],
            "data02": product["data02"],
            "title": product["title"],
            "fulltitle": product["fulltitle"],
            "variants": []
        }

        products_list_for_db.append(product_for_db)

    return products_list_for_db

# FETCH NIEUWE PRODUCTS


def fetch_new_products():
    # ZOEK HOOGSTE NUMMER
    product_found = products_collection.find().sort("id", -1).limit(1)
    for prod in product_found:
        hoogste_id = prod["id"]
        print(hoogste_id)

    url_ls_products_since = f"https://{api_key_ls}:{api_secret_key_ls}@api.webshopapp.com/nl/products.json?since_id={hoogste_id}"

    respons_lightspeed = requests.get(url_ls_products_since)
    data_lightspeed = respons_lightspeed.json()

    product_list_since = data_lightspeed["products"]

    if product_list_since != []:

        products_list_for_db = []
        for product in product_list_since:
            product_for_db = {
                "id": product["id"],
                "visibility": product["visibility"],
                "machine1": "",
                "machine2": "",
                "data01": product["data01"],
                "data02": product["data02"],
                "title": product["title"],
                "fulltitle": product["fulltitle"],
                "variants": []
            }

            products_list_for_db.append(product_for_db)
    else:
        products_list_for_db = []
    return products_list_for_db


# FETCH VARIABLES VAN PRODUCT ID
def fetch_variants(product):
    url_ls_variants = f"https://{api_key_ls}:{api_secret_key_ls}@api.webshopapp.com/nl/variants.json?product={product}"
    respons_lightspeed = requests.get(url_ls_variants)
    data_lightspeed = respons_lightspeed.json()

    variant_list = data_lightspeed["variants"]

    variant_list_for_db = []
    for variant in variant_list:
        variant_for_db = {
            "id": variant["id"],
            "articleCode": variant["articleCode"],
            "title": variant["title"],
            "ean": variant["ean"],
            "sku": variant["sku"],
            "magazijn": "",
            "priceExcl": variant["priceExcl"],
            "priceIncl": variant["priceIncl"],
            "oldPriceExcl": variant["oldPriceExcl"],
            "oldPriceIncl": variant["oldPriceIncl"],
            "priceCost": variant["priceCost"],
        }

        variant_list_for_db.append(variant_for_db)

    return variant_list_for_db

# FETCH AND SAVE PRODUCTS: 50 PER PAGE


def fetch_and_save_products():
    prods = fetch_products()
    for prod in prods:
        print(prod["id"])
        variants = fetch_variants(prod["id"])
        prod["variants"] = variants
        time.sleep(1)
    products_collection.insert_many(prods)

# FETCH AND SAVE NEW PRODUCTS


def fetch_and_save_new_products():
    prods = fetch_new_products()
    # print(prods)
    if prods != []:
        for prod in prods:
            print(prod["id"])
            variants = fetch_variants(prod["id"])
            prod["variants"] = variants
            time.sleep(1)
        products_collection.insert_many(prods)
    else:
        print("GEEN")


if __name__ == "__main__":
    print(__name__, ": VAN FETCH PRODUCTS")
    # fetch_and_save_products()
    # fetch_variants(130733819)
    # fetch_and_save_new_products()
