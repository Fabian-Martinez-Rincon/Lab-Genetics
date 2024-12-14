from flask import Blueprint, request, flash, redirect, url_for, render_template
from src.web.controllers.utils import verificar_autenticacion, verificar_rol
from src.core.models.database import db
from src.core.models.estudio import Estudio
from src.core.models.historialEstado import HistorialEstado
from src.core.models.presupuesto import Presupuesto
from src.core.models.notificacion import Notificacion
from datetime import datetime
bp = Blueprint('verificar_pago', __name__)

@bp.route('/verificar_pago/<estudio_id>', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(2)
def verificar_pago(estudio_id):
    estudio = Estudio.query.filter_by(id=estudio_id).first()
    presupuesto = Presupuesto.query.filter_by(id=estudio.id_presupuesto).first()
    if request.method == 'POST':
        accion = request.form.get('accion')
        observaciones = request.form.get('observaciones', '').strip()
        mail = " "
        if accion == 'aceptar':
            presupuesto.id_estado = 3  
            presupuesto.observaciones = None
            presupuesto.fecha_pago = datetime.now().date()
            estudio.historial.append(HistorialEstado(estado="PAGO ACEPTADO"))
            flash("Pago aceptado correctamente", "success")
            mail = "El pago de su estudio ha sido aceptado."
            db.session.commit()
        else:
            if not observaciones:
                flash("Debe proporcionar observaciones para rechazar el pago.", "error")
                return redirect(url_for('verificar_pago.verificar_pago', estudio_id=estudio_id))   
            presupuesto.id_estado = 4  
            presupuesto.observaciones = observaciones
            db.session.commit()
            flash("Pago rechazado correctamente", "success")
            mail = f"El pago de su estudio ha sido rechazado. Motivo: {observaciones}"
        Notificacion.send_mail(estudio.id_paciente, mail)
        
        return redirect(url_for('administrador.presupuestos_pagados'))
    return render_template(
        'administrador/presupuesto_estudio.html',
        estudio=estudio,
        presupuesto=presupuesto,
        comprobante_path=presupuesto.comprobante_path
    )