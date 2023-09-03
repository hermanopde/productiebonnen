# pip install opencv-python, pip install pyzbar, pip install python-barcode
from barcode.writer import ImageWriter
import time
import json
import cv2  # read img  camara/video import
from pyzbar.pyzbar import decode
import webbrowser
from barcode import EAN13, Code128
from dotenv import dotenv_values

import requests
import sys
import time
from pymongo import MongoClient
from datetime import datetime

from bson.objectid import ObjectId
# print(sys.path)

config = dotenv_values(".env")


api_key_ls = config["API_KEY_LS"]
api_secret_key_ls = config["API_SECRET_KEY_LS"]


def scan_open():
    while True:
        id = input("geef nr : ")
        print(id)
        url = f"https://brianto.webshopapp.com/admin/orders/{id}"
        webbrowser.open(url)
        time.sleep(30)


# -----------------------------------------------
# # CREATE PNG  BARCODE
# order_id = str(256776)
# my_code = Code128(order_id, writer=ImageWriter())
# my_code.save(f"./prints/BC-{order_id}")

# # READ BARCODE FROM IMAGE
# img = cv2.imread(f"./prints/BC-{order_id}.png")
# resp = decode(img)  # r is a list
# barcode_type = resp[0].type
# barcode_data = resp[0].data  # returns a b' (byte) string
# print(barcode_type)
# print(barcode_data)
# print(barcode_data.decode("utf-8"))

# IN CASE OF MORE CODES IN IMAGE

# for r in resp:
#     print(r.type)
#     print(r.data)
#     print(r.data.decode("utf-8"))

# -----------------------------------------------
# # FROM CCAMERA

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(3, 640)  # 3 = width 640 px
# cap.set(4, 480)  # 4 = height 480 px

# camera = True
# while camera == True:  # camera is continuous scan
#     success, frame = cap.read()

#     for code in decode(frame):
#         print(code.type)
#         print(code.data)
#         order = code.data
#         time.sleep(2)

#     cv2.imshow('Testing-code-scan', frame)
#     cv2.waitKey(1)  # 1 milliesec

# --------------------------------------------

# OPEN WEBBROWSER FROM LINK
url = "https://brianto.webshopapp.com/admin/orders/252285050"
url = "https://brianto.webshopapp.com/admin/orders/252282009"
# webbrowser.open_new(url)
# webbrowser.open(url)

# ORDERS
# https://brianto.webshopapp.com/admin/orders/252523566


def get_shipping_id(order_id):
    url = f"https://{api_key_ls}:{api_secret_key_ls}@api.webshopapp.com/nl/shipments.json?order={order_id}"

    r = requests.get(url=url)
    r_json = r.json()
    shipments_id = r_json["shipments"][0]["id"]
    print(shipments_id)


def get_shipment(shipment_id):
    url = f"https://{api_key_ls}:{api_secret_key_ls}@api.webshopapp.com/nl/shipments/{shipment_id}.json"
    r = requests.get(url=url)
    r_json = r.json()
    print(r_json)


# ETIKETTEN KNOP
# https://brianto.webshopapp.com/admin/orders/252523566/shipments/244458532/label?force_new=true

# get_shipping_id(252583624)
if __name__ == "__main__":

    scan_open()
