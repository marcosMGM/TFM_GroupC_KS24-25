from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g
from matplotlib import markers
from app.utils.decorators import login_required
from app.models.custom_model import get_parameters, update_by_key, recalculate_all

custom_controller = Blueprint('custom_controller', __name__)

@custom_controller.route("/")
@custom_controller.route("/index")
@login_required
def index():
    g.page_title = "Inicio"
    g.bc_level_1 = ("Inicio", url_for('home_controller.index'))
    g.bc_level_2 = ("Personalizacion", url_for('custom_controller.index'))
    
    # g.bc_level_3 = ("Idealista", url_for('idealista_controller.index'))

    return render_template("pages/custom/parameters.html", parameters = get_parameters())



@custom_controller.route("/update", methods=["GET", "POST"])
@custom_controller.route("/update/<parametro>", methods=["GET", "POST"])
@login_required
def update(parametro=None):
    if request.method == 'POST':
        for key in request.form:
            update_by_key(key.replace("name_",""), request.form[key])
        recalculate_all()


    flash("Parámetros actualizados correctamente", "primary")
    # return "HOLA"
    if parametro is not None and parametro == "dashboard":
        return redirect(url_for('custom_controller.index', parametro=parametro))
    return redirect(url_for('custom_controller.index'))



@custom_controller.route("/mantenimiento")
@custom_controller.route("/maintenance")
def maintenance():
    g.page_title = "Mantenimiento"
    return render_template("pages/maintenance/maintenance.html")
