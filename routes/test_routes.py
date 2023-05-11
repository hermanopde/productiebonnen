# from flask import Blueprint,  redirect, url_for, render_template
# import datetime
# from fetch import testje
# app = Flask(__name__)
# print(__name__)

# testje()


# pages = Blueprint("habits", __name__,
#                   template_folder="templates", static_folder="static")


# @app.route("/")
# def home():
#     year = datetime.datetime.now().year

#     return render_template("home.html", year=year)


# @app.route("/orders/")
# def orders():
#     return render_template("orders.html")


# @app.route("/orderdetail/<int:order_number>")
# def order_detail(order_number):
#     return render_template("orderdetail.html", order_nr=order_number)


# @app.route("/userlogin/")
# def user_login():
#     # return "USER PAGINA"
#     # return redirect(url_for("orders"))
#     return render_template("login.html")


# @app.route("/userregister/")
# def user_register():
#     return render_template("register.html", order_nr=12345)


# if __name__ == "__main__":
#     app.run(debug=True)
