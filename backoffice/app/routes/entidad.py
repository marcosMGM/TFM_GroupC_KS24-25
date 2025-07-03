from flask import Blueprint, render_template, request, redirect, url_for
from app.models.entidad import Entidad

entidad_bp = Blueprint("entidad", __name__)

@entidad_bp.route("/")
def list():
    return render_template("entidad/list.html", entidades=Entidad.all())

@entidad_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"]
        Entidad.add(Entidad(nombre))
        return redirect(url_for("entidad.list"))
    return render_template("entidad/form.html", accion="Crear", entidad=None)

@entidad_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    entidad = Entidad.get(id)
    if not entidad:
        return "Entidad no encontrada", 404
    if request.method == "POST":
        nombre = request.form["nombre"]
        Entidad.update(id, nombre)
        return redirect(url_for("entidad.list"))
    return render_template("entidad/form.html", accion="Editar", entidad=entidad)

@entidad_bp.route("/eliminar/<int:id>")
def eliminar(id):
    Entidad.delete(id)
    return redirect(url_for("entidad.list"))
