from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from app.utils.decorators import login_required
# from app.models.idealista_model import get_user_by_login, update_last_access
from werkzeug.security import check_password_hash

idealista_controller = Blueprint('idealista_controller', __name__)

@idealista_controller.route("/index")
@idealista_controller.route("/")
@login_required
def index():
    g.page_title = "Idealista"
    return redirect(url_for('home_controller.index'))

