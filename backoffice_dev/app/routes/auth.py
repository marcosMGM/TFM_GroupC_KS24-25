from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.utils.decorators import login_required

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        if usuario == "admin" and clave == "1234":
            session["usuario"] = usuario
            return redirect(url_for("main.index"))
        else:
            flash("Credenciales incorrectas")
    return render_template("login.html")
