from flask import Blueprint, url_for, render_template
user_pages = Blueprint("users", __name__, static_folder="static",
                       template_folder="templates")


@user_pages.route("/")
def users_home():
    return render_template("userwelkom.html")


@user_pages.route("/login")
def users_login():
    return render_template("login.html")


@user_pages.route("/register")
def users_register():
    return render_template("register.html")
