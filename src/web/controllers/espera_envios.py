from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.web.controllers.utils import verificar_autenticacion, verificar_rol
from src.core.models.estudio import Estudio
from src.core.models.database import db
from src.core.models.historialEstado import HistorialEstado
from sqlalchemy.sql import func
from sqlalchemy.orm import aliased
from src.core.models.notificacion import Notificacion
from src.core.models.exterior import Exterior

bp = Blueprint("espera_envios", __name__)
@verificar_autenticacion
@verificar_rol(2)
@bp.route('/espera_envios', methods=['GET','POST'])
def espera_envios():
    estudios = Estudio.query \
    .join(HistorialEstado, Estudio.id == HistorialEstado.estudio_id) \
    .filter(HistorialEstado.estado == "ESPERANDO ENVIO AL EXTERIOR") \
    .all()
    cantidad_estudios = len(estudios)
    if request.method == 'POST':
        primeros_estudios = Estudio.query \
        .join(HistorialEstado, Estudio.id == HistorialEstado.estudio_id) \
        .filter(HistorialEstado.estado == "ESPERANDO ENVIO AL EXTERIOR") \
        .filter(Estudio.fecha_ingreso_central != None) \
        .order_by(Estudio.fecha_ingreso_central.asc()) \
        .limit(100) \
        .all()
        if not primeros_estudios or len(primeros_estudios) != 100:
            flash('No hay estudios para enviar al exterior. Solo Se pueden enviar de a 100', 'error')
            return redirect(url_for('espera_envios.espera_envios'))
        exterior = Exterior(
            estado="ENVIADO AL EXTERIOR"
        )
        db.session.add(exterior)
        for estudio in primeros_estudios:
            estudio.historial.append(HistorialEstado(estado="ENVIADO AL EXTERIOR"))
            Notificacion.send_mail(estudio.id_paciente, f"Su estudio {estudio.id} ha sido enviado al exterior.")
            exterior.estudios.append(estudio)
        db.session.commit()
        flash('Estudios envios exitosamente.', 'success')
        return redirect(url_for('espera_envios.espera_envios'))
    
    return render_template('administrador/espera_envios.html', estudios=estudios, cantidad_estudios=cantidad_estudios)