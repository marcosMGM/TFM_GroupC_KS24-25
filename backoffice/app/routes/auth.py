from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from app.utils.decorators import login_required
from app.models.auth_model import get_user_by_login, update_last_access, update_password
from app.models.custom_model import recalculate_all
from werkzeug.security import check_password_hash

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        login_input = request.form['username']
        password_input = request.form['password']

        user = get_user_by_login(login_input)

        if user and check_password_hash(user.password, password_input):
            session['user'] = user.login
            session['user_name'] = user.nombre
            session['user_lastname'] = user.apellidos
            session['user_mail'] = user.email
            session['user_id'] = user.id
            update_last_access(user.id)

            """Dado que el recálculo de parámetros tarda poco, lo hacemos en cada login
            de esta forma cancelamos el riesgo de que se hayan quedado viviendas con 
            campos incorrectos por nuevos scrapping o actualizaciones de la tabla."""
            recalculate_all()

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
        if request.form['new_pwd'] != request.form['repeat_new_pwd']:
            flash("Las contraseñas especificadas no coinciden, no es posible realizar el cambio.", "warning")
            return render_template('pages/auth/password.html')
        
        user = get_user_by_login(session['user'])
        if not user or not check_password_hash(user.password, request.form['current_pwd']):
            flash("La contraseña actual especificada no es correcta, no es posible realizar el cambio.", "warning")
            return render_template('pages/auth/password.html')
        
        # aqui se debe cambiar la contraseña del usuario
        update_password(session.get('user_id','0'), request.form['new_pwd'])
        session.clear()
        flash("Contraseña modificada correctamente. Es necesario volver a iniciar sesión.", "primary")
        return redirect(url_for('auth_controller.login'))


    # return redirect(url_for('home_controller.login'))
    g.page_title = "Restablecimiento de contraseña"
    g.bc_level_1 = ("Home", url_for('home_controller.index'))
    g.bc_level_2 = ("Configuración de la cuenta", url_for('auth_controller.password'))
    # g.bc_level_3 = ("Cambiar sgfergr", url_for('auth_controller.password'))
    return render_template('pages/auth/password.html')


 



