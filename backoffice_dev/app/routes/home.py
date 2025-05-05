from flask import Blueprint, render_template

home_controller = Blueprint('home_controller', __name__)

@home_controller.route("/")
def index():
    return render_template("pages/inicio.html")
