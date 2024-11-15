from flask import render_template, Blueprint, flash, redirect, url_for
from src.core.models.database import db
from src.web.controllers.utils import verificar_rol, verificar_autenticacion
from src.core.models.estudio import Estudio

from src.core.models.historialEstado import HistorialEstado

bp = Blueprint('administrador', __name__)

@bp.route('/presupuestos_solicitados', methods=['GET'])
@verificar_autenticacion
@verificar_rol(2)
def mis_estudios_solicitados():
    # Subconsulta para obtener el último estado de cada estudio
    subquery = db.session.query(
        HistorialEstado.estudio_id,
        HistorialEstado.estado
    ).filter(HistorialEstado.estado == "SOLICITADO")\
    .order_by(HistorialEstado.estudio_id, HistorialEstado.fecha_hora.desc())\
    .distinct(HistorialEstado.estudio_id).subquery()

    # Obtener todos los estudios cuyo último estado sea "SOLICITADO"
    estudios = db.session.query(Estudio).join(subquery, Estudio.id == subquery.c.estudio_id).all()

    # Añadir el estado "SOLICITADO" para cada estudio
    for estudio in estudios:
        estudio.estado_nombre = "SOLICITADO"

    return render_template('administrador/presupuestos_solicitados.html', estudios=estudios)

@bp.route('/generar_presupuesto/<estudio_id>', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(2)
def generar_presupuesto(estudio_id):
    # Aquí puedes agregar la lógica para generar el presupuesto del estudio con el ID dado.
    estudio = Estudio.query.get(estudio_id)
    if not estudio:
        flash('Estudio no encontrado.', 'error')
        return redirect(url_for('administrador.mis_estudios_solicitados'))
    
    # Lógica para generar el presupuesto (esto es solo un ejemplo)
    # Generar un nuevo registro de presupuesto o actualizar uno existente
    flash('Presupuesto generado exitosamente.', 'success')
    return redirect(url_for('administrador.mis_estudios_solicitados'))
