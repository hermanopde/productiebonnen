from pymongo import MongoClient, UpdateOne
from dotenv import dotenv_values
from passlib.hash import pbkdf2_sha256

from flask import Flask, redirect, url_for, render_template, request, session, flash, abort
from routes import order_pages, user_pages
# from fetch import fetch_and_save_lsorders, fetch_last_order, get_customization
import time
from datetime import datetime, timedelta

# from templates import UserForm

config = dotenv_values(".env")

year = datetime.now().year
app = Flask(__name__)

app.secret_key = config["APP_SECRET_KEY"]

app.permanent_session_lifetime = timedelta(minutes=5)


password_mg_db = config["MONGODB_PWD"]
connection_string = f"mongodb+srv://herman:{password_mg_db}@production.4d02xna.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(connection_string)
db = client.packinglist

user_collection = db.users

app.register_blueprint(order_pages, url_prefix="/production")
app.register_blueprint(user_pages, url_prefix="/auth")

orders_collection = db.lsorders

orders_collection.delete_many({"id": {"$lte": 250401058}})


orders_to = [354484, 354485]
# for nr in range(354355, 354484):
#     print(nr)
#     orders_collection.update_one({"number": nr}, {
#         "$set": {"flagPrinted": True}})


# orders_collection.bulk_write([{UpdateOne: {"filter": {
#     "number": orders_to[0]}, "update": {"$set": {"flagPrinted": True}}}},
#     {UpdateOne: {"filter": {
#         "number": orders_to[1]}, "update": {"$set": {"flagPrinted": True}}}}
# ])
# gevonden_orders = orders_collection.find({"flagPrinted": False}).sort("id", -1)

# for order in gevonden_orders:
#     print(order["number"])

# @app.route("/")
# def home():
#     return redirect(url_for("orders"))


# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if request.method == "POST":
#         user = request.form.get("email")
#         password = request.form.get("password")
#         user_check = user_collection.find_one({"user": user})
#         if user_check:
#             if pbkdf2_sha256.verify(password, user_check["hpw"]):
#                 session["email"] = user
#                 return redirect(url_for("orders"))

#         return "VERKEERD PASWOORD OF EMAIL"

#     else:
#         # session.clear()
#         return render_template("login.html", joske=year)


# @app.route("/orders")
# def orders():
#     email = session.get("email")
#     if not email:
#         return redirect(url_for("login"))

#     return render_template("orders.html")


# @app.route("/<path>")
# def lost(path):
#     abort(404)
#     return render_template("404.html", path=path)


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template("404.html", error=error), 404


#     # XXXXX- REGISTER PART ONLY FOR INTERNAL USE - XXXXX
#     # @app.route("/register", methods=["POST", "GET"])
#     # def register():
#     #     if request.method == "POST":
#     #         user = request.form.get("email")
#     #         password = request.form.get("password")
#     #         hashed_password = pbkdf2_sha256.hash(password)
#     #         user_check = user_collection.find_one({"user": user})
#     #         if user_check:
#     #             print("USER BESTAAT REEDS")
#     #             # flash("USER BESTAAT REEDS")
#     #             return redirect(url_for("login.html"))
#     #         else:
#     #             new_user = {"user": user, "hpw": hashed_password}
#     #             user_collection.insert_one(new_user)
#     #             # flash("THANK YOU FOR REGISTER")
#     #             return redirect(url_for("register_success"))
#     #     else:
#     #         return render_template("register.html")
#     # @app.route("/register-success")
#     # def register_success():
#     #     return render_template("thank-register.html")
#     # XXXXX- END OF REGISTER PART - XXXXX
# if __name__ == "__main__":
#     print("APP IS RUNNING ON PORT 5000")
#     app.run()
#     print("AFTER APP RUN")
