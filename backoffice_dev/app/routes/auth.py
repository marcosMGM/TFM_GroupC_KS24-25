from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
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
        return render_template('pages/auth/login.html')
    
    # flash("Tiene que iniciar sesión", "success")
    return render_template('pages/auth/login.html')


@auth_controller.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for('auth_controller.login'))

@auth_controller.route('/password', methods=["GET", "POST"])
@login_required
def password(): 
    if request.method == 'POST':
        login_input = request.form['username']
        password_input = request.form['password']
        flash("Sesión cerrada correctamente", "success")

    # return redirect(url_for('home_controller.login'))

    g.page_title = "Restablecimiento de contraseña"
    g.bc_level_1 = ("Home", url_for('home_controller.index'))
    g.bc_level_2 = ("Configuración de la cuenta", url_for('auth_controller.password'))
    # g.bc_level_3 = ("Cambiar sgfergr", url_for('auth_controller.password'))
    return render_template('pages/auth/password.html')


 



