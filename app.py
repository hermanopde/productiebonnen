from pymongo import MongoClient
from dotenv import dotenv_values
from passlib.hash import pbkdf2_sha256
import copy
import requests

from flask import Flask, redirect, url_for, render_template, request, session, flash, abort
from routes import order_pages, user_pages
from fetch import fetch_and_save_lsorders, fetch_last_order, get_customization
import time
from datetime import datetime, timedelta
from fpdf import FPDF
from create_pdf import create_orderbonnen
from forms import LoginForm, SearchField


config = dotenv_values(".env")

year = datetime.now().year
app = Flask(__name__)

app.secret_key = config["APP_SECRET_KEY"]

app.permanent_session_lifetime = timedelta(minutes=60)


password_mg_db = config["MONGODB_PWD"]
connection_string = f"mongodb+srv://herman:{password_mg_db}@production.4d02xna.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(connection_string)
db = client.packinglist

user_collection = db.users
orders_collection = db.lsorders
last_order_collection = db.lastorder


app.register_blueprint(order_pages, url_prefix="/production")
app.register_blueprint(user_pages, url_prefix="/auth")


def format_date(str):
    date_format = '%Y-%m-%dT%H:%M:%S+02:00'
    formatted_date = datetime.strptime(
        str, date_format).strftime("%d-%m-%Y %H:%M")
    return formatted_date


def format_date_v_2(str):
    date_format = '%Y-%m-%dT%H:%M:%S+02:00'
    formatted_date = datetime.strptime(
        str, date_format).strftime("%d-%m-%Y")
    return formatted_date


def format_date_now():
    if datetime.today().day < 10:
        dag = f"0{datetime.today().day}"
    else:
        dag = datetime.today().day

    dd_now = f"{dag}-{datetime.today().month}-{datetime.today().year}-{datetime.today().hour}h{datetime.today().minute}m"
    return dd_now


def format_status(status):
    if status == "processing_awaiting_shipment":
        return "klaar voor verzending"
    if status == "processing_awaiting_payment":
        return "wacht op betaling"
    if status == "processing_awaiting_pickup":
        return "klaar voor afhaling"
    if status == "cancelled":
        return "cancelled"
    else:
        return "onbekend"


TEMPLATE_LIMIT = 200


@app.route("/")
def home():
    return redirect(url_for("orders"))


# HTML LOGIN FORM

# @app.route("/login/", methods=["POST", "GET"])
# def login():
#     if request.method == "POST":
#         user = request.form.get("email")
#         password = request.form.get("password")
#         user_check = user_collection.find_one({"user": user})
#         if user_check:
#             if pbkdf2_sha256.verify(password, user_check["hpw"]):
#                 session["email"] = user
#                 return redirect(url_for("orders"))

#         return render_template("login_fout.html")

#     else:
#         # session.clear()
#         return render_template("login.html")


# WTF-FLASK LOGIN FORM

@app.route("/login/", methods=["POST", "GET"])
def login():
    form = LoginForm()
    # VERVANGT IF REQUEST METHOD IS POST
    if form.validate_on_submit():
        user = form.email.data
        password = form.paswoord.data
        user_check = user_collection.find_one({"user": user})
        if user_check:
            if pbkdf2_sha256.verify(password, user_check["hpw"]):
                session["email"] = user
                return redirect(url_for("orders"))

        return render_template("login_fout.html")

    else:
        # session.clear()
        return render_template("wtf_login.html", form=form)


@app.route("/logout/")
def logout():
    session.pop("email")
    return redirect(url_for("login"))


@app.route("/orders/")
def orders():
    form = SearchField()
    email = session.get("email")
    if not email:
        return redirect(url_for("login"))
    last_order = last_order_collection.find_one()
    last_order_id = last_order["lastOrder"]
    orders_array = []
    today_order_value = 0
    total = 0
    order_data = orders_collection.find(
        {"id": {"$lte": last_order_id}}).sort("id", -1).limit(TEMPLATE_LIMIT)
    for order in order_data:
        if order["status"] == "processing_awaiting_shipment" or order["status"] == "processing_awaiting_pickup" or order["status"] == "processing_awaiting_payment":
            if order["flagPrinted"]:
                orders_array.append(
                    (order["number"], order["firstname"], order["lastname"], order["addressShippingCountry"], order["companyName"], format_date(order["created_at"]), format_status(order["status"]), order["priceIncl"], "printed"))
            else:
                orders_array.append(
                    (order["number"], order["firstname"], order["lastname"], order["addressShippingCountry"], order["companyName"], format_date(order["created_at"]), format_status(order["status"]), order["priceIncl"], "notprinted"))

            if datetime.today().strftime("%d-%m-%Y") == format_date_v_2(order["created_at"]):

                today_order_value += order["priceIncl"]

                total = round(today_order_value, 2)

    return render_template("orders.html", orders_array=orders_array, total=total, form=form)


@app.route("/orderdetail/", methods=["GET"])
def orderdetail():
    email = session.get("email")
    if not email:
        return redirect(url_for("login"))

    order_number = request.args.get("id")
    try:
        order = orders_collection.find_one({"number": int(order_number)})
        formatted_date = format_date(order["created_at"])
        formatted_status = format_status(order["status"])
        return render_template("orderdetail.html", order=order, formatted_date=formatted_date, formatted_status=formatted_status)
    except:
        return redirect(url_for("orders"))


# VOOR ZOEKBALK WTF PROTECTED IN ORDERS
@app.route("/orderdetail-wtf/", methods=["GET", "POST"])
def orderdetail_wtf():
    email = session.get("email")
    if not email:
        return redirect(url_for("login"))
    form = SearchField()
    # waarom werkt form.validate hier niet? OPLOSING The CSRF token is missing:{{form.hidden_tag()}}
    if form.validate_on_submit():
        order_number = form.gezocht_order.data

    # print(form.errors)

    try:
        order = orders_collection.find_one({"number": int(order_number)})
        formatted_date = format_date(order["created_at"])
        formatted_status = format_status(order["status"])
        return render_template("orderdetail.html", order=order, formatted_date=formatted_date, formatted_status=formatted_status)
    except:
        return redirect(url_for("orders"))


@app.route("/order_print/", methods=["GET"])
def order_print():
    email = session.get("email")
    if not email:
        return redirect(url_for("login"))

    # try:
    # gevonden_orders = orders_collection.find(
    #     {"flagPrinted": False}).sort("id", -1).limit(1)

    gevonden_orders = orders_collection.find({"$and": [{"flagPrinted": False}, {"$or": [
                                             {"status": "processing_awaiting_shipment"}, {"status": "processing_awaiting_pickup"}]}]}).sort("id", -1).limit(25)

    # gevonden_orders = orders_collection.find(
    #     {"number": {"$lte": 354560}}).sort("number", -1).limit(2)

    # MAke e deepcopy, the create orderbonnen functie lijkt de gevonden_orders weg te returnen
    gevonden_orders_copy = copy.deepcopy(gevonden_orders)
    gevonden_orders_copy_2 = copy.deepcopy(gevonden_orders)

    aantal_orders = 0
    hoogste_order_number = 0

    for order in gevonden_orders_copy:
        print(order['number'], 1)
        aantal_orders += 1
        if order["number"] > hoogste_order_number:
            hoogste_order_number = order["number"]

    if aantal_orders != 0:
        create_orderbonnen(
            gevonden_orders, hoogste_order_number, aantal_orders)
    else:
        return render_template("after_print_none.html")

    for order in gevonden_orders_copy_2:

        orders_collection.update_one({"number": order["number"]}, {
            "$set": {"flagPrinted": True}})

    return render_template("after_print.html", hoogste_order_number=hoogste_order_number)

    # except:

    return render_template("print_error.html")


@app.route("/print_one/", methods=["GET"])
def print_one():
    email = session.get("email")
    if not email:
        return redirect(url_for("login"))

    order_number = request.args.get("id")

    order_data = orders_collection.find({"number": int(order_number)})

    create_orderbonnen(order_data, order_number, 1)

    orders_collection.update_one({"number": int(order_number)}, {
        "$set": {"flagPrinted": True}})

    return render_template("after_print_one.html", order_number=order_number)


@app.route("/webhook_ls/")
def webhook_ls():
    # data = request
    return "webhook ls"


@app.route("/<path>")
def lost(path):

    # abort(404)
    return render_template("404.html", path=path)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error=error), 404

# XXXXX- REGISTER PART ONLY FOR INTERNAL USE - XXXXX


# @app.route("/register", methods=["POST", "GET"])
# def register():
#     if request.method == "POST":
#         user = request.form.get("email")
#         password = request.form.get("password")
#         hashed_password = pbkdf2_sha256.hash(password)
#         user_check = user_collection.find_one({"user": user})
#         if user_check:
#             print("USER BESTAAT REEDS")
#             # flash("USER BESTAAT REEDS")
#             return redirect(url_for("login.html"))
#         else:
#             new_user = {"user": user, "hpw": hashed_password}
#             user_collection.insert_one(new_user)
#             # flash("THANK YOU FOR REGISTER")
#             return redirect(url_for("register_success"))
#     else:
#         return render_template("register.html")


# @app.route("/register-success")
# def register_success():
#     return render_template("thank-register.html")
# # XXXXX- END OF REGISTER PART - XXXXX


if __name__ == "__main__":
    print("APP IS RUNNING ON PORT 5000")
    app.run(debug=True)
    print("AFTER APP RUN")
