from flask import Flask, render_template, Blueprint, request, redirect, url_for
from src.core.models.laboratorio import Laboratorio
from src.core.models.database import db
from src.web.controllers.utils import verificar_autenticacion
bp = Blueprint('listar_laboratorios', __name__)
@verificar_autenticacion
@bp.route('/listar_laboratorios', methods=['GET', 'POST'])
def listar_laboratorios():
    if request.method == 'POST':
        laboratorio_id = request.form.get('laboratorio_id')
        nuevo_estado = request.form.get('estado')

        # Actualiza el estado del laboratorio
        laboratorio = Laboratorio.query.get(laboratorio_id)
        if laboratorio:
            laboratorio.estado = nuevo_estado
            db.session.commit()

        return redirect(url_for('listar_laboratorios.listar_laboratorios'))

    laboratorios = Laboratorio.query.all()
    
    return render_template('owner/listar_laboratorios.html', laboratorios=laboratorios)

