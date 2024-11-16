from flask import render_template, Blueprint, flash, redirect, url_for
from src.core.models.database import db
from src.web.controllers.utils import verificar_rol, verificar_autenticacion
from src.core.models.estudio import Estudio
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from src.core.models.historialEstado import HistorialEstado

bp = Blueprint('administrador', __name__)

@bp.route('/presupuestos_solicitados', methods=['GET'])
@verificar_autenticacion
@verificar_rol(2)
def presupuestos_solicitados():
    # Subconsulta para obtener la última fecha por estudio_id
    subquery_max_date = db.session.query(
        HistorialEstado.estudio_id,
        func.max(HistorialEstado.fecha_hora).label('ultima_actualizacion')
    ).group_by(HistorialEstado.estudio_id).subquery()

    # Subconsulta para obtener el estado asociado a la última fecha
    subquery_estado = db.session.query(
        HistorialEstado.estudio_id,
        HistorialEstado.estado
        ).join(
            subquery_max_date,
            (HistorialEstado.estudio_id == subquery_max_date.c.estudio_id) &
            (HistorialEstado.fecha_hora == subquery_max_date.c.ultima_actualizacion)
        ).subquery()

    # Consulta final
    estudios = db.session.query(Estudio).join(
        subquery_estado,
        Estudio.id == subquery_estado.c.estudio_id
    ).filter(
        subquery_estado.c.estado == 'SOLICITADO',
        Estudio.id_presupuesto == None
    ).all()

    # Añadir el estado "SOLICITADO" para cada estudio
    for estudio in estudios:
        estudio.estado_nombre = "SOLICITADO"

    return render_template('administrador/presupuestos_solicitados.html', estudios=estudios)
# @bp.route('/generar_presupuesto/<estudio_id>', methods=['GET', 'POST'])
# @verificar_autenticacion
# @verificar_rol(2)
# def generar_presupuesto(estudio_id):
#     # Aquí puedes agregar la lógica para generar el presupuesto del estudio con el ID dado.
#     estudio = Estudio.query.get(estudio_id)
#     if not estudio:
#         flash('Estudio no encontrado.', 'error')
#         return redirect(url_for('administrador.mis_estudios_solicitados'))
    
#     # Lógica para generar el presupuesto (esto es solo un ejemplo)
#     # Generar un nuevo registro de presupuesto o actualizar uno existente
#     flash('Presupuesto generado exitosamente.', 'success')
#     return redirect(url_for('administrador.mis_estudios_solicitados'))
