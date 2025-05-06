from flask import Flask, session, g
from app.config import SECRET_KEY, APP_NAME, VERSION

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY


    @app.context_processor
    def inject_config_constants():
        return {
            "APP_NAME": APP_NAME,
            "VERSION": VERSION
        }
    @app.context_processor
    def inject_user():
        return dict(
            profile_user=session.get('user'),
            profile_user_name=session.get('user_name'),
            profile_user_mail=session.get('user_mail'),
            profile_user_id=session.get('user_id'),
            )  
    @app.context_processor
    def inject_global_vars():
        return dict(page_title=getattr(g, 'page_title', APP_NAME))



    from app.routes.home import home_controller
    from app.routes.auth import auth_controller
    from app.routes.idealista import idealista_controller
    # from app.routes.entidad import entidad_bp

    app.register_blueprint(home_controller)
    app.register_blueprint(auth_controller, url_prefix="/auth")
    app.register_blueprint(idealista_controller, url_prefix="/idealista")
    # app.register_blueprint(auth_controller, url_prefix="/auth")
    # app.register_blueprint(entidad, url_prefix="/entidades")


    return app


