import flask
from src.web.controllers import (
    root,
    registrar,
    listar_usuarios,
    listar_laboratorios,
    registrar_laboratorio,
    editar_perfil
)

_blueprints = (
    root.bp,
    registrar.bp,
    listar_usuarios.bp,
    listar_laboratorios.bp,
    registrar_laboratorio.bp,
    editar_perfil.bp
)

def init_app(app: flask.Flask):
    """Initializes the controllers.
    Registers the blueprints and error handlers for the application.
    Also registers the before request hook for the application.
    """

    for bp in _blueprints:
        app.register_blueprint(bp)
