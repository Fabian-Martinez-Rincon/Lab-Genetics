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
    estudios = Estudio.query \
    .join(HistorialEstado, Estudio.id == HistorialEstado.estudio_id) \
    .filter(HistorialEstado.estado == "ESPERANDO ENVIO AL EXTERIOR") \
    .all()
    cantidad_estudios = len(estudios)
    return render_template('administrador/espera_envios.html', estudios=estudios, cantidad_estudios=cantidad_estudios)