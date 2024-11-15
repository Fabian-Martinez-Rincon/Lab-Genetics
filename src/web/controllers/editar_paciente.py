from flask import render_template, redirect, url_for, flash, Blueprint, session, abort, request
from src.core.models.database import db
from src.core.models.patologia import Patologia
from src.core.models.usuario import Usuario, antecedentes_usuarios
from src.web.controllers.utils import verificar_rol, verificar_autenticacion

bp = Blueprint('editar_paciente', __name__)

@bp.route('/editar_paciente/<int:paciente_id>', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(4)
def editar_paciente(paciente_id):
    paciente = Usuario.query.get_or_404(paciente_id)
    id_medico = session.get('user_id')
    if paciente.id_medico != id_medico:
        abort(404, description="Paciente no encontrado o no autorizado para ver este perfil")

    if request.method == 'POST':
        nueva_patologia_id = request.form.get('patologia')
        relacion = request.form.get('relacion')
        if nueva_patologia_id and relacion:
            nueva_patologia = Patologia.query.get(nueva_patologia_id)
            if nueva_patologia and nueva_patologia not in paciente.patologias:
                paciente.patologias.append(nueva_patologia)
                db.session.commit()
                db.session.execute(
                    antecedentes_usuarios.update()
                    .where(
                        antecedentes_usuarios.c.usuario_id == paciente.id,
                        antecedentes_usuarios.c.patologia_id == nueva_patologia.id
                    )
                    .values(relacion=relacion)
                )
                db.session.commit()
                
                flash('Antecedente Familiar agregado exitosamente.', 'success')
                return redirect(url_for('ver_paciente.ver_paciente', paciente_id=paciente_id))

    todas_las_patologias = Patologia.query.all()
    patologias_existentes = {patologia.id for patologia in paciente.patologias}
    patologias_disponibles = [patologia for patologia in todas_las_patologias if patologia.id not in patologias_existentes]

    antecedentes = db.session.query(Patologia, antecedentes_usuarios.c.relacion).join(
        antecedentes_usuarios, Patologia.id == antecedentes_usuarios.c.patologia_id
    ).filter(antecedentes_usuarios.c.usuario_id == paciente_id).all()

    return render_template(
        'medico/editar_paciente.html', 
        paciente=paciente, 
        todas_las_patologias=patologias_disponibles, 
        antecedentes=antecedentes
    )
