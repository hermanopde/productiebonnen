from pymongo import MongoClient
from dotenv import dotenv_values
from passlib.hash import pbkdf2_sha256
import copy
import requests
import json
from bson.objectid import ObjectId
from flask import Flask, redirect, url_for, render_template, request, session, flash, abort
from routes import order_pages, user_pages
from fetch import fetch_and_save_lsorders, fetch_last_order, get_customization, save_order_in_db, update_order_shipped, update_order_paid
import time
from datetime import datetime, timedelta
from fpdf import FPDF
from create_pdf import create_orderbonnen
import pandas as pd
# from pandas import *
import math


config = dotenv_values(".env")


password_mg_db = config["MONGODB_PWD"]
connection_string = f"mongodb+srv://herman:{password_mg_db}@production.4d02xna.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(connection_string)
db = client.packinglist


orders_collection = db.lsorders

exact_products_collection = db.exact_producten


def exact_products_to_db():
    # read excelfile in dict
    df = pd.read_excel("LogItems_test.xlsx")
    dict = df.to_dict()

    # xls = ExcelFile('LogItems_test.xlsx')
    # data = xls.parse(xls.sheet_names[0])
    # print(data.to_dict())
    # loop over dict
    # update products
    for key, value in dict["Code"].items():
        art_number = str(value)
        print(art_number)
        # STR TO HAndle nan
        mach_1 = str(dict["Productie Instellingen"][key])
        mach_2 = str(dict["X252"][key])

        if mach_1 == "nan":
            mach_1 = ""
        if mach_2 == "nan":
            mach_2 = ""
        product = {"article": art_number,
                   "machine1": mach_1, "machine2": mach_2}

        # products_collection.update_one({"number": order_number}, {
        #     "$set": {"shipped_created_at": shipped, "status": new_status}})

        exact_products_collection.insert_one(product)
        time.sleep(1)


def get_machine_inst(article):
    r = exact_products_collection.find_one({"article": article})
    return r


if __name__ == "__main__":
    print(__name__, ": VAN EAXCT_PRODUCTS.PY")
    # exact_products_to_db()
    a = get_machine_inst("1000000")
    print(a)
