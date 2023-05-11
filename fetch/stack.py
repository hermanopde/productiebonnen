import requests
from dotenv import dotenv_values
import json
import time
config = dotenv_values(".env")

stack_password = config["STACK_WW"]
stack_user_name = config["STACK_USER_NAME"]


def stack_auth():
    STACK_URL_AUTH = "https://brianto.stack.storage/api/v2/authenticate"
    payload_auth = {
        "username": stack_user_name,
        "password": stack_password,
        "sessionDuration": 3600
    }

    respons_auth = requests.post(
        STACK_URL_AUTH, data=json.dumps(payload_auth))  # werkt
    auth_status_code = respons_auth.status_code

    x_session_token = respons_auth.headers['X-Sessiontoken']
    x_csrf_token = respons_auth.headers['X-Csrf-Token']

    return {"x_session_token": x_session_token, "x_csrf_token": x_csrf_token, "auth_status_code": auth_status_code}


# customzation node : {"id":214929,"name":"Customizations","path":"files/Customizations"}

# time.sleep(3)

STACK_URL_NODES = "https://brianto.stack.storage/api/v2/nodes"

x_session_token = 'FT3HU14EsoHCmRhnfaocTlBd_mI'
x_csrf_token = '0KVFqJfA9DoWl1Vy8LQ'


# payload_nodes = {

#     "X-SessionToken": x_session_token,
#     "X-Csrf-Token": x_csrf_token}


# respons_nodes = requests.get(STACK_URL_NODES, headers=payload_nodes)  # : werkt
# print(respons_nodes.status_code)
# print(respons_nodes.content)


# respons = requests.get(STACK_URL_2, data=json.dumps(payload))
# print(respons.content)
