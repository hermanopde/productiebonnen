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

# //--------------GET ORDERS LiMIT FROM LIGHTSPEED------------
# https://94a9144f0045ad47828370f2377913da:f51b1ad465c34d47a3b984cf9bb192e8@api.webshopapp.com/nl/orders.json?limit=1


# //--------------GET ORDERS SINCE LAST ORDER FROM LIGHTSPEED------------


def fetch_orders_since(last_order):
    url_ls_since = f"https://{api_key_ls}:{api_secret_key_ls}@api.webshopapp.com/nl/orders.json?since_id={last_order}"

    respons_lightspeed = requests.get(url_ls_since)
    data_lightspeed = respons_lightspeed.json()

    orders_list = data_lightspeed["orders"]

    order_list_for_db = []
    for order in orders_list:
        order_for_db = {
            "id": order["id"],
            "created_at": order["createdAt"],
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
        order_list_for_db.append(order_for_db)
        # print(order_for_db["number"],
        #       order_for_db["shipmentTitle"], order_for_db["comment"])

    return order_list_for_db


# //--------------GET PRODUCTS FROM ORDER LIGHTSPEED------------


def fetch_products_from_order(order_id, order_number):
    url_products = f"https://{api_key_ls}:{api_secret_key_ls}@api.webshopapp.com/nl/orders/{order_id}/products.json"
    respons_products_orders = requests.get(url_products)
    order_products = respons_products_orders.json()
    product_list = order_products["orderProducts"]

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

                    product["pdfFileName"] = f"{order_number}-{product['customizationId']}-{formatted_product_title}.pdf"
                    product["jpgFileName"] = f"{order_number}-{product['customizationId']}-{formatted_product_title}.jpg"

        product_list_for_db.append(product)
        # product_list_for_db.append({"naam": "joske", "beroep": "werker"})

    return product_list_for_db


def remove_old_orders(num):
    order_collection.delete_many({"number": {"$lte": num}})


def add_products_to_orders(orders):
    for order in orders:
        order_id = order["id"]
        order_number = order["number"]
        product_list = fetch_products_from_order(order_id, order_number)
        time.sleep(2)
        for product in product_list:
            order["products"].append(product)

    return orders


def fetch_last_order():

    last_order_object = last_order_collection.find_one()
    last_order_id = last_order_object["lastOrder"]
    return last_order_id


def fetch_and_save_lsorders(last_order_id):
    lightspeed_order_list = fetch_orders_since(last_order_id)
    orders_ready_for_db = add_products_to_orders(lightspeed_order_list)
    if orders_ready_for_db != []:
        order_collection.insert_many(orders_ready_for_db)
        new_last_order = orders_ready_for_db[0]["id"]
        new_last_order_number = int(orders_ready_for_db[0]["number"])
        objInstance = ObjectId("644cd093f9bc46bd8da4f580")
        last_order_collection.update_one(
            {"_id": objInstance}, {"$set": {"lastOrder": new_last_order}})

        remove_old_orders(new_last_order_number-NUMBER_OF_ORDERS_TO_KEEP)

        print("SAVED TO DB", "new last order =", new_last_order)

    else:
        print("GEEN NIEUWE ORDERS", datetime.now())


if __name__ == "__main__":
    print(__name__, ": VAN FETCH LIFGTSPEED")
    # fetch_and_save_lsorders(last_order)


# printer = pprint.PrettyPrinter()

# @app.get("/test/")
# def get_query_params():
#     # print(dir(request))
#     respons_1 = request.query_string
#     respons_2 = request.args.get("a")

#     print(respons_1, respons_2, "gggg")
#     return " wat is me da na"

# @app.route("/form", )
# def form():
#     return render_template("form.html")

# @app.route("/klantenzone", methods=["post"])
# # @app.post("/page")
# def get_fotm_data():
#     first_name = request.form.get("fname")
#     last_name = request.form.get("lname")
#     if first_name != "herman":
#         print(first_name, last_name)
#         return redirect(url_for("geen_toegang", naam=first_name))

#     else:
#         print(first_name, last_name)
#         return f"van form page ontvangen, WELKOM {first_name}"

# @app.route("/<naam>")
# def geen_toegang(naam):
#     return f"u heeft geen toegang, registreer eerst   {naam} "

# if __name__ == "__main__":
#     app.run(debug=True)


# };

# //--------------GET ORDERS SINCE LAST ORDER FROM LIGHTSPEED------------
# const getOrdersSince = async function (lastOrder) {
#   const result = await axios.get(
#     `https://${process.env.API_KEY_LS}:${process.env.API_SECRET_KEY_LS}@api.webshopapp.com/nl/orders.json?since_id=${lastOrder}`
#   );
#   const orderDataLs = result.data.orders;

#   return orderDataLs;
# };


# //--------------GET EVENTS VAN ORDERS UNPAID - CHECK NEW PAYMENTS------------
# const getEventsFromOrder = async function (order) {
#   const result = await axios.get(
#     `https://${process.env.API_KEY_LS}:${process.env.API_SECRET_KEY_LS}@api.webshopapp.com/nl/orders/events.json?order=${order}`
#   );
#   //const EventdataLs = result.data.ordersEvents;
#   //console.log(dataLs);
#   //return EventdataLs;
#   return result.data.ordersEvents;
# };
