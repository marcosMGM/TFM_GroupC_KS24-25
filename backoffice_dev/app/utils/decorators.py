from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Es necesario iniciar sesión para acceder a esta funcionalidad',"warning")
            return redirect(url_for('auth_controller.login'))
        return f(*args, **kwargs)
    return decorated_function
