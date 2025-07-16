from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g
from matplotlib import markers
from app.utils.decorators import login_required
from app.models.custom_model import get_parameters, update_by_key, recalculate_all

custom_controller = Blueprint('custom_controller', __name__)

@custom_controller.route("/")
@custom_controller.route("/index")
@custom_controller.route("/index/")
@custom_controller.route("/index/<parametro>")
@login_required
def index(parametro=None):
    g.page_title = "Personalización de ajustes y parámetros"
    g.bc_level_1 = ("Inicio", url_for('home_controller.index'))
    g.bc_level_2 = ("Personalizacion", url_for('custom_controller.index'))
    if parametro != "dashboard":
        parametro = None
        
    return render_template("pages/custom/parameters.html", parameters = get_parameters(), parametro=parametro)

@custom_controller.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method == 'POST':
        for key in request.form:
            if key != "retorno_dashboard":
                update_by_key(key.replace("name_",""), request.form[key])
        recalculate_all()
    flash("Parámetros actualizados correctamente", "primary")
    
    if request.form.get("retorno_dashboard") == "1":
        return redirect(url_for('home_controller.index'))
    
    return redirect(url_for('custom_controller.index'))




@custom_controller.route("/mantenimiento")
@custom_controller.route("/maintenance")
def maintenance():
    g.page_title = "Mantenimiento"
    return render_template("pages/maintenance/maintenance.html")
