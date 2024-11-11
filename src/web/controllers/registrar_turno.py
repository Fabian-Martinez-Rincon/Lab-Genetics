from flask import Blueprint, render_template, redirect, url_for, flash, request
from src.core.models.database import db
from src.web.formularios.solicitar_turno import RegisterTurnoForm
from src.core.models.laboratorio import Laboratorio
from flask_login import current_user
from src.core.models.turno import Turno
from src.web.controllers.utils import verificar_autenticacion
bp = Blueprint("registrar_turno", __name__)

@verificar_autenticacion
@bp.route('/registrar_turno/<int:laboratorio_id>', methods=['GET', 'POST'])
def register_turno(laboratorio_id):
    form = RegisterTurnoForm()
    laboratorio = Laboratorio.query.get(laboratorio_id)
    if laboratorio:
        form.id_laboratorio.data = laboratorio.nombre
        form.id_laboratorio.render_kw = {'readonly': True}
    else:
        return "Laboratorio no encontrado", 404

    if form.validate_on_submit():
        new_turno = Turno(
            id_paciente=current_user.id,
            id_laboratorio=laboratorio.id,
            id_estudio=form.id_estudio.data,
            estado=form.estado.data,
            fecha=form.fecha.data,
            hora=form.hora.data,
        )
        db.session.add(new_turno)
        db.session.commit()
        return redirect(url_for('some_success_route'))

    return render_template('registrar_turno.html', form=form, laboratorio=laboratorio)
