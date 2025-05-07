from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from app.utils.decorators import login_required
from app.models.idealista_model import get_datalist
from werkzeug.security import check_password_hash
from flask import jsonify
from app.config import IDEALISTA_URL

idealista_controller = Blueprint('idealista_controller', __name__)

@idealista_controller.route("/index")
@idealista_controller.route("/")
@login_required
def index():
    g.page_title = "Propiedades obtenidas desde Idealista"
    g.bc_level_1 = ("Inicio", url_for('home_controller.index'))
    g.bc_level_2 = ("Propiedades", url_for('home_controller.index'))
    g.bc_level_3 = ("Idealista", url_for('idealista_controller.index'))
    return render_template("pages/idealista/list.html", IDEALISTA_URL=IDEALISTA_URL)
    # return redirect(url_for('home_controller.index'))



""" 
Esta es la petición que se hace desde el datatable al cargar la página:

con esto debo controlar paginación, ordenación y búsqueda de los datos que se muestran en el datatable, 
>serverside<

127.0.0.1 - - [06/May/2025 23:14:31] "GET /idealista/datalist?draw=1&columns[0][data]=id&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=titulo&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start=0&length=10&search[value]=&search[regex]=false&_=1746566070857 HTTP/1.1" 200 -


 """
@idealista_controller.route("/datalist")
@login_required
def datalist():
    datalist = get_datalist(request.args)
    # datalist = get_datalist(request.form)
    return jsonify(datalist)
