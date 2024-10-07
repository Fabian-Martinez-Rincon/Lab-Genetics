from flask import Flask, render_template, Blueprint
from src.core.models.laboratorio import Laboratorio

bp = Blueprint('listar_laboratorios', __name__)

@bp.route('/listar_laboratorios')
def listar_laboratorios():
    laboratorios = Laboratorio.query.all()
    
    return render_template('owner/listar_laboratorios.html', laboratorios=laboratorios)

