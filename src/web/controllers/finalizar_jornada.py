from flask import Blueprint, request, jsonify, flash, redirect, url_for
from src.core.models.pedido import Pedido
from src.core.models.database import db
from src.web.controllers.utils import verificar_autenticacion, verificar_rol
from sqlalchemy import and_
from datetime import datetime
from src.core.models.historialEstado import HistorialEstado
from src.core.models.estudio import Estudio
from src.core.models.notificacion import Notificacion

bp = Blueprint("finalizar_jornada", __name__)
@verificar_autenticacion
@verificar_rol(6)
@bp.route('/finalizar_jornada', methods=['POST'])
def finalizar_jornada():
    pedidos_finalizados = Pedido.query.filter(
        and_(
            Pedido.estado == 'FINALIZADO',
            Pedido.fecha_ingreso_central == None  
        )
    ).all()
    for pedido in pedidos_finalizados:
        pedido.fecha_ingreso_central = datetime.now().date()
        for estudio in pedido.estudios:
            estudio.historial.append(HistorialEstado(estado="ESPERANDO ENVIO AL EXTERIOR"))
            estudio.fecha_ingreso_central = datetime.now().date()
            Notificacion.send_mail(estudio.id_paciente, f"El estudio {estudio.id} ya se encuentra en espera de ser enviado al exterior.")
    db.session.commit()
    flash('Jornada finalizada correctamente.', 'success')
    return redirect(url_for('transportista.listar_pedidos_pendientes')) 