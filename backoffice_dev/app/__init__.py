from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'kjlcoGDSFGNHIOFJVSDfdjsbjgfdvhf'

    from app.routes.home import home_controller
    from app.routes.auth import auth_controller
    # from app.routes.entidad import entidad_bp

    app.register_blueprint(home_controller)
    app.register_blueprint(auth_controller, url_prefix="/auth")
    # app.register_blueprint(entidad, url_prefix="/entidades")


    @app.context_processor
    def inject_titulo():
        # Define the value for TITULO here
        # This value will be available in all templates
        return dict(TITULO="Título de la Aplicación")


    return app
