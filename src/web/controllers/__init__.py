import flask
from src.web.controllers import (
    root,
    registrar,
    listar,
    listar_laboratorios,
    registrar_laboratorio,
    editar_perfil,
    registrar_paciente,
    mis_pacientes,
    reasignar,
    registrar_turno,
)

_blueprints = (
    root.bp,
    registrar.bp,
    listar.bp,
    listar_laboratorios.bp,
    registrar_laboratorio.bp,
    editar_perfil.bp,
    registrar_paciente.bp,
    mis_pacientes.bp,
    reasignar.bp,
    registrar_turno.bp,
)

def init_app(app: flask.Flask):
    """Initializes the controllers.
    Registers the blueprints and error handlers for the application.
    Also registers the before request hook for the application.
    """

    for bp in _blueprints:
        app.register_blueprint(bp)
