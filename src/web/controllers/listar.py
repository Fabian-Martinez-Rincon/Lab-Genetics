from flask import Flask, render_template, Blueprint, request, redirect, url_for, session, flash
from src.core.models.database import db
from src.core.models.usuario import Usuario
from src.core.models.rol import Rol
from src.core.models.turno import Turno
from src.core.models.estado import Estado
from src.web.controllers.utils import verificar_rol, verificar_autenticacion
from src.core.models.laboratorio import Laboratorio

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

@bp.route('/listar_usuarios', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(1)
def listar_usuarios():
    roles_permitidos = [2, 4, 6]
    
    if request.method == 'POST':
        usuario_id = request.form.get('usuario_id')
        nuevo_estado = request.form.get('nuevo_estado')

        # Actualiza el estado del usuario
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            usuario.estado = nuevo_estado
            db.session.commit()

        return redirect(url_for('listar.listar_usuarios'))

    usuarios = filtrar_usuarios(roles_permitidos)
    return render_template('owner/listar_usuarios.html', usuarios=usuarios)


@bp.route('/listar_turnos')
@verificar_autenticacion
@verificar_rol(3)
def listar_turnos():
    # Consulta que incluye el nombre del estado y el usuario asociado al turno
    mis_turnos = Turno.query \
        .join(Estado, Turno.estado == Estado.id) \
        .outerjoin(Usuario, Turno.id_paciente == Usuario.id) \
        .add_columns(
            Turno.fecha, Turno.hora, Turno.id_estudio, Estado.nombre.label('estado_nombre'),
            Usuario.dni, Usuario.nombre, Usuario.apellido
        ) \
        .order_by(Turno.fecha.asc()).all()
    return render_template('owner/listar_turnos.html', turnos=mis_turnos)

@bp.route('/listar_laboratorios_turnos', methods=['GET'])
def listar_laboratorios():
    laboratorios = Laboratorio.query.filter_by(estado='ACTIVO').all()
    return render_template('owner/listar_laboratorios_turnos.html', laboratorios=laboratorios)

@bp.route('/mis_estudios', methods=['GET'])
@verificar_autenticacion
@verificar_rol(5)
def mis_estudios():
    id_usuario = session.get('user_id')
    
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        flash('Usuario no encontrado.', 'error')
        return redirect(url_for('root.index_get'))
    
    estudios = usuario.estudios_como_paciente
    for estudio in estudios:
        estado_nombre = db.session.query(Estado.nombre).filter_by(id=estudio.id_estado).scalar()
        estudio.estado_nombre = estado_nombre
    return render_template('paciente/mis_estudios.html', estudios=estudios)


