from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.web.controllers.utils import verificar_autenticacion, verificar_rol, enviar_estudios_automaticamente
from src.core.models.estudio import Estudio
from src.core.models.database import db
from src.core.models.historialEstado import HistorialEstado
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased
from src.core.models.notificacion import Notificacion
from src.core.models.exterior import Exterior


bp = Blueprint("espera_envios", __name__)

@enviar_estudios_automaticamente
@verificar_autenticacion
@verificar_rol(2)
@bp.route('/espera_envios', methods=['GET','POST'])
def espera_envios():
    ultimo_estado_subquery = (
            db.session.query(
                HistorialEstado.estudio_id,
                func.max(HistorialEstado.fecha_hora).label("ultima_fecha")
            )
            .group_by(HistorialEstado.estudio_id)
            .subquery()
        )
    ultimo_estado = aliased(HistorialEstado)
    estudios = (
        db.session.query(Estudio)
        .join(ultimo_estado, Estudio.id == ultimo_estado.estudio_id)
        .join(ultimo_estado_subquery, 
            (ultimo_estado.estudio_id == ultimo_estado_subquery.c.estudio_id) &
            (ultimo_estado.fecha_hora == ultimo_estado_subquery.c.ultima_fecha))
        .filter(ultimo_estado.estado == "ESPERANDO ENVIO AL EXTERIOR")
        .filter(Estudio.fecha_ingreso_central != None)
        .order_by(Estudio.fecha_ingreso_central.asc())
        .all()
    )
    cantidad_estudios = len(estudios)
    return render_template('administrador/espera_envios.html', estudios=estudios, cantidad_estudios=cantidad_estudios)