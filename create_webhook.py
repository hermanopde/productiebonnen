import requests
from dotenv import dotenv_values
import json

config = dotenv_values(".env")

api_key_ls = config["API_KEY_LS"]
api_secret_key_ls = config["API_SECRET_KEY_LS"]
cluster_id = config["CLUSTER_ID"]

print(api_key_ls, "---------", api_secret_key_ls, "------", cluster_id)

resp_url = "https://prod.givanto.shop/webhook-ls/"
url_1 = "http://127.0.0.1:5000/webhook-ls/"


url = f"https://{api_key_ls}:{api_secret_key_ls}@api.webshopapp.com/nl/webhooks.json"


payload_auth = {
    "webhook": {

        "isActive": True,
        "itemGroup": "orders",
        "itemAction": "*",
        "language": "en",
        "format": "json",
        "address": "https://prod.givanto.shop/webhook-ls/"
    }
}


r = requests.post(url, data=json.dumps(payload_auth))
print(r, "from create : 1")
print(r.content, "from create : 2")
