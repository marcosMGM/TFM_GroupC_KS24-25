from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g
from matplotlib import markers
from app.utils.decorators import login_required
from app.models.home_model import get_oportunities, get_improvable_oportunities
from app.models.custom_model import get_parameters_by_key

home_controller = Blueprint('home_controller', __name__)

@home_controller.route("/")
@login_required
def index():
    g.page_title = "Smart Summary"
    parameters = get_parameters_by_key()
    oportunities = get_oportunities()
    improvable_oportunities = get_improvable_oportunities()

    return render_template("pages/home/inicio.html", oportunities = oportunities, improvable_oportunities = improvable_oportunities, parameters=parameters)






@home_controller.route("/mantenimiento")
@home_controller.route("/maintenance")
def maintenance():
    g.page_title = "Mantenimiento"
    return render_template("pages/maintenance/maintenance.html")
