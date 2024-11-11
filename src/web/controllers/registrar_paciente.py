from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app, session
from src.web.formularios.registrar_paciente import RegisterPacienteForm
from src.web.controllers.utils import verificar_rol, verificar_autenticacion
from src.core.models.usuario import Usuario, antecedentes_usuarios
from src.core.models.patologia import Patologia
from werkzeug.security import generate_password_hash
from src.core.models.database import db
from werkzeug.utils import secure_filename
import os
from src.core.models.notificacion import Notificacion
bp = Blueprint('registrar_paciente', __name__)

@bp.route('/registrar_paciente', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(4)
def registrar_paciente():
    form = RegisterPacienteForm()
    patologias = Patologia.query.all()  
    form.patologias.choices = [(p.id, p.nombre) for p in patologias]  
    if request.method == 'POST':
        if form.validate_on_submit():
            if Usuario.query.filter_by(email=form.email.data).first():
                flash('Ya existe un usuario registrado con ese email', 'error')
                form.email.data = ''
                return render_template('medico/registrar_paciente.html', form=form, patologias=patologias)

            if Usuario.query.filter_by(dni=form.dni.data).first():
                flash('Ya existe un usuario registrado con ese dni', 'error')
                return render_template('medico/reasignar.html')
            patologias_seleccionadas = request.form.getlist('patologias')
            if not validar_parentesco(form, patologias_seleccionadas):
                return render_template('medico/registrar_paciente.html', form=form, patologias=patologias)

            historia = form.historia.data
            ruta_historia = cargar_historia_clinica(historia, form)
            if not ruta_historia:
                return render_template('medico/registrar_paciente.html', form=form, patologias=patologias)
            
            id_medico = session.get('user_id')
            hashed_password = generate_password_hash(form.dni.data, method='pbkdf2:sha256')
            new_user = Usuario(
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                email=form.email.data,
                password=hashed_password,
                dni=form.dni.data,
                fecha_nacimiento=form.fecha_nacimiento.data,
                telefono=form.telefono.data,
                historia_path=ruta_historia,
                id_rol=5,
                id_medico = id_medico
            )
            
            try:
                db.session.add(new_user)
                asignar_parentesco(new_user, patologias_seleccionadas, request.form)
                db.session.commit()
                flash('Registro exitoso', 'success')
                descripcion = f" Ha sido Registrado con exito en la plataforma. \n Recuerde que Su constraseña es: \n {form.dni.data}"
                Notificacion.send_mail(new_user.id, descripcion)
                return redirect(url_for('root.index_get'))
            except Exception as e:
                db.session.rollback()
                flash(f'Ocurrió un error al guardar en la base de datos: {e}', 'error')
                return render_template('medico/registrar_paciente.html', form=form, patologias=patologias)

        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    if err == "Por favor ingrese un correo electrónico válido.":
                        form.email.data = ''
                        flash(f'{err}', 'error')
                    elif err == 'This field is required.':
                        flash(f'El campo {fieldName} es obligatorio', 'error')
                    else:
                        form.fecha_nacimiento.data = None
                        flash(f'{err}', 'error')
            return render_template('medico/registrar_paciente.html', form=form, patologias=patologias)

    return render_template('medico/registrar_paciente.html', form=form, patologias=patologias)

def validar_parentesco(form, patologias_seleccionadas):
    for patologia_id in patologias_seleccionadas:
        relacion_field = f'relacion_{patologia_id}'
        parentesco = request.form.get(relacion_field, '') 
        if not parentesco:
            flash(f"Debe ingresar el parentesco para la patología seleccionada", 'error')
            return False
    return True

def asignar_parentesco(new_user, patologias_seleccionadas, form):
    for patologia_id in patologias_seleccionadas:
        patologia = Patologia.query.get(patologia_id)
        relacion_field = f'relacion_{patologia_id}'
        parentesco = form.get(relacion_field, '') 

        # Agregar el antecedente con el campo `relacion`
        antecedente = antecedentes_usuarios.insert().values(
            usuario_id=new_user.id,
            patologia_id=patologia.id,
            relacion=parentesco
        )
        db.session.execute(antecedente)


def cargar_historia_clinica(historia, form):
    ruta_historia = None  
    if historia:
        dni = form.dni.data  
        nombre_archivo = f"{secure_filename(dni)}.pdf"  
        if nombre_archivo.lower().endswith('.pdf'):
            ruta_carpeta = 'historia'  
            carpeta_absoluta = os.path.join(current_app.config['UPLOAD_FOLDER'], ruta_carpeta)
            os.makedirs(carpeta_absoluta, exist_ok=True)
            ruta_historia_absoluta = os.path.join(carpeta_absoluta, nombre_archivo)
            if os.path.exists(ruta_historia_absoluta):
                flash('Ya existe un archivo con este DNI.', 'error')
            historia.save(ruta_historia_absoluta)
            ruta_historia = os.path.join(ruta_carpeta, nombre_archivo).replace("\\", "/")  # Guardar solo "historia/12345678.pdf"
        else:
            flash('El archivo debe estar en formato PDF.', 'error')               
    return ruta_historia
