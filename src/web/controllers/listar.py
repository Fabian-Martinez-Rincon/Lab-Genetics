from flask import render_template, Blueprint, session
from src.core.models.database import db
from src.core.models.usuario import Usuario
from src.core.models.rol import Rol
from src.core.models.turno import Turno
from src.core.models.estado import Estado
from src.web.controllers.utils import verificar_rol, verificar_autenticacion


"""
## Roles
--------------
1: Owner
2: Administrador
3: Laboratorio
4: Medico
5: Paciente
6: Transportista
--------------
"""

bp = Blueprint('listar', __name__)

def filtrar_usuarios(roles_permitidos):
    return db.session.query(Usuario).join(Rol).filter(Usuario.id_rol.in_(roles_permitidos)).all()

@bp.route('/listar_usuarios')
@verificar_autenticacion
@verificar_rol(1)
def listar_usuarios():
    roles_permitidos = [2, 4, 6]
    usuarios = filtrar_usuarios(roles_permitidos)
    return render_template('owner/listar_usuarios.html', usuarios=usuarios)

@bp.route('/listar_turnos')
@verificar_autenticacion
@verificar_rol(3)
def listar_turnos():
    # Consulta que incluye el nombre del estado y ordena los turnos por fecha
    mis_turnos = Turno.query.join(Estado, Turno.estado == Estado.id).filter(
        Turno.id_laboratorio == session['user_id']
    ).add_columns(
        Turno.fecha, Turno.hora, Turno.id_estudio, Estado.nombre.label('estado_nombre')
    ).order_by(Turno.fecha.asc()).all()  # Ordena los turnos por fecha de forma ascendente
    return render_template('owner/listar_turnos.html', turnos=mis_turnos)