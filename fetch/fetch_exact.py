import requests
import json
from pymongo import MongoClient
from dotenv import dotenv_values
from bson.objectid import ObjectId

config = dotenv_values(".env")

password_mg_db = config["MONGODB_PWD"]
connection_string = f"mongodb+srv://herman:{password_mg_db}@production.4d02xna.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(connection_string)

db = client.packinglist
refresh_token_collection = db.exact_refresh
exact_products_collection = db.exact_producten

# EXACT
redirect_uri = config["REDIRECT_URI"]
client_id = config["CLIENT_ID"]
client_secret = config["CLIENT_SECRET"]


def request_new_token():
    db_resp = refresh_token_collection.find_one()
    refresh_token = db_resp["refresh_token"]
    url = "https://start.exactonline.be/api/oauth2/token"
    request_new_token = {"grant_type": "refresh_token", "client_id": client_id,
                         "client_secret": client_secret, "refresh_token": refresh_token}

    r = requests.post(url=url, data=request_new_token)
    print(r, 2)
    print(r.content, 2)
    exact_data = r.content
    dict = json.loads(exact_data)
    access_token = dict["access_token"]
    refresh_token = dict["refresh_token"]
    print(access_token, "-----", refresh_token)
    objInstance = ObjectId("64db069cb38e3e794271319b")
    refresh_token_collection.update_one(
        {"_id": objInstance}, {"$set": {"access_token": access_token, "refresh_token": refresh_token}})
    return "EXACT-API-GET NEW REFRESH TOKEN"


def request_division():
    db_resp = refresh_token_collection.find_one()
    access_token = db_resp["access_token"]

    url = "https://start.exactonline.be/api/v1/current/Me?$select=CurrentDivision"

    headers = {"authorization": f"Bearer {access_token}",
               "Content-Type": "application/json",
               "Accept": "application/json"}

    r = requests.get(url, headers=headers)
    print(r, 3)
    print(r.content, 3)
    exact_data = r.content
    dict = json.loads(exact_data)

    print("division is : ", dict)


def request_products():
    db_resp = refresh_token_collection.find_one()
    access_token = db_resp["access_token"]
    print(access_token)

    url = "https://start.exactonline.be/api/v1/183814/logistics/Items/?$select=ID,Code,Description,Modified,IsMakeItem,IsStockItem,IsWebshopItem,ItemGroup,ItemGroupCode,ItemGroupDescription"

    url_1 = "https://start.exactonline.be/api/v1/183814/logistics/Items"

    headers = {"authorization": f"Bearer {access_token}",
               "Content-Type": "application/json",
               "Accept": "application/json"}

    r = requests.get(url, headers=headers)
    print(r, 4)
    print(r.content, 4)
    exact_data = r.content
    dict = json.loads(exact_data)

    print("PRODUCTEN", dict)


# url_test = "https://prod.givanto.shop/exact-api/"
# url = "https://start.exactonline.be/api/oauth2/token"
#

if __name__ == "__main__":
    print(__name__, ": VAN FETCH EXACT")
    # request_new_token()
    # request_division()
    # request_products()
