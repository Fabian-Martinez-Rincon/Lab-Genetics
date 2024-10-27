from flask import render_template, request, Blueprint, abort, session, send_from_directory, current_app, flash
from flask_login import current_user
from src.core.models.usuario import Usuario
from src.web.controllers.utils import verificar_rol, verificar_autenticacion
import os
bp = Blueprint('ver_paciente', __name__)

@bp.route('/ver_paciente/<int:paciente_id>', methods=['GET'])
@verificar_autenticacion
@verificar_rol(4)
def ver_paciente(paciente_id):
    # Obtener el ID del médico actual
    id_medico = session.get('user_id')
    paciente = Usuario.query.filter_by(id=paciente_id, id_medico=id_medico).first()
    if not paciente:
        abort(404, description="Paciente no encontrado o no autorizado para ver este perfil.")

    return render_template('medico/ver_paciente.html', paciente=paciente)

@bp.route('/descargar_historia/<int:paciente_id>', methods=['GET'])
@verificar_autenticacion
@verificar_rol(4)
def descargar_historia(paciente_id):
    id_medico = session.get('user_id')
    paciente = Usuario.query.filter_by(id=paciente_id, id_medico=id_medico).first()
    if not paciente or not paciente.historia_path:
        flash('Paciente o historia clínica no encontrada o no autorizado.')
        return render_template('medico/mis_pacientes.html')

    relative_path = paciente.historia_path
    directory = os.path.join(current_app.root_path, '..', 'static', 'historia')
    full_path = os.path.join(directory, os.path.basename(relative_path))
    print(f"Ruta completa del archivo: {full_path}")

    if not os.path.isfile(full_path):
        flash('Archivo no encontrado en el servidor.')
        return render_template('medico/mis_pacientes.html')
    return send_from_directory(directory=directory, path=os.path.basename(relative_path), as_attachment=False)

