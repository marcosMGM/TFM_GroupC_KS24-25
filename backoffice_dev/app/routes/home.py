from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g
from matplotlib import markers
from app.utils.decorators import login_required
from app.models.home_model import get_pie_ide_by_bedrooms, get_home_cards, get_sct1, get_map_markers

home_controller = Blueprint('home_controller', __name__)

@home_controller.route("/")
@login_required
def index():
    g.page_title = "Inicio"
    cards = get_home_cards()
    pie1 = get_pie_ide_by_bedrooms()
    sct1 = get_sct1()
    map_markers = get_map_markers()
    return render_template("pages/home/inicio.html", pie1=pie1, cards=cards, sct1=sct1, map_markers=map_markers)



@home_controller.route("/mantenimiento")
@home_controller.route("/maintenance")
def maintenance():
    g.page_title = "Mantenimiento"
    return render_template("pages/maintenance/maintenance.html")
