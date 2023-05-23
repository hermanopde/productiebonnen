import requests
from dotenv import dotenv_values
import json
import time
import hashlib
import hmac
config = dotenv_values(".env")

stack_password = config["STACK_WW"]
stack_user_name = config["STACK_USER_NAME"]

COLORLAB_SHOP_ID = config["COLORLAB_SHOP_ID"]
COLORLAB_API_KEY = config["COLORLAB_API_KEY"]
COLORLAB_API_SECRET = config["COLORLAB_API_SECRET"]


def stack_auth():
    STACK_URL_AUTH = "https://brianto.stack.storage/api/v2/authenticate"
    # STACK_URL_AUTH = "http://httpbin.org/post"
    payload_auth = {
        "username": stack_user_name,
        "password": stack_password,
        "sessionDuration": 600
    }

    respons_auth = requests.post(
        STACK_URL_AUTH, data=json.dumps(payload_auth))  # data=json.dumps(payload_auth)
    auth_status_code = respons_auth.status_code

    x_session_token = respons_auth.headers['X-Sessiontoken']
    x_csrf_token = respons_auth.headers['X-Csrf-Token']

    f_res = {"x_session_token": x_session_token,
             "x_csrf_token": x_csrf_token, "auth_status_code": auth_status_code}
    print(f_res)
    return f_res


def get_nodes():
    auth_params = stack_auth()
    time.sleep(3)

    STACK_URL_NODES = "https://brianto.stack.storage/api/v2/nodes"

    x_session_token = auth_params["x_session_token"]
    x_csrf_token = auth_params["x_csrf_token"]
    payload_nodes = {"X-SessionToken": x_session_token,
                     "X-Csrf-Token": x_csrf_token}

    respons_nodes = requests.get(
        STACK_URL_NODES, headers=payload_nodes)
    print(respons_nodes.status_code)
    print(respons_nodes.content)


def upload_custom():
    auth_params = stack_auth()
    time.sleep(3)

    STACK_URL_UPLOAD = "https://brianto.stack.storage/api/v2/upload"
    # STACK_URL_UPLOAD = "http://httpbin.org/post"
    x_session_token = auth_params["x_session_token"]
    x_csrf_token = auth_params["x_csrf_token"]
    values = {"X-FileByteSize": 483397,
              "X-ParentID": 55722, "X-Filename": "perre.pdf"}
    headers = {"X-SessionToken": x_session_token,
               "X-Csrf-Token": x_csrf_token, "X-FileByteSize": "483397",
               "X-ParentID": "55722", "X-Filename": "perre.pdf", "Content-Type": "application/json"
               }
    # files = {"X-Filename": file_to_upload,
    #          'content-type': 'application/json'}
    with open("joske.txt", "rb") as fff:
        r = requests.post(
            STACK_URL_UPLOAD, headers=headers,  files={"file": fff})
        print(r.status_code)

        print("BODY", r.request.body)
        print("HEDDERS", r.request.headers)
        print("PATH", r.request.path_url)

# files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}


# upload_custom()

# r = requests.get("https://imgs.xkcd.com/comics/python.png")
# print(r.content)

# with open("joske.png", "wb") as f:
#     f.write(r.content)

if __name__ == "__main__":
    pass


# def color():
#     verificationString = COLORLAB_SHOP_ID + \
#         "271557e524785a-a114-41fc-a307-309dad599a09"

#     hash = hmac.new(COLORLAB_API_SECRET.encode('utf-8'), verificationString.encode(
#         'utf-8'), hashlib.sha256).hexdigest()

#     colorlab_url = f"https://api.colorlab.io/v1/configuration/271557/e524785a-a114-41fc-a307-309dad599a09/export"

#     headers = {"content-Type": "application/pdf", "X-Colorlab-Shop": COLORLAB_SHOP_ID,
#                "X-Colorlab-Api-Key": COLORLAB_API_KEY, "X-Colorlab-Api-Signature": hash}
#     response = requests.get(url=colorlab_url, headers=headers)
#     customization_file = response.content

#     file_size = response.headers["Content-Length"]
#     file_size_b = int(file_size)
#     file_alt = response.headers["Alt-Svc"]
#     # print(file_size)
#     return {"customization_file": customization_file, "file_size": file_size_b}
