from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g
from app.utils.decorators import login_required

prueba_controller = Blueprint('prueba_controller', __name__)

@prueba_controller.route("/")   # /prueba/
@prueba_controller.route("/hola")   # /prueba/
@prueba_controller.route("/adios")   # /prueba/
@login_required
def index():
    g.page_title = "Esta es mi poágina Prueba"
    g.bc_level_1 = ("Home", url_for('home_controller.index'))
    g.bc_level_2 = ("Home", url_for('home_controller.index'))
    return render_template("pages/prueba/index.html")