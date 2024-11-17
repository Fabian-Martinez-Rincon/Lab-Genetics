from flask import render_template, redirect, url_for, flash, Blueprint, request, jsonify
from src.core.models.laboratorio import Laboratorio
from src.core.models.turno import Turno
from src.core.models.estudio import Estudio
from src.core.models.historialEstado import HistorialEstado
from src.core.models.database import db
from datetime import datetime

bp = Blueprint('solicitar_turno', __name__)

@bp.route('/solicitar_turno/<id_estudio>', methods=['GET', 'POST'])
def solicitar_turno(id_estudio):
    estudio = Estudio.query.filter_by(id=id_estudio).first()
    min_fecha = (datetime.utcnow()).strftime('%Y-%m-%d')
    address = [addr[0] for addr in Laboratorio.query.with_entities(Laboratorio.address).distinct().all()]
    
    if request.method == 'POST':
        laboratorio_id = request.form.get('laboratorio_id')
        fecha_seleccionada = request.form.get('fecha')
        hora_seleccionada = request.form.get('hora')

        if not laboratorio_id or not fecha_seleccionada or not hora_seleccionada:
            flash("Por favor, selecciona todos los campos.", "error")
            return redirect(url_for('solicitar_turno.solicitar_turno', id_estudio=id_estudio))

        fecha_seleccionada = datetime.strptime(fecha_seleccionada, '%Y-%m-%d').date()
        hora_seleccionada = datetime.strptime(hora_seleccionada, '%H:%M').time()

        if fecha_seleccionada < datetime.utcnow().date():
            flash("La fecha seleccionada debe ser posterior a hoy.", "error")
            return redirect(url_for('solicitar_turno.solicitar_turno', id_estudio=id_estudio))
        
        if fecha_seleccionada.weekday() in [5, 6]:  # 5 = Sábado, 6 = Domingo
            flash("No se permiten turnos los sábados o domingos. Por favor selecciona otra fecha.", "error")
            return redirect(url_for('solicitar_turno.solicitar_turno', id_estudio=id_estudio))
        turno_existente = Turno.query.filter_by(
            id_laboratorio=laboratorio_id,
            fecha=fecha_seleccionada,
            hora=hora_seleccionada
        ).first()

        if (turno_existente)and(turno_existente.estado_interno=="OCUPADO"):
            flash("Este turno ya está ocupado. Por favor, elige otro.", "error")
            return redirect(url_for('solicitar_turno.solicitar_turno', id_estudio=id_estudio))

        nuevo_turno = Turno(
            id_paciente=estudio.id_paciente,
            id_laboratorio=laboratorio_id,
            fecha=fecha_seleccionada,
            hora=hora_seleccionada,
            id_estudio=estudio.id,
            estado=1,
            estado_interno="OCUPADO"
        )

        db.session.add(nuevo_turno)
        estudio.historial.append(HistorialEstado(estado="ESPERANDO EXTRACCION"))
        db.session.commit()

        flash("¡Turno solicitado con éxito!", "success")
        return redirect(url_for('listar.detalle_estudio', estudio_id=id_estudio))

    return render_template(
        'paciente/solicitar_turno.html',
        id_estudio=id_estudio,
        address=address,
        min_fecha=min_fecha
    )


@bp.route('/get_laboratorios', methods=['POST'])
def get_laboratorios():
    address = request.json.get('address')
    laboratorios = Laboratorio.query.filter_by(address=address, estado='ACTIVO').all()
    return jsonify([{'id': lab.id, 'nombre': lab.nombre, 'direccion': lab.direccion} for lab in laboratorios])


@bp.route('/get_horarios_ocupados', methods=['POST'])
def get_horarios_ocupados():
    try:
        laboratorio_id = request.json.get('laboratorio_id')
        fecha = request.json.get('fecha')
        print(f"Datos recibidos: laboratorio_id={laboratorio_id}, fecha={fecha}")
        if not laboratorio_id or not fecha:
            return jsonify({"error": "Datos incompletos"}), 400

        turnos_ocupados = Turno.query.filter_by(id_laboratorio=laboratorio_id, fecha=fecha , estado_interno="OCUPADO").all()
        horarios = [turno.hora.strftime('%H:%M') for turno in turnos_ocupados]
        return jsonify(horarios), 200

    except Exception as e:
        print(f"Error al obtener horarios ocupados: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
