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
    editar_paciente,
    ver_paciente,
    solicitar_estudio,
    administrador,
    generar_presupuesto,
    acciones_presupuesto,
    verificar_pago,
    solicitar_turno,
    confirmar_turno,
    transportista
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
    editar_paciente.bp,
    ver_paciente.bp,
    solicitar_estudio.bp,
    administrador.bp,
    generar_presupuesto.bp,
    acciones_presupuesto.bp,
    verificar_pago.bp,
    solicitar_turno.bp,
    confirmar_turno.bp,
    transportista.bp
)

def init_app(app: flask.Flask):
    """Initializes the controllers.
    Registers the blueprints and error handlers for the application.
    Also registers the before request hook for the application.
    """

    for bp in _blueprints:
        app.register_blueprint(bp)
