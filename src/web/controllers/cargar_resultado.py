from flask import render_template, request, redirect, url_for, flash, Blueprint
from src.core.models.database import db
from src.core.models.estudio import Estudio
from src.core.models.historialEstado import HistorialEstado
from src.core.models.resultado import Resultado
from src.web.controllers.utils import verificar_autenticacion, verificar_rol, enviar_estudios_automaticamente
from .api import SnippetsAPI
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from src.core.models.exterior import Exterior
from src.core.models.notificacion import Notificacion
bp = Blueprint("cargar_resultado", __name__) 

@enviar_estudios_automaticamente
@verificar_autenticacion
@verificar_rol(2)
@bp.route('/cargar_resultado', methods=['GET', 'POST'])
def cargar_resultado():
    api = SnippetsAPI() 
    ultimo_estado_subquery = (
        db.session.query(
            HistorialEstado.estudio_id,
            func.max(HistorialEstado.fecha_hora).label("ultima_fecha")
        )
        .group_by(HistorialEstado.estudio_id)
        .subquery()
    )
    ultimo_estado = aliased(HistorialEstado)
    estudios_enviados_1 = (
        db.session.query(Estudio.id)
        .join(ultimo_estado, Estudio.id == ultimo_estado.estudio_id)
        .join(
            ultimo_estado_subquery,
            (ultimo_estado.estudio_id == ultimo_estado_subquery.c.estudio_id) & 
            (ultimo_estado.fecha_hora == ultimo_estado_subquery.c.ultima_fecha)
        )
        .filter(ultimo_estado.estado == "ENVIADO AL EXTERIOR")
        .order_by(Estudio.fecha_ingreso_central.asc())
        .all()
    )

    estudios_enviados = [estudio.id for estudio in estudios_enviados_1]
        
    if request.method == 'POST':
        id_estudio = request.form['id_estudio']
        variantes = request.form['variantes']
        resultados_genes = request.form.get('resultados_genes', '')  
        hallazgos_secundarios = request.form.get('hallazgos_secundarios', '') 

        estudio = Estudio.query.filter_by(id=id_estudio).first()
        if not estudio:
            flash('ID de estudio no válido.', 'error')
            return redirect(url_for('cargar_resultado.cargar_resultado'))
        if id_estudio not in estudios_enviados:
            flash('Este estudio no ha sido enviado al exterior.', 'error')
            return redirect(url_for('cargar_resultado.cargar_resultado'))
        if not variantes:
            flash('Debe Ingresar las Variantes.', 'error')
            return redirect(url_for('cargar_resultado.cargar_resultado'))
        if estudio.genes_adicionales and not resultados_genes:
            flash('El estudio solicitó genes adicionales, pero no se cargaron resultados.', 'error')
            return redirect(url_for('cargar_resultado.cargar_resultado'))

        if estudio.hallazgos_secundarios and not hallazgos_secundarios:
            flash('El estudio solicitó hallazgos secundarios, pero no se cargaron resultados.', 'error')
            return redirect(url_for('cargar_resultado.cargar_resultado'))

        variantes_lista = variantes.split(",") if variantes else []
        diagnostico_confirmado = None
        observaciones = []
        tipo_resultado = "Baja Calidad" 
        for patologia in estudio.patologias:
            diagnostico = api.confirmar_diagnostico(patologia.nombre, variantes_lista)
            if diagnostico is None:
                flash(f'No se pudo confirmar el diagnóstico para la patología {patologia.nombre} con la API.', 'error')
                return redirect(url_for('cargar_resultado.cargar_resultado'))
            observaciones.append(f"Diagnóstico para {patologia.nombre}: {'Confirmado' if diagnostico else 'No confirmado'}")
            if diagnostico:
                tipo_resultado = "Positivo"
        
        observacion_api = " | ".join(observaciones)
        resultado = Resultado(
            resultadoBase=f"{tipo_resultado} - Variantes obtenidas: {variantes}",
            resultadoGenesAdicionales=resultados_genes,  
            resultadoHallazgosSecundarios=hallazgos_secundarios,  
            observacion=observacion_api
        )

        db.session.add(resultado)
        db.session.commit()
        estudio.id_resultado = resultado.id
        estudio.historial.append(HistorialEstado(estado="RESULTADO CARGADO"))
        detalle_resultado = f"""
        Estudio ID: {estudio.id}
        Tipo de Resultado: {tipo_resultado}
        Variantes obtenidas: {variantes}
        Diagnósticos confirmados: {observacion_api}
        """
        
        if resultados_genes:
            detalle_resultado += f"\nResultados de Genes adicionales: {resultados_genes}"

        if hallazgos_secundarios:
            detalle_resultado += f"\nHallazgos secundarios: {hallazgos_secundarios}"
        Notificacion.send_mail(estudio.id_paciente, f"El Resultado de su estudio {estudio.id} ha sido cargado.\n\nDetalles del resultado:\n{detalle_resultado}")
        exterior = Exterior.query.filter_by(id=estudio.id_exterior).first()
        todos_listos =0 
        for estudio in exterior.estudios:
            estado = HistorialEstado.query.filter_by(estudio_id=estudio.id).order_by(HistorialEstado.fecha_hora.desc()).first()
            if estado.estado == "RESULTADO CARGADO":
                todos_listos += 1
        if todos_listos == len(exterior.estudios):
            exterior.estado = "RESULTADOS RECIBIDOS"
        db.session.commit()

        flash('Resultado cargado exitosamente.', 'success')
        return redirect(url_for('cargar_resultado.cargar_resultado'))
    
    return render_template('administrador/cargar_resultado.html', estudios_enviados=estudios_enviados)
