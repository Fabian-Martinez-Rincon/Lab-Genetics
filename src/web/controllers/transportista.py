from flask import render_template, Blueprint, flash, redirect, url_for
from src.core.models.database import db
from src.web.controllers.utils import verificar_rol, verificar_autenticacion, actualizar_presupuestos_vencidos
from src.core.models.estudio import Estudio
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from src.core.models.historialEstado import HistorialEstado
from src.core.models.pedido import Pedido
from src.core.models.laboratorio import Laboratorio

bp = Blueprint('transportista', __name__)

@bp.route('/listar_pedidos_pendientes', methods=['GET'])
@verificar_autenticacion
@verificar_rol(6)  # Asegúrate de que solo roles específicos puedan acceder
def listar_pedidos_pendientes():
    # Filtrar pedidos en estado "Pendiente"
    pedidos_pendientes = Pedido.query.filter_by(estado='Pendiente').order_by(Pedido.fecha.asc()).all()

    return render_template('laboratorio/listar_pedidos_pendientes.html', pedidos=pedidos_pendientes)



@bp.route('/detalle_pedido/<int:pedido_id>', methods=['GET'])
@verificar_autenticacion
@verificar_rol(6)  # Suponiendo que el rol 3 corresponde al laboratorio
def detalle_pedido(pedido_id):
    # Obtener el pedido
    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        flash('Pedido no encontrado.', 'error')
        return redirect(url_for('listar_pedidos'))  # Redirige a la lista de pedidos

    # Obtener el laboratorio asociado
    laboratorio = Laboratorio.query.get(pedido.id_laboratorio)

    # Preparar los estudios asociados al pedido
    estudios = pedido.estudios

    return render_template(
        'laboratorio/detalle_pedido.html',
        pedido=pedido,
        laboratorio=laboratorio,
        estudios=estudios
    )
