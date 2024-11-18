from flask import Blueprint, flash, redirect, url_for
from src.core.models.turno import Turno
from src.core.models.database import db
from src.core.models.notificacion import Notificacion
from src.core.models.historialEstado import HistorialEstado
from src.core.models.estudio import Estudio
from src.core.models.pedido import Pedido
bp = Blueprint("confirmar_turno", __name__)

@bp.route('/confirmar_turno', methods=['GET', 'POST'])
def confirmar_turno(turno_id):
    turno = Turno.query.filter_by(id=turno_id).first()
    if not turno:
        flash('Turno no encontrado.', 'error')