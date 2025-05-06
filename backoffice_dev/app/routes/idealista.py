from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from app.utils.decorators import login_required
# from app.models.idealista_model import get_user_by_login, update_last_access
from werkzeug.security import check_password_hash

idealista_controller = Blueprint('idealista_controller', __name__)

@idealista_controller.route("/index")
@idealista_controller.route("/")
@login_required
def index():
    g.page_title = "Propiedades obtenidas desde Idealista"
    g.bc_level_1 = ("Inicio", url_for('home_controller.index'))
    g.bc_level_2 = ("Propiedades", url_for('home_controller.index'))
    g.bc_level_3 = ("Idealista", url_for('idealista_controller.index'))
    return render_template("pages/idealista/list.html")
    # return redirect(url_for('home_controller.index'))

