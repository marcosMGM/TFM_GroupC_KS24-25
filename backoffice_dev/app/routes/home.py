from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g
from app.utils.decorators import login_required
from app.models.home_model import get_pie_ide_by_bedrooms, get_home_cards

home_controller = Blueprint('home_controller', __name__)

@home_controller.route("/")
@login_required
def index():
    g.page_title = "Inicio"
    cards = get_home_cards()
    pie1 = get_pie_ide_by_bedrooms()
    return render_template("pages/home/inicio.html", pie1=pie1, cards=cards)



@home_controller.route("/mantenimiento")
@home_controller.route("/maintenance")
def maintenance():
    g.page_title = "Mantenimiento"
    return render_template("pages/maintenance/maintenance.html")
