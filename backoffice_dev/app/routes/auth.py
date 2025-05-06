from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.utils.decorators import login_required
from app.models.auth_model import get_user_by_login, update_last_access
from werkzeug.security import check_password_hash

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        login_input = request.form['username']
        password_input = request.form['password']

        user = get_user_by_login(login_input)

        if user and check_password_hash(user.password, password_input):
            session['user'] = user.nombre or user.login
            session['user_name'] = user.nombre
            session['user_mail'] = user.email
            session['user_id'] = user.id
            update_last_access(user.id)
            return redirect(url_for('home_controller.index'))

        flash("Credenciales inválidas o usuario inactivo", "danger")
        return render_template('pages/login.html')
    
    # flash("Tiene que iniciar sesión", "success")
    return render_template('pages/login.html')


@auth_controller.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for('auth_controller.login'))



