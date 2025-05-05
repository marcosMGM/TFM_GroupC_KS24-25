from flask import Blueprint, render_template
from app.utils.decorators import login_required

home_controller = Blueprint('home_controller', __name__)

@home_controller.route("/")
# @login_required
def index():
    return render_template("pages/inicio.html")
