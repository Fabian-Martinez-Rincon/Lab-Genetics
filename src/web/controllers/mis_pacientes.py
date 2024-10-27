from flask import render_template, request, Blueprint, flash, redirect, url_for, session
from src.web.controllers.utils import verificar_rol, verificar_autenticacion
from flask_login import current_user
from src.core.models.usuario import Usuario
from src.core.models.database import db

bp = Blueprint('mis_pacientes', __name__)

@bp.route('/mis_pacientes', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(4)
def mis_pacientes():
    # Obtén los pacientes asociados con el médico actual
    id_medico = session.get('user_id')
    pacientes = Usuario.query.filter_by(id_medico=id_medico).all()
    return render_template('medico/mis_pacientes.html', pacientes=pacientes)
