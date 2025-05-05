from flask import Flask
from config import SECRET_KEY

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    from app.routes.home import home_controller
    from app.routes.auth import auth_controller
    # from app.routes.entidad import entidad_bp

    app.register_blueprint(home_controller)
    app.register_blueprint(auth_controller, url_prefix="/auth")
    # app.register_blueprint(entidad, url_prefix="/entidades")



    return app
