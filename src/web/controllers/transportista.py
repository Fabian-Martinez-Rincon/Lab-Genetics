from flask import render_template, Blueprint, flash, redirect, url_for
from src.core.models.database import db
from src.web.controllers.utils import verificar_rol, verificar_autenticacion
from src.core.models.pedido import Pedido
from src.core.models.laboratorio import Laboratorio

bp = Blueprint('transportista', __name__)

from datetime import date

@bp.route('/listar_pedidos_pendientes', methods=['GET'])
@verificar_autenticacion
@verificar_rol(6)  # Asegúrate de que solo roles específicos puedan acceder
def listar_pedidos_pendientes():
    # Filtrar el pedido en estado 'EN PROCESO'
    pedido_en_proceso = db.session.query(
        Pedido.id, Pedido.estado, Pedido.fecha, Laboratorio.nombre, Laboratorio.direccion,
        Laboratorio.telefono, Laboratorio.latitud, Laboratorio.longitud
    ).join(Laboratorio, Pedido.id_laboratorio == Laboratorio.id).filter(
        Pedido.estado == 'EN PROCESO'
    ).first()

    # Filtrar pedidos pendientes con fecha hasta hoy
    hoy = date.today()
    pedidos_pendientes = db.session.query(
        Pedido.id, Pedido.estado, Pedido.fecha, Laboratorio.nombre, Laboratorio.direccion,
        Laboratorio.telefono, Laboratorio.latitud, Laboratorio.longitud
    ).join(Laboratorio, Pedido.id_laboratorio == Laboratorio.id).filter(
        Pedido.estado == 'PENDIENTE',
        Pedido.fecha <= hoy
    ).order_by(Pedido.fecha.asc()).all()

    # Filtrar pedidos finalizados
    pedidos_finalizados = db.session.query(
        Pedido.id, Pedido.estado, Pedido.fecha, Laboratorio.nombre, Laboratorio.direccion,
        Laboratorio.telefono, Laboratorio.latitud, Laboratorio.longitud
    ).join(Laboratorio, Pedido.id_laboratorio == Laboratorio.id).filter(
        Pedido.estado == 'FINALIZADO'
    ).order_by(Pedido.fecha.asc()).all()

    # Construir el listado final
    pedidos = []
    if pedido_en_proceso:
        pedidos.append(pedido_en_proceso)
    pedidos.extend(pedidos_pendientes)
    pedidos.extend(pedidos_finalizados)

    # Convertir pedidos a JSON para el mapa, excluyendo los FINALIZADOS
    laboratorios_json = [
        {
            'nombre': pedido.nombre,
            'direccion': pedido.direccion,
            'telefono': pedido.telefono,
            'latitud': pedido.latitud,
            'longitud': pedido.longitud
        }
        for pedido in pedidos if pedido.estado != 'FINALIZADO'
    ]

    return render_template(
        'laboratorio/listar_pedidos_pendientes.html',
        pedidos=pedidos,
        laboratorios_json=laboratorios_json,
        pedido_en_proceso=pedido_en_proceso
    )




@bp.route('/detalle_pedido/<int:pedido_id>', methods=['GET'])
@verificar_autenticacion
@verificar_rol(6)  # Rol correspondiente al transportista o laboratorio
def detalle_pedido(pedido_id):
    # Obtener el pedido
    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        flash('Pedido no encontrado.', 'error')
        return redirect(url_for('listar_pedidos'))  # Redirige a la lista de pedidos

    # Obtener el laboratorio asociado
    laboratorio = Laboratorio.query.get(pedido.id_laboratorio)
    if not laboratorio:
        flash('Laboratorio no encontrado.', 'error')
        return redirect(url_for('listar_pedidos'))

    # Preparar los estudios asociados al pedido
    estudios = pedido.estudios

    return render_template(
        'laboratorio/detalle_pedido.html',
        pedido=pedido,
        laboratorio=laboratorio,
        estudios=estudios
    )

@bp.route('/comenzar_viaje/<int:pedido_id>', methods=['POST'])
@verificar_autenticacion
@verificar_rol(6)
def comenzar_viaje(pedido_id):
    pedido_en_proceso = Pedido.query.filter_by(estado='EN PROCESO').first()
    if pedido_en_proceso:
        flash(f'Ya tienes un pedido en estado "EN PROCESO" (Pedido #{pedido_en_proceso.id}). Finaliza ese viaje antes de comenzar otro.', 'error')
        return redirect(url_for('transportista.listar_pedidos_pendientes'))
    
    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        flash('Pedido no encontrado.', 'error')
        return redirect(url_for('transportista.listar_pedidos_pendientes'))

    if pedido.estado == 'PENDIENTE':
        pedido.estado = 'EN PROCESO'
        db.session.commit()
        flash(f'El estado del pedido #{pedido.id} ha cambiado a "EN PROCESO".', 'success')
    else:
        flash('El pedido no está en estado "Pendiente".', 'error')

    return redirect(url_for('transportista.listar_pedidos_pendientes'))


@bp.route('/empezar_jornada', methods=['POST'])
@verificar_autenticacion
@verificar_rol(6)
def empezar_jornada():
    flash("¡Jornada iniciada exitosamente!", "success")
    return redirect(url_for('transportista.listar_pedidos_pendientes'))


@bp.route('/terminar_jornada', methods=['POST'])
@verificar_autenticacion
@verificar_rol(6)
def terminar_jornada():
    flash("¡Jornada finalizada con éxito!", "success")
    return redirect(url_for('transportista.listar_pedidos_pendientes'))

@bp.route('/terminar_viaje/<int:pedido_id>', methods=['POST'])
@verificar_autenticacion
@verificar_rol(6)
def terminar_viaje(pedido_id):
    pedido = Pedido.query.get(pedido_id)
    if not pedido or pedido.estado != 'EN PROCESO':
        flash('No hay un viaje en curso para este pedido.', 'error')
        return redirect(url_for('transportista.listar_pedidos_pendientes'))
    
    pedido.estado = 'FINALIZADO'
    db.session.commit()
    flash(f'El pedido #{pedido.id} ha sido finalizado.', 'success')
    return redirect(url_for('transportista.listar_pedidos_pendientes'))
