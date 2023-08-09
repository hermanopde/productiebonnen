from dotenv import load_dotenv, find_dotenv
import os
import requests
import sys
import time

load_dotenv(find_dotenv())


api_key_ls = os.environ.get("API_KEY_LS")
api_secret_key_ls = os.environ.get("API_SECRET_KEY_LS")
password_mg_db = os.environ.get("MONGODB_PWD")


def hook_ls():
    url_ls = "http://127.0.0.1:5000/webhook_ls"

    respons = requests.get(url_ls)
    print(respons, "--------------------------------------")


hook_ls()
