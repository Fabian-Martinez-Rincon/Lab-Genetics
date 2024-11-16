from flask import Flask, render_template, Blueprint, request, redirect, url_for, session, flash
from src.core.models.database import db
from src.core.models.usuario import Usuario
from src.core.models.rol import Rol
from src.core.models.turno import Turno
from src.core.models.estado import Estado
from src.web.controllers.utils import verificar_rol, verificar_autenticacion
from src.core.models.laboratorio import Laboratorio
from src.core.models.estudio import Estudio
from src.core.models.historialEstado import HistorialEstado
from src.core.models.resultado import Resultado
from src.core.models.presupuesto import Presupuesto

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

@verificar_autenticacion
@bp.route('/listar_laboratorios_turnos', methods=['GET'])
def listar_laboratorios():
    laboratorios = Laboratorio.query.filter_by(estado='ACTIVO').all()
    return render_template('owner/listar_laboratorios_turnos.html', laboratorios=laboratorios)


"""
Tenes que agarrar el último estado del historial_esatdo de un ID de estudio y si esta en estado "APROBADO" Lo listas. 
A partir de ahí tiene que haber un botón de solicitar turno que a partir de ese ID de 
estudio elige Laboratorio de extracción, fecha y Horario

> Esto lo dejo para despues, de momento los vamos a listar asi nomas
"""
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
        estado_actual = db.session.query(HistorialEstado.estado)\
            .filter(HistorialEstado.estudio_id == estudio.id)\
            .order_by(HistorialEstado.fecha_hora.desc())\
            .first()
        
        estudio.estado_nombre = estado_actual.estado if estado_actual else 'Desconocido'

    return render_template('paciente/mis_estudios.html', estudios=estudios)

@bp.route('/detalle_estudio/<estudio_id>', methods=['GET'])
@verificar_autenticacion
@verificar_rol(5)
def detalle_estudio(estudio_id):
    estudio = Estudio.query.get(estudio_id)
    if not estudio:
        flash('Estudio no encontrado.', 'error')
        return redirect(url_for('paciente.mis_estudios'))
    
    # Obtener el estado actual del estudio
    estado_actual = db.session.query(HistorialEstado.estado)\
        .filter(HistorialEstado.estudio_id == estudio.id)\
        .order_by(HistorialEstado.fecha_hora.desc())\
        .first()
    estudio.estado_nombre = estado_actual.estado if estado_actual else 'Desconocido'

    # Obtener el resultado relacionado
    resultado = None
    if estudio.id_resultado:
        resultado = db.session.query(Resultado).get(estudio.id_resultado)

    return render_template('paciente/detalle_estudio.html', estudio=estudio, resultado=resultado)

from sqlalchemy import or_

@bp.route('/ver_estudios_medico', methods=['GET'])
@verificar_autenticacion
@verificar_rol(4)
def ver_estudios_medico():
    id_usuario = session.get('user_id')
    
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        flash('Usuario no encontrado.', 'error')
        return redirect(url_for('root.index_get'))
    
    # Obtener el parámetro de búsqueda
    estudio_id = request.args.get('estudio_id', '')

    # Filtrar estudios por ID con coincidencias parciales
    estudios = usuario.estudios_como_medico
    if estudio_id:
        estudios = [estudio for estudio in estudios if estudio_id in str(estudio.id)]

    # Obtener el estado actual de cada estudio
    for estudio in estudios:
        estado_actual = db.session.query(HistorialEstado.estado)\
            .filter(HistorialEstado.estudio_id == estudio.id)\
            .order_by(HistorialEstado.fecha_hora.desc())\
            .first()
        
        estudio.estado_nombre = estado_actual.estado if estado_actual else 'Desconocido'

    return render_template('medico/ver_estudios_medico.html', estudios=estudios)



@bp.route('/detalle_estudio_medico/<estudio_id>', methods=['GET'])
@verificar_autenticacion
@verificar_rol(4)
def detalle_estudio_medico(estudio_id):
    estudio = Estudio.query.get(estudio_id)
    if not estudio:
        flash('Estudio no encontrado.', 'error')
        return redirect(url_for('medico/ver_estudios_medico.html'))
    
    # Obtener el estado actual del estudio
    estado_actual = db.session.query(HistorialEstado.estado)\
        .filter(HistorialEstado.estudio_id == estudio.id)\
        .order_by(HistorialEstado.fecha_hora.desc())\
        .first()
    estudio.estado_nombre = estado_actual.estado if estado_actual else 'Desconocido'

    # Obtener el resultado relacionado
    resultado = None
    if estudio.id_resultado:
        resultado = db.session.query(Resultado).get(estudio.id_resultado)

    return render_template('medico/detalle_estudio.html', estudio=estudio, resultado=resultado)


@bp.route('/ver_estudios_paciente/<int:paciente_id>', methods=['GET'])
@verificar_autenticacion
@verificar_rol(4)
def ver_estudios_paciente(paciente_id):
    # Verificar que el médico tenga acceso al paciente
    id_medico = session.get('user_id')
    paciente = Usuario.query.filter_by(id=paciente_id, id_medico=id_medico).first()
    if not paciente:
        flash('Paciente no encontrado o no autorizado para ver este perfil.', 'error')
        return redirect(url_for('root.index_get'))

    # Obtener el parámetro de búsqueda para coincidencias parciales de ID
    estudio_id = request.args.get('estudio_id', '')

    # Filtrar estudios del paciente específico por coincidencias parciales en el ID
    estudios = paciente.estudios_como_paciente
    if estudio_id:
        estudios = [estudio for estudio in estudios if estudio_id in str(estudio.id)]

    # Obtener el estado actual de cada estudio
    for estudio in estudios:
        estado_actual = db.session.query(HistorialEstado.estado)\
            .filter(HistorialEstado.estudio_id == estudio.id)\
            .order_by(HistorialEstado.fecha_hora.desc())\
            .first()
        
        estudio.estado_nombre = estado_actual.estado if estado_actual else 'Desconocido'

    return render_template('paciente/ver_estudios_paciente.html', paciente=paciente, estudios=estudios)

@bp.route('/presupuesto_estudio/<estudio_id>', methods=['GET'])
@verificar_autenticacion
@verificar_rol(5)
def presupuesto_estudio(estudio_id):
    # Obtener el estudio
    estudio = Estudio.query.get(estudio_id)
    if not estudio:
        flash('Estudio no encontrado.', 'error')
        return redirect(url_for('listar.mis_estudios'))

    # Obtener el presupuesto relacionado con el estudio
    presupuesto = Presupuesto.query.get(estudio.id_presupuesto)
    
    if not presupuesto:
        flash('Presupuesto no disponible para este estudio.', 'error')
        return redirect(url_for('listar.mis_estudios'))

    # Renderizar la plantilla con el presupuesto y su comprobante
    return render_template(
        'administrador/presupuesto_estudio.html',
        estudio=estudio,
        presupuesto=presupuesto,
        comprobante_path=presupuesto.comprobante_path
    )

