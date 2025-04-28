from flask import Blueprint, render_template, request, session, redirect, url_for
from models.login import get_user_by_login, update_last_access
from werkzeug.security import check_password_hash

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['username']
        password_input = request.form['password']

        user = get_user_by_login(login_input)

        if user and check_password_hash(user.password, password_input):
            session['user'] = user.nombre or user.login
            session['user_id'] = user.id
            update_last_access(user.id)
            return redirect(url_for('home'))

        # return render_template('login.html', error="Credenciales inválidas o usuario inactivo")
        return render_template('sign_in_1.html', error="Credenciales inválidas o usuario inactivo")

    # return render_template('login.html')
    return render_template('sign_in_1.html')
