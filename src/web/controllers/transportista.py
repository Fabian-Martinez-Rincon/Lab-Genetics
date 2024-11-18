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
    pedidos_pendientes = db.session.query(
        Pedido.id, Pedido.estado, Pedido.fecha, Laboratorio.nombre, Laboratorio.direccion,
        Laboratorio.telefono, Laboratorio.latitud, Laboratorio.longitud
    ).join(Laboratorio, Pedido.id_laboratorio == Laboratorio.id).filter(Pedido.estado == 'PENDIENTE').all()

    # Convertir pedidos pendientes a JSON para el mapa
    laboratorios_json = [
        {
            'nombre': pedido.nombre,
            'direccion': pedido.direccion,
            'telefono': pedido.telefono,
            'latitud': pedido.latitud,
            'longitud': pedido.longitud
        }
        for pedido in pedidos_pendientes
    ]

    return render_template(
        'laboratorio/listar_pedidos_pendientes.html',
        pedidos=pedidos_pendientes,
        laboratorios_json=laboratorios_json
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


#from flask import render_template, jsonify

import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos puntos geográficos usando la fórmula de Haversine.
    :param lat1, lon1: Coordenadas del primer punto
    :param lat2, lon2: Coordenadas del segundo punto
    :return: Distancia en kilómetros
    """
    R = 6371  # Radio de la Tierra en kilómetros
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@bp.route('/recorrido_pedidos_pendientes', methods=['GET'])
@verificar_autenticacion
@verificar_rol(6)  # Rol correspondiente al transportista o usuario autorizado
def recorrido_pedidos_pendientes():
    # Consultar pedidos pendientes y unirlos con la información del laboratorio
    pedidos_pendientes = db.session.query(
        Pedido.id, Pedido.estado, Pedido.fecha, Laboratorio.nombre, Laboratorio.direccion,
        Laboratorio.telefono, Laboratorio.latitud, Laboratorio.longitud
    ).join(Laboratorio, Pedido.id_laboratorio == Laboratorio.id).filter(Pedido.estado == 'PENDIENTE').all()

    # Punto de referencia (ejemplo: la ubicación actual del transportista)
    punto_inicial = {'lat': -34.6037, 'lon': -58.3816}  # Buenos Aires, como ejemplo

    # Convertir los resultados a JSON y calcular distancias
    laboratorios_json = [
        {
            'nombre': pedido.nombre,
            'direccion': pedido.direccion,
            'telefono': pedido.telefono,
            'latitud': pedido.latitud,
            'longitud': pedido.longitud,
            'distancia': haversine(punto_inicial['lat'], punto_inicial['lon'], pedido.latitud, pedido.longitud)
        }
        for pedido in pedidos_pendientes
    ]

    # Ordenar los laboratorios por distancia al punto inicial
    laboratorios_json.sort(key=lambda lab: lab['distancia'])

    return render_template(
        'laboratorio/recorrido_laboratorios.html',
        laboratorios_json=laboratorios_json
    )
