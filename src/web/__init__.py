import os
from src.web import controllers
from src.core.models import database, Usuario
from datetime import timedelta
from flask import Flask, session
from flask_login import LoginManager
from src.core.config import config
from src.core.models import Laboratorio

def create_app(env: str = "development", static_folder: str = "../static"):
    app = Flask(
        __name__, static_folder=static_folder, template_folder="./templates"
    )
    configure_app(app, env)
    database.init_app(app)
    controllers.init_app(app)
    init_login_manager(app)
    init_cli_commands(app)
    return app

def init_cli_commands(app):
    """Define los comandos personalizados de Flask"""
    
    @app.cli.command(name="resetdb")
    def resetdb():
        """Comando para reiniciar la base de datos"""
        with app.app_context():
            database.reset_db()
            print("✅ La base de datos ha sido eliminada y recreada con éxito. 😎")
    
    from src.core import seed
    @app.cli.command(name="seeddb")
    def seed_db():
        """Comando para agregar semillas a la base de datos"""
        with app.app_context():
            database.reset_db()
            seed.seed_db()
            print("🙌 ¡Semilla cargada con éxito!🙌")


def init_login_manager(app):
    """Inicializa el gestor de sesiones y login"""
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "root.index_get"  # Ruta de inicio de sesión

    @login_manager.user_loader
    def load_user(user_id):
        # Comprobar el tipo de usuario en la sesión
        user_type = session.get('user_type')
        id = int(user_id)  # Convertir el ID a entero, ya que solo almacenamos el número
        
        if user_type == "usuario":
            return Usuario.query.get(id)
        elif user_type == "laboratorio":
            return Laboratorio.query.get(id)
        return None




def configure_app(app, env:str):
    """Configura los parámetros generales de la aplicación"""
    app.config.from_object(config[env])
    app.config['SECRET_KEY'] = 'e8771dffd56434456199d5087a3ea4d4'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)
    app.config['UPLOAD_FOLDER'] = os.path.join(
        os.getcwd(), "src", "static"
    ).replace(os.sep, "/") 