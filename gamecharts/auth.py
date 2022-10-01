from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db


auth = Blueprint("auth", __name__)


@auth.route("/login", methods = ['GET'])
def get_login():
    return render_template("auth/login.html")


@auth.route("/login", methods = ['POST'])
def post_login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    
    if (user):
        if (check_password_hash(user.pwd, password)):
            login_user(user, remember=True)
            return redirect(url_for("views.get_home"))
        else:
            flash('password is incorrect.', category='error')
    else:
        flash('username does not exist.', category='error')

    return render_template("auth/login.html")


@auth.route("/register", methods = ['GET'])
def get_register():
    return render_template("auth/register.html")


@auth.route("/register", methods = ['POST'])
def post_register():
    username = request.form.get("username")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")

    username_exists = User.query.filter_by(username=username).first()

    if username_exists:
        flash('username already exists.', category='error')
    elif len(username) < 5:
        flash('username must be at least 5 characters in length.', category='error')
    elif password1 != password2:
        flash('passwords do NOT match.', category='error')
    elif len(password1) < 8:
        flash('password must be at least 8 characters in length.', category='error')
    else:
        new_user = User(username=username, pwd=generate_password_hash(password1, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth.get_login"))

    return render_template("auth/register.html")


@auth.route("/logout", methods = ['GET'])
def get_logout():
    logout_user()
    return redirect(url_for("views.get_home"))