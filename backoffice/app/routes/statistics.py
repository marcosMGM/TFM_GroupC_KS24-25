from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g
from matplotlib import markers
from app.utils.decorators import login_required
from app.models.statistics_model import  get_home_kpi, get_map_markers, get_houses_by_distrito, get_home_scatter
from app.models.custom_model import get_parameters_by_key

statistics_controller = Blueprint('statistics_controller', __name__)

@statistics_controller.route("/")
@statistics_controller.route("/index")
@statistics_controller.route("/index/")
@login_required
def index():
    g.page_title = "Data Explorer"
    home_kpi = get_home_kpi()
    parameters = get_parameters_by_key()
    houses_by_distrito = get_houses_by_distrito()
    scatter_data = get_home_scatter()

    return render_template("pages/statistics/index.html", kpi=home_kpi, parameters=parameters , houses_by_distrito=houses_by_distrito, scatter_data=scatter_data)

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
