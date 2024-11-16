from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.core.models.usuario import Usuario, antecedentes_usuarios
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

def verificar_estudio_existente(paciente, patologia):
    estudio_existente = (
        Estudio.query
        .join(HistorialEstado, HistorialEstado.estudio_id == Estudio.id)
        .filter(
            Estudio.id_paciente == paciente.id,
            Estudio.patologias.any(id=patologia),
            HistorialEstado.estado != "FINALIZADO"  
        )
        .first()
    )
    return estudio_existente

def verificar_sospecha_familiar(form, paciente):
    patologias_ids = request.form.getlist('patologias')
    if not patologias_ids:
        flash('Por favor, seleccione al menos una patología para el estudio familiar.', 'error')
        return False
    patologias = Patologia.query.filter(Patologia.id.in_(patologias_ids)).all()
    for patologia in patologias:
        if (verificar_estudio_existente(paciente, patologia.id)):
            flash(f'Ya tiene solicitado un estudio para las patologías seleccionadas que aún no se ha finalizado.', 'error')
            return False
    return True

def verificar_sospecha_puntual(form, paciente, api):
    sintomas = request.form.get('sintomas')
    patologia_id = request.form.get('patologia')
    if not sintomas or not patologia_id:
        flash('Por favor, ingrese síntomas y la patologia a evaluar para el estudio puntual.', 'error')
        return False
    sintomas_lista_ingresados = [sintoma.strip().lower() for sintoma in sintomas.split(',')]  
    patologia = Patologia.query.filter_by(id=patologia_id).first()
    if (api.confirmar_diagnostico(patologia.nombre, sintomas_lista_ingresados) == False):
        flash(f'Los sintomas ingresados no son cardinales a la patologia seleccionada.', 'error')
        return False
    if (verificar_estudio_existente(paciente, patologia.id)):
        flash(f'Ya tiene solicitado un estudio para la patología seleccionada que aún no se ha finalizado.', 'error')
        return False
    return True

def obtener_genes(patologias, api):
    listado_genes = []
    for patologia in patologias:
        patologia = Patologia.query.filter_by(id=patologia).first()
        genes_data = api.obtener_genes_por_patologia(patologia.nombre)
        if isinstance(genes_data, dict) and 'gen' in genes_data:
            listado_genes.append(genes_data['gen'])
    return ", ".join(listado_genes) if listado_genes else None
    
def generar_estudio(paciente_id, tipo_estudio, hallazgos_secundarios, patologias, adicionales, id_medico, api):  
    paciente = Usuario.query.filter_by(id=paciente_id).first()
    estudio = Estudio(
        id = Estudio.generar_id(paciente.apellido, paciente.nombre, paciente.id),
        id_paciente=paciente.id,
        id_medico=id_medico,
        tipo_estudio=tipo_estudio,
        hallazgos_secundarios=hallazgos_secundarios,
        genes_adicionales = adicionales,
        listado_genes = obtener_genes(patologias, api),
    )
    for patologia_id in patologias:
        patologia = Patologia.query.filter_by(id=patologia_id).first()
        if patologia:
            estudio.patologias.append(patologia)
    if tipo_estudio == 'puntual':
        sintomas = request.form.get('sintomas')
        estudio.sintomas = sintomas
    
    historial = HistorialEstado(estudio_id=estudio.id, estado="SOLICITADO")
    db.session.add(historial)
    db.session.add(estudio)
    db.session.commit()
    flash('Estudio solicitado exitosamente.', 'success')
    return True

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
    sintomas_lista = api.obtener_lista_sintomas()
    adicionales_lista = api.obtener_lista_genes()
    patologias = Patologia.query.all()
    antecedentes = db.session.query(Patologia, antecedentes_usuarios.c.relacion).join(
        antecedentes_usuarios, Patologia.id == antecedentes_usuarios.c.patologia_id
    ).filter(antecedentes_usuarios.c.usuario_id == paciente_id).all()
    
    if not sintomas_lista or not adicionales_lista:
        flash('Error al obtener la lista de síntomas o lista de genes adicionales.', 'error')
    if request.method == 'POST':
        tipo_estudio = request.form.get('tipo_estudio')
        hallazgos_secundarios = 'hallazgos_secundarios' in request.form
        adicionales = request.form.get('genes_adicionales')
        if tipo_estudio == 'familiar':
            if verificar_sospecha_familiar(request.form, paciente):
                patologias = request.form.getlist('patologias')
                if (generar_estudio(paciente.id, tipo_estudio, hallazgos_secundarios, patologias, adicionales, id_medico, api)):
                    return redirect(url_for('ver_paciente.ver_paciente', paciente_id=paciente_id))
            return render_template('medico/solicitar_estudio.html', paciente=paciente, sintomas_lista=sintomas_lista, adicionales_lista=adicionales_lista, patologias=patologias, antecedentes=antecedentes)
        else:
            if verificar_sospecha_puntual(request.form, paciente, api):
                patologias = request.form.get('patologia')
                if (generar_estudio(paciente.id, tipo_estudio, hallazgos_secundarios, patologias, adicionales, id_medico, api)):
                    return redirect(url_for('ver_paciente.ver_paciente', paciente_id=paciente_id))
            return render_template('medico/solicitar_estudio.html', paciente=paciente, sintomas_lista=sintomas_lista, adicionales_lista=adicionales_lista, patologias=patologias, antecedentes=antecedentes)
    return render_template('medico/solicitar_estudio.html', paciente=paciente, sintomas_lista=sintomas_lista, adicionales_lista=adicionales_lista, patologias=patologias, antecedentes=antecedentes)




