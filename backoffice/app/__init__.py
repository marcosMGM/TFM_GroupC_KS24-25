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
            profile_user_lastname=session.get('user_lastname'),
            profile_user_mail=session.get('user_mail'),
            profile_user_id=session.get('user_id'),
            )  
    @app.context_processor
    def inject_global_vars():
        return dict(
            page_title=getattr(g, 'page_title', APP_NAME),
            bc_level_1=getattr(g, 'bc_level_1', None),
            bc_level_2=getattr(g, 'bc_level_2', None),
            bc_level_3=getattr(g, 'bc_level_3', None),
            )



    from app.routes.home import home_controller
    from app.routes.statistics import statistics_controller
    from app.routes.auth import auth_controller
    from app.routes.idealista import idealista_controller
    from app.routes.prueba import prueba_controller
    from app.routes.custom import custom_controller

    app.register_blueprint(home_controller)
    app.register_blueprint(statistics_controller, url_prefix="/statistics")
    app.register_blueprint(auth_controller, url_prefix="/auth")
    app.register_blueprint(idealista_controller, url_prefix="/idealista")
    app.register_blueprint(custom_controller, url_prefix="/custom")
    app.register_blueprint(prueba_controller, url_prefix="/prueba")



    return app


