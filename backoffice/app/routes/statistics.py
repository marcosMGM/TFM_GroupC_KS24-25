from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g
from matplotlib import markers
from app.utils.decorators import login_required
from app.models.statistics_model import get_pie_ide_by_bedrooms, get_pie_ide_by_district, get_home_cards, get_sct1, get_map_markers

statistics_controller = Blueprint('statistics_controller', __name__)

@statistics_controller.route("/")
@login_required
def index():
    g.page_title = "Inicio"
    cards = get_home_cards()
    pie1 = get_pie_ide_by_district()
    bars1 = get_pie_ide_by_bedrooms()
    print(bars1)
    sct1 = get_sct1()
    map_markers = get_map_markers()
    return render_template("pages/statistics/inicio.html", pie1=pie1, bars1=bars1, cards=cards, sct1=sct1, map_markers=map_markers)

@statistics_controller.route("/roi_map")
@login_required
def roi_map():
    g.page_title = "Mapa de Rentabilidad de Inversión"
    map_markers = get_map_markers()
    return render_template("pages/statistics/roi_map.html", map_markers=map_markers)



@statistics_controller.route("/mantenimiento")
@statistics_controller.route("/maintenance")
def maintenance():
    g.page_title = "Mantenimiento"
    return render_template("pages/maintenance/maintenance.html")
