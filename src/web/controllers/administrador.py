from flask import render_template, Blueprint, flash, redirect, url_for
from src.core.models.database import db
from src.web.controllers.utils import verificar_rol, verificar_autenticacion, actualizar_presupuestos_vencidos
from src.core.models.estudio import Estudio
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from src.core.models.historialEstado import HistorialEstado

bp = Blueprint('administrador', __name__)

@bp.route('/presupuestos_solicitados', methods=['GET'])
@verificar_autenticacion
@actualizar_presupuestos_vencidos
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


@bp.route('/presupuestos_pagados', methods=['GET'])
@verificar_autenticacion
@verificar_rol(2)
def presupuestos_pagados():
    from src.core.models.presupuesto import Presupuesto
    from src.core.models.estado import Estado
    from src.core.models.estudio import Estudio

    # Obtén el ID del estado "PAGADO"
    estado_pagado = Estado.query.filter_by(nombre="PAGADO").first()
    if not estado_pagado:
        flash('El estado "PAGADO" no está configurado.', 'error')
        return redirect(url_for('administrador.presupuestos_solicitados'))
    
    # Consulta los presupuestos con el estado "PAGADO"
    presupuestos = Presupuesto.query.filter_by(id_estado=estado_pagado.id).all()

    # Agrega el ID del estudio relacionado a cada presupuesto
    presupuestos_con_estudios = []
    for presupuesto in presupuestos:
        estudio = Estudio.query.filter_by(id_presupuesto=presupuesto.id).first()
        presupuestos_con_estudios.append({
            'id': presupuesto.id,
            'detalle': presupuesto.Detalle,
            'monto_final': presupuesto.montoFinal,
            'comprobante_path': presupuesto.comprobante_path,
            'id_estudio': estudio.id if estudio else None  # ID del estudio relacionado, si existe
        })

    return render_template(
        'administrador/presupuestos_pagados.html',
        presupuestos=presupuestos_con_estudios
    )


# @bp.route('/presupuestos/<int:presupuesto_id>', methods=['GET'])
# @verificar_autenticacion
# @verificar_rol(2)
# def detalle_presupuesto(presupuesto_id):
#     from src.core.models.presupuesto import Presupuesto

#     # Obtén el presupuesto por ID
#     presupuesto = Presupuesto.query.get(presupuesto_id)
#     if not presupuesto:
#         flash('El presupuesto no existe.', 'error')
#         return redirect(url_for('administrador.presupuestos_pagados'))
    
#     return render_template('administrador/detalle_presupuesto.html', presupuesto=presupuesto)

@bp.route('/presupuestos_aceptados', methods=['GET'])
@verificar_autenticacion
@verificar_rol(2)
def presupuestos_aceptados():
    from src.core.models.presupuesto import Presupuesto
    from src.core.models.estado import Estado
    from src.core.models.estudio import Estudio

    # Obtén el ID del estado "ACEPTADO"
    estado_aceptado = Estado.query.filter_by(nombre="ACEPTADO").first()
    if not estado_aceptado:
        flash('El estado "ACEPTADO" no está configurado.', 'error')
        return redirect(url_for('administrador.presupuestos_solicitados'))
    
    # Consulta los presupuestos con el estado "ACEPTADO"
    presupuestos = Presupuesto.query.filter_by(id_estado=estado_aceptado.id).all()

    # Agrega el ID del estudio relacionado a cada presupuesto
    presupuestos_con_estudios = []
    for presupuesto in presupuestos:
        estudio = Estudio.query.filter_by(id_presupuesto=presupuesto.id).first()
        presupuestos_con_estudios.append({
            'id': presupuesto.id,
            'detalle': presupuesto.Detalle,
            'monto_final': presupuesto.montoFinal,
            'comprobante_path': presupuesto.comprobante_path,
            'id_estudio': estudio.id if estudio else None  # ID del estudio relacionado, si existe
        })

    return render_template(
        'administrador/presupuestos_aceptados.html',
        presupuestos=presupuestos_con_estudios
    )
