from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash
import pyodbc
import os
import datetime
from credenciales_sqlserver import *

app = Flask(__name__)
app.secret_key = 'supersecretkey'


conn_str = (
    # f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    # f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'DRIVER={{SQL Server}};'
    f'SERVER={SERVER},{PORT};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
)

# Ruta base del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_login = request.form['username']
        password = request.form['password']

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, login, password, nombre FROM sys_user
            WHERE login = ? AND estado = 1
        """, (user_login,))
        user = cursor.fetchone()

        if user and check_password_hash(user.password, password):
            session['user'] = user.nombre or user.login
            session['user_id'] = user.id

            """ Si el login es correcto, actualizar la fecha de acceso """
            now = datetime.datetime.now()
            cursor.execute("UPDATE sys_user SET last_access = ? WHERE id = ?", (now, user.id))
            conn.commit()
            conn.close()

            return redirect(url_for('home'))
        else:
            conn.close()
            return render_template('login.html', error="Credenciales inválidas o usuario inactivo.")

    return render_template('login.html')

@app.route('/menu')
def menu():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html', user=session['user'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


