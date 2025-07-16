from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g
from matplotlib import markers
from app.utils.decorators import login_required
from app.models.statistics_model import get_pie_ide_by_bedrooms, get_pie_ide_by_district, get_home_cards, get_sct1, get_map_markers
from app.models.custom_model import get_parameters_by_key

statistics_controller = Blueprint('statistics_controller', __name__)

@statistics_controller.route("/")
@statistics_controller.route("/index")
@statistics_controller.route("/index/")
@login_required
def index():
    g.page_title = "Inicio"
    cards = get_home_cards()
    pie1 = get_pie_ide_by_district()
    bars1 = get_pie_ide_by_bedrooms()
    print(bars1)
    sct1 = get_sct1()
    return render_template("pages/statistics/index.html", pie1=pie1, bars1=bars1, cards=cards, sct1=sct1)

@statistics_controller.route("/roi_map")
@login_required
def roi_map():
    g.page_title = "Radar de Oportunidades"
    map_markers = get_map_markers()
    parameters = get_parameters_by_key()
    return render_template("pages/statistics/roi_map.html", map_markers=map_markers, parameters=parameters)



@statistics_controller.route("/mantenimiento")
@statistics_controller.route("/maintenance")
def maintenance():
    g.page_title = "Mantenimiento"
    return render_template("pages/maintenance/maintenance.html")
