from flask import Blueprint, flash, redirect, url_for
from src.core.models.turno import Turno
from src.core.models.database import db
from src.core.models.notificacion import Notificacion
from src.core.models.historialEstado import HistorialEstado
from src.core.models.estudio import Estudio
from src.core.models.pedido import Pedido
from src.web.controllers.utils import verificar_autenticacion, verificar_rol
from datetime import datetime, timedelta
from src.core.models.usuario import Usuario

bp = Blueprint("confirmar_turno", __name__)
@verificar_autenticacion
@verificar_rol(3)
@bp.route('/confirmar_turno/<int:turno_id>', methods=['POST'])
def confirmar_turno(turno_id):
    turno = Turno.query.filter_by(id=turno_id).first()
    if not turno:
        flash('Turno no encontrado.', 'error')
        return redirect(url_for('listar.listar_turnos'))
    if turno.fecha != datetime.now().date():
        flash('Solamente puedes confirmar los turnos del dia', 'error')
        return redirect(url_for('listar.listar_turnos'))
    turno.estado = 3
    turno.estado_interno = "FINALIZADO"
    estudio = Estudio.query.filter_by(id=turno.id_estudio).first()
    estudio.historial.append(HistorialEstado(estado="ESPERANDO ENVIO A CENTRAL"))
    Notificacion.send_mail(estudio.id_paciente, f"Se ha confirmado la extraccion para el estudio: {estudio.id}. El estudio se encuentra en espera de ser enviado a la central.")
    fecha_mañana = turno.fecha + timedelta(days=1)
    pedido_mañana = Pedido.query.filter_by(id_laboratorio=turno.id_laboratorio, fecha=fecha_mañana).first()
    if not pedido_mañana:
        pedido_mañana = Pedido(id_laboratorio=turno.id_laboratorio, fecha=fecha_mañana, estado="PENDIENTE")
        db.session.add(pedido_mañana)
    pedido_mañana.estudios.append(estudio)
    db.session.commit()
    flash('Turno confirmado correctamente.', 'success')
    return redirect(url_for('listar.listar_turnos'))
    