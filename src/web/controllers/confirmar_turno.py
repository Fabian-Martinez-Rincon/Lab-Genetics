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
    turno.estado = 3
    turno.estado_interno = "FINALIZADO"
    estudio = Estudio.query.filter_by(id=turno.id_estado).first()
    estudio.historial.append(HistorialEstado(estado="ESPERANDO ENVIO A CENTRAL"))
    Notificacion.send_mail(estudio.id_paciente, f"El Turno para el estudio {estudio.id} ha sido confirmado.")
    fecha_mañana = turno.fecha + timedelta(days=1)
    pedido_mañana = Pedido.query.filter_by(id_laboratorio=turno.id_laboratorio, fecha=fecha_mañana).first()
    if not pedido_mañana:
        pedido_mañana = Pedido(id_laboratorio=turno.id_laboratorio, fecha=fecha_mañana, estado="PENDIENTE")
        db.session.add(pedido_mañana)
    pedido_mañana.estudios.append(estudio)
    transportista = Usuario.query.filter_by(id_rol=6).first()
    db.session.commit()
    