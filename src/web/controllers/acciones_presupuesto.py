from flask import render_template, Blueprint, redirect, url_for, session, flash
from src.core.models.usuario import Usuario
from src.web.controllers.utils import verificar_rol, verificar_autenticacion, actualizar_presupuestos_vencidos
from src.core.models.presupuesto import Presupuesto
from src.core.models.estudio import Estudio
from src.core.models.estado import Estado

bp = Blueprint('presupuesto', __name__)

@bp.route('/mis_presupuestos', methods=['GET'])
@verificar_autenticacion
@actualizar_presupuestos_vencidos
@verificar_rol(5)
def mis_presupuestos():
    id_usuario = session.get('user_id')
    
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        flash('Usuario no encontrado.', 'error')
        return redirect(url_for('root.index_get'))
    
    # Obtener los estudios del usuario
    estudios = usuario.estudios_como_paciente

    # Obtener presupuestos relacionados con los estudios y su estado
    presupuestos = [
        {
            'presupuesto': Presupuesto.query.get(estudio.id_presupuesto),
            'estado_nombre': Estado.query.get(Presupuesto.query.get(estudio.id_presupuesto).id_estado).nombre,
            'id_estudio': estudio.id
        }
        for estudio in estudios if estudio.id_presupuesto
    ]

    return render_template('paciente/mis_presupuestos.html', presupuestos=presupuestos)



@bp.route('/detalle_presupuesto/<int:presupuesto_id>', methods=['GET'])
@verificar_autenticacion
@actualizar_presupuestos_vencidos
@verificar_rol(5)
def detalle_presupuesto(presupuesto_id):
    presupuesto = Presupuesto.query.get(presupuesto_id)
    if not presupuesto:
        flash('Presupuesto no encontrado.', 'error')
        return redirect(url_for('presupuesto.mis_presupuestos'))
    
    # Obtener el estudio relacionado con el presupuesto
    estudio = None
    if presupuesto.id in [estudio.id_presupuesto for estudio in Estudio.query.all()]:
        estudio = Estudio.query.filter_by(id_presupuesto=presupuesto.id).first()
    
    return render_template(
        'administrador/detalle_presupuesto.html',
        presupuesto=presupuesto,
        estudio=estudio
    )
