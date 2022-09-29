from flask import Blueprint, render_template, redirect, url_for


auth = Blueprint("auth", __name__)


@auth.route("/login", methods = ['GET'])
def get_login():
    return render_template("auth/login.html")


@auth.route("/login", methods = ['POST'])
def post_login():
    username = request.form.get("username")
    password = request.form.get("password")
    return render_template("auth/login.html")


@auth.route("/register", methods = ['GET'])
def get_register():
    return render_template("auth/register.html")


@auth.route("/register", methods = ['POST'])
def post_register():
    username = request.form.get("username")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    return render_template("auth/register.html")


@auth.route("/logout", methods = ['GET'])
def get_logout():
    return redirect(url_for("views.home"))