from flask import Flask, render_template, session, redirect, url_for
from controllers.login_controller import login_bp
import config 

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.context_processor
def inject_config_constants():
    return {
        "APP_NAME": config.APP_NAME,
        "VERSION": config.VERSION,
        "SESSION": session
    }

app.register_blueprint(login_bp)

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login_bp.login'))
    return render_template('pages/inicio.html', user=session['user'], name=session['user_name'], mail=session['user_mail'], pageTitle="Inicio")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_bp.login'))

if __name__ == '__main__':
    app.run(debug=config.DEBUG)
    # app.run(host='