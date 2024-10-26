from flask import render_template, request, Blueprint, flash, redirect, url_for, session
from src.core.models.usuario import Usuario
from src.core.models.database import db
from src.web.controllers.utils import verificar_autenticacion, verificar_rol
bp = Blueprint('reasignar', __name__)

@bp.route('/reasignar', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(4)
def reasignar():
    if request.method == 'POST':
        dni = request.form.get('dni')
        id_medico_nuevo = session.get('user_id')
        paciente = Usuario.query.filter_by(dni=dni).first()
        if not paciente:
            flash('No se encontró ningún paciente con ese DNI.', 'error')
            return render_template('medico/reasignar.html')

        # Reasignar el paciente
        try:
            paciente.id_medico = id_medico_nuevo
            db.session.commit()
            flash('Paciente reasignado exitosamente.', 'success')
            return redirect(url_for('root.index_get'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al reasignar al paciente: {e}', 'error')
            return render_template('medico/reasignar.html')

    return render_template('medico/reasignar.html')
