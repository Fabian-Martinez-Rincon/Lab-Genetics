from flask import Blueprint, render_template, request, redirect, url_for, flash 
from src.core.models.database import db
from src.core.models.presupuesto import Presupuesto
from src.core.models.estudio import Estudio
from src.web.controllers.utils import verificar_autenticacion, verificar_rol
from datetime import datetime, timedelta
from src.core.models.historialEstado import HistorialEstado
bp = Blueprint("generar_presupuesto", __name__)

def generar_detalle_precio(precio_base, precio_adicionales, precio_hallazos, supera_5_genes, hallazgos):
    detalle = f"Detalle de Precio: \n Precio Base {precio_base}usd (Hasta 5 Genes)"
    if supera_5_genes:
        detalle += f" + {precio_adicionales}usd por Gen Adicional\n"
    if hallazgos:
        detalle += f"Se le cobrara {precio_hallazos}usd por la solicitud de hallazgos secundarios\n"
    return detalle

@verificar_autenticacion
@verificar_rol(2)
@bp.route('/generar_presupuesto/<estudio_id>', methods=['GET', 'POST'])
def generar_presupuesto(estudio_id):
    estudio = Estudio.query.get(estudio_id)
    genes_analizar = len(estudio.listado_genes.split(',')) #Perteneces a las patologias solicitadas
    genes_analizar_adicionales = len(estudio.genes_adicionales.split(',')) if estudio.genes_adicionales else 0 # Genes adicionales que cargo el medico
    mas_5_genes = genes_analizar + genes_analizar_adicionales > 5
    if request.method == 'POST':
        fecha_vencimiento = request.form.get('fecha_vencimiento')
        precio_base = int(request.form.get('precio_base'))  # 500 usd
        montoFinal = precio_base
        precio_adicionales = 0
        precio_hallazgos = 0
        if estudio.hallazgos_secundarios:
            precio_hallazgos = int(request.form.get('precio_hallazgos'))  # 200usd
            montoFinal += precio_hallazgos
        if mas_5_genes:
            precio_adicionales = int(request.form.get('precio_adicionales')) # Si supera 5 genes, 30usd por Gen Adicional
            montoFinal += ((genes_analizar + genes_analizar_adicionales - 5) * precio_adicionales)
        detalle_monto = generar_detalle_precio(precio_base, precio_adicionales, precio_hallazgos, mas_5_genes, estudio.hallazgos_secundarios)
        detalle_monto += f"El monto final a abonar es de {montoFinal}usd."
        patologias = ', '.join([patologia.nombre for patologia in estudio.patologias])
        detalle = Presupuesto.generar_detalle(
                patologias=patologias,
                genes=estudio.listado_genes,
                adicionales=estudio.genes_adicionales,
                hallazgos=estudio.hallazgos_secundarios
            ) + detalle_monto
        print(detalle)
        presupuesto = Presupuesto(
            fecha_vencimiento=fecha_vencimiento,
            Detalle= detalle,
            montoFinal=montoFinal,
            id_estado=1
        )
        db.session.add(presupuesto)
        db.session.commit()
        estudio.id_presupuesto = presupuesto.id
        estudio.historial.append(HistorialEstado(estado="PRESUPUESTADO"))
        db.session.commit()
        flash('Presupuesto generado exitosamente.', 'success')
        return redirect(url_for('administrador.presupuestos_solicitados'))
    return render_template('administrador/generar_presupuesto.html', estudio=estudio, mas_5_genes=mas_5_genes, now=datetime.now, timedelta=timedelta)