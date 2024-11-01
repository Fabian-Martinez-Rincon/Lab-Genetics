from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.core.models.usuario import Usuario
from src.core.models.estudio import Estudio
from src.core.models.patologia import Patologia
from src.core.models.historialEstado import HistorialEstado
from src.web.controllers.utils import verificar_rol, verificar_autenticacion
from datetime import datetime
from src.core.models.database import db
from .api import SnippetsAPI
import json
import os

bp = Blueprint('solicitar_estudio', __name__)

def cargar_sintomas_patologias():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "..", "core", "data", "patologias_sintomas.json")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

@bp.route('/solicitar_estudio/<int:paciente_id>', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(4)
def solicitar_estudio(paciente_id):
    id_medico = session.get('user_id')
    paciente = Usuario.query.filter_by(id=paciente_id, id_medico=id_medico).first()

    if not paciente:
        flash('Paciente no encontrado o Médico no autorizado para solicitar un estudio para el paciente.')
        return redirect(url_for('medico.mis_pacientes'))

    api = SnippetsAPI()  
    sintomas_patologias = cargar_sintomas_patologias()  

    sintomas_unicos = set()
    for sintomas in sintomas_patologias.values():
        sintomas_unicos.update(sintomas)

    sintomas_lista = list(sintomas_unicos)

    if request.method == 'POST':
        tipo_estudio = request.form.get('tipo_estudio')
        hallazgos_secundarios = 'hallazgos_secundarios' in request.form

        if tipo_estudio == 'familiar':
            patologias_ids = request.form.getlist('patologias')
            if not patologias_ids:
                flash('Por favor, seleccione al menos una patología para el estudio familiar.')
                return render_template('medico/solicitar_estudio.html', paciente=paciente, sintomas_lista=sintomas_lista)
            patologias = Patologia.query.filter(Patologia.id.in_(patologias_ids)).all()
            for patologia in patologias:
                estudio_existente = (
                    Estudio.query
                    .join(HistorialEstado, HistorialEstado.estudio_id == Estudio.id)
                    .filter(
                        Estudio.id_paciente == paciente.id,
                        Estudio.patologias.contains(patologia),
                        HistorialEstado.estado != "FINALIZADO"  
                    )
                    .first()
                )
                if estudio_existente:
                    flash(f'Ya tiene solicitado un estudio para la patología {patologia.nombre} que aún no se ha finalizado.')
                    return render_template('medico/ver_paciente.html', paciente=paciente)

        estudio = Estudio(
            id_paciente=paciente.id,
            id_medico=id_medico,
            tipo_estudio=tipo_estudio,
            hallazgos_secundarios=hallazgos_secundarios
        )

        estudio.id = estudio.generar_id(paciente.apellido)
        if request.form.get('genes_adicionales'):
            estudio.genes_adicionales = request.form.get('genes_adicionales')
            
        if tipo_estudio == 'puntual':
            sintomas = request.form.get('sintomas')
            if not sintomas:
                flash('Por favor, ingrese síntomas para el estudio puntual.')
                return render_template('medico/solicitar_estudio.html', paciente=paciente, sintomas_lista=sintomas_lista)
            sintomas_lista_ingresados = [sintoma.strip().lower() for sintoma in sintomas.split(',')]  
            patologias_detectadas = []

            for patologia, sintomas_patologia in sintomas_patologias.items():
                if any(sintoma in map(str.lower, sintomas_patologia) for sintoma in sintomas_lista_ingresados):
                    patologias_detectadas.append(patologia)

            if not patologias_detectadas:
                flash('Los síntomas ingresados no coinciden con ninguna patología conocida para análisis.')
                return render_template('medico/solicitar_estudio.html', paciente=paciente, sintomas_lista=sintomas_lista)

            for patologia in patologias_detectadas:
                estudio_existente = (
                    Estudio.query
                    .join(HistorialEstado, HistorialEstado.estudio_id == Estudio.id)
                    .filter(
                        Estudio.id_paciente == paciente.id,
                        Estudio.patologias.contains(Patologia.query.filter_by(nombre=patologia).first()),
                        HistorialEstado.estado != "FINALIZADO"  
                    )
                    .first()
                )
                if estudio_existente:
                    flash(f'Ya tiene solicitado un estudio para la patología {patologia} que aún no se ha finalizado.')
                    return render_template('medico/ver_paciente.html', paciente=paciente)

            estudio.sintomas = sintomas
            for patologia in patologias_detectadas:
                estudio.patologias.append(Patologia.query.filter_by(nombre=patologia).first())

            listado_genes = []
            for patologia in patologias_detectadas:
                genes_data = api.obtener_genes_por_patologia(patologia)
                if isinstance(genes_data, dict) and 'gen' in genes_data:
                    listado_genes.append(genes_data['gen'])

            estudio.listado_genes = ", ".join(listado_genes) if listado_genes else None

        elif tipo_estudio == 'familiar':
            listado_genes = []
            for patologia in patologias:
                genes_data = api.obtener_genes_por_patologia(patologia.nombre)
                if isinstance(genes_data, dict) and 'gen' in genes_data:
                    listado_genes.append(genes_data['gen'])

                estudio.patologias.append(patologia)

            estudio.listado_genes = ", ".join(listado_genes) if listado_genes else None

        if tipo_estudio == 'puntual' or (tipo_estudio == 'familiar' and not estudio_existente):
            historial = HistorialEstado(estudio_id=estudio.id, estado="SOLICITADO")
            db.session.add(historial)
            db.session.add(estudio)
            db.session.commit()

            flash('Estudio solicitado exitosamente.')
            return render_template('medico/ver_paciente.html', paciente=paciente)

    return render_template('medico/solicitar_estudio.html', paciente=paciente, sintomas_lista=sintomas_lista)




