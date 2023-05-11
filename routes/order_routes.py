from flask import Blueprint, url_for, render_template
order_pages = Blueprint("orders", __name__, static_folder="static",
                        template_folder="templates")


@order_pages.route("/")
def orders_home():
    return render_template("orders.html")


@order_pages.route("/detail")
def orders_detail():
    return render_template("orderdetail.html")

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
