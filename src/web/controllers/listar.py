from flask import Flask, render_template, Blueprint, request, redirect, url_for, session, flash, current_app
from src.core.models.database import db
from src.core.models.usuario import Usuario
from src.core.models.rol import Rol
from src.core.models.turno import Turno
from src.core.models.estado import Estado
from src.web.controllers.utils import verificar_rol, verificar_autenticacion, actualizar_presupuestos_vencidos, actualizar_turnos_vencidos
from src.core.models.laboratorio import Laboratorio
from src.core.models.estudio import Estudio
from src.core.models.historialEstado import HistorialEstado
from src.core.models.resultado import Resultado
from src.core.models.presupuesto import Presupuesto
from src.core.models.notificacion import Notificacion
from werkzeug.utils import secure_filename
import os

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
            if nuevo_estado == 'INACTIVO':
                Notificacion.send_mail(usuario.id, f"Su cuenta ha sido desactivada por el Administrador General. Ante cualquier duda, contacte al soporte.")
            else:
                Notificacion.send_mail(usuario.id, f"Su cuenta ha sido reactivada por el Administrador General. ¡Bienvenido de vuelta!")

        return redirect(url_for('listar.listar_usuarios'))

    usuarios = filtrar_usuarios(roles_permitidos)
    return render_template('owner/listar_usuarios.html', usuarios=usuarios)


from datetime import date

@bp.route('/listar_turnos')
@verificar_autenticacion
@actualizar_turnos_vencidos
@verificar_rol(3)
def listar_turnos():
    # Filtrar turnos únicamente en estado "PENDIENTE" y ordenarlos por fecha y hora
    turnos_pendientes = Turno.query \
        .join(Estado, Turno.estado == Estado.id) \
        .outerjoin(Usuario, Turno.id_paciente == Usuario.id) \
        .outerjoin(Estudio, Turno.id_estudio == Estudio.id) \
        .filter(Estado.nombre == 'PENDIENTE') \
        .add_columns(
            Turno.id.label('turno_id'),
            Turno.fecha,
            Turno.hora,
            Turno.id_estudio,
            Estado.nombre.label('estado_nombre'),
            Usuario.dni.label('usuario_dni'),
            Usuario.nombre.label('usuario_nombre'),
            Usuario.apellido.label('usuario_apellido'),
            Estudio.consentimiento_path.label('consentimiento_path')
        ) \
        .order_by(Turno.fecha.asc(), Turno.hora.asc()).all()

    current_date = date.today()

    return render_template(
        'owner/listar_turnos.html',
        turnos=turnos_pendientes,
        current_date=current_date
    )






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
@actualizar_presupuestos_vencidos
@actualizar_turnos_vencidos
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
@actualizar_turnos_vencidos
@verificar_rol(5)
def detalle_estudio(estudio_id):
    estudio = Estudio.query.get(estudio_id)
    if not estudio:
        flash('Estudio no encontrado.', 'error')
        return redirect(url_for('listar.mis_estudios'))
    
    # Obtener el estado actual del estudio
    estado_actual = db.session.query(HistorialEstado.estado)\
        .filter(HistorialEstado.estudio_id == estudio.id)\
        .order_by(HistorialEstado.fecha_hora.desc())\
        .first()
    estudio.estado_nombre = estado_actual.estado if estado_actual else 'Desconocido'

    # Verificar si el estado actual es "PAGO ACEPTADO"
    estado_pago_aceptado = estado_actual.estado == "PAGO ACEPTADO" if estado_actual else False
    estado_turno_cancelado = estado_actual.estado == "TURNO CANCELADO" if estado_actual else False
    # Obtener el historial de estados ordenado por fecha descendente
    historial_estados = db.session.query(HistorialEstado)\
        .filter(HistorialEstado.estudio_id == estudio.id)\
        .order_by(HistorialEstado.fecha_hora.desc()).all()

    # Obtener el resultado relacionado
    resultado = None
    if estudio.id_resultado:
        resultado = db.session.query(Resultado).get(estudio.id_resultado)

    return render_template(
        'paciente/detalle_estudio.html', 
        estudio=estudio, 
        resultado=resultado, 
        historial_estados=historial_estados,
        estado_pago_aceptado=estado_pago_aceptado, estado_turno_cancelado=estado_turno_cancelado
    )



from sqlalchemy import or_

@bp.route('/ver_estudios_medico', methods=['GET'])
@verificar_autenticacion
@actualizar_presupuestos_vencidos
@actualizar_turnos_vencidos
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
@actualizar_presupuestos_vencidos
@actualizar_turnos_vencidos
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


def cargar_comprobante(comprobante, estudio_id):
    ruta_comprobante = None  
    _, extension = os.path.splitext(comprobante.filename)
    extension = extension.lower()
    if extension in ['.jpg', '.png', '.pdf']:
        nombre_archivo = f"{secure_filename(estudio_id)}{extension}"
        ruta_carpeta = 'comprobante'  
        carpeta_absoluta = os.path.join(current_app.config['UPLOAD_FOLDER'], ruta_carpeta)
        os.makedirs(carpeta_absoluta, exist_ok=True)
        ruta_comprobante_absoluta = os.path.join(carpeta_absoluta, nombre_archivo)
        comprobante.save(ruta_comprobante_absoluta)
        ruta_comprobante = os.path.join(ruta_carpeta, nombre_archivo).replace("\\", "/")
    else:
        flash('El archivo debe ser una imagen o un pdf', 'error')              
    return ruta_comprobante

@bp.route('/presupuesto_estudio/<estudio_id>', methods=['GET', 'POST'])
@verificar_autenticacion
@actualizar_presupuestos_vencidos
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
    
    if request.method == 'POST':
        # Actualizar el comprobante del presupuesto
        comprobante = request.files.get('comprobante')
        if comprobante:
            ruta = cargar_comprobante(comprobante, estudio_id)
            if ruta :
                presupuesto.comprobante_path = ruta
                presupuesto.id_estado = 2
                db.session.commit()
                flash('Comprobante actualizado correctamente.', 'success')
                redirect(url_for('listar.presupuesto_estudio', estudio_id=estudio_id))
            else:
                redirect(url_for('listar.presupuesto_estudio', estudio_id=estudio_id))
        else:
            flash('No se ha seleccionado un archivo.', 'error')
            redirect(url_for('listar.presupuesto_estudio', estudio_id=estudio_id))
            
    # Renderizar la plantilla con el presupuesto y su comprobante
    return render_template(
        'administrador/presupuesto_estudio.html',
        estudio=estudio,
        presupuesto=presupuesto,
        comprobante_path=presupuesto.comprobante_path
    )


@bp.route('/mis_turnos', methods=['GET'])
@verificar_autenticacion
@actualizar_turnos_vencidos
@verificar_rol(5)
def mis_turnos():
    id_usuario = session.get('user_id')
    
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        flash('Usuario no encontrado.', 'error')
        return redirect(url_for('root.index_get'))
    
    turnos = usuario.turnos  # Relación definida en el modelo Usuario

    for turno in turnos:
        # Obtener el estado como nombre
        estado = Estado.query.get(turno.estado)
        turno.estado_nombre = estado.nombre if estado else 'Desconocido'
        
        # Obtener detalles del estudio relacionado
        estudio = Estudio.query.get(turno.id_estudio)
        turno.estudio_id = estudio.id if estudio else 'Desconocido'
        turno.estudio_tipo = estudio.tipo_estudio if estudio else 'Desconocido'
        turno.estudio_fecha = estudio.fecha_solicitud.strftime('%d/%m/%Y') if estudio else 'Desconocido'

    return render_template('paciente/mis_turnos.html', turnos=turnos)

@bp.route('/cancelar_turno/<int:turno_id>', methods=['POST'])
@verificar_autenticacion
@verificar_rol(5)
def cancelar_turno(turno_id):
    turno = Turno.query.get(turno_id)
    if not turno:
        flash('Turno no encontrado.', 'error')
        return redirect(url_for('listar.mis_turnos'))
    
    if turno.estado == 5:  # Si ya está cancelado
        flash('El turno ya está cancelado.', 'info')
        return redirect(url_for('listar.mis_turnos'))

    # Cambiar estado a CANCELADO
    turno.estado = 5
    turno.estado_interno = 'LIBRE'
    estudio = Estudio.query.filter_by(id = turno.id_estudio).first()
    estudio.historial.append(HistorialEstado(estado="TURNO CANCELADO"))
    db.session.commit()
    Notificacion.send_mail(estudio.id_paciente, f"Ha cancelado el turno para el estudio {estudio.id}. exitosamente. Recuerde que puede solicitar un nuevo turno en cualquier momento.")
    flash('Turno cancelado exitosamente.', 'success')
    return redirect(url_for('listar.mis_turnos'))
