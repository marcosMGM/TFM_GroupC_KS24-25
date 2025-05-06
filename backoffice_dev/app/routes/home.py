from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g
from app.utils.decorators import login_required

home_controller = Blueprint('home_controller', __name__)

@home_controller.route("/")
@login_required
def index():
    g.page_title = "Inicio"
    return render_template("pages/home/inicio.html")

@home_controller.route("/mantenimiento")
@home_controller.route("/maintenance")
def maintenance():
    g.page_title = "Mantenimiento"
    return render_template("pages/maintenance/maintenance.html")
