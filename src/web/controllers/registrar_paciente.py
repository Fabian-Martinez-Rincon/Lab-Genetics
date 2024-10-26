from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app, session
from src.web.formularios.registrar_paciente import RegisterPacienteForm
from src.web.controllers.utils import verificar_rol, verificar_autenticacion
from src.core.models.usuario import Usuario
from src.core.models.patologia import Patologia
from werkzeug.security import generate_password_hash
from src.core.models.database import db
from werkzeug.utils import secure_filename
import os

bp = Blueprint('registrar_paciente', __name__)

@bp.route('/registrar_paciente', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(4)
def registrar_paciente():
    form = RegisterPacienteForm()
    patologias = Patologia.query.all()  # Obtener todas las patologías de la base de datos
    form.patologias.choices = [(p.id, p.nombre) for p in patologias]  # Configurar las opciones del formulario

    if request.method == 'POST':
        if form.validate_on_submit():
            # Validación de formulario
            if Usuario.query.filter_by(email=form.email.data).first():
                flash('Ya existe un usuario registrado con ese email', 'error')
                form.email.data = ''
                return render_template('medico/registrar_paciente.html', form=form, patologias=patologias)

            if Usuario.query.filter_by(dni=form.dni.data).first():
                flash('Ya existe un usuario registrado con ese dni', 'error')
                return render_template('medico/reasignar.html')

            if len(form.password.data) < 8:
                flash('La contraseña debe tener mínimo 8 caracteres', 'error')
                form.password.data = ''
                return render_template('medico/registrar_paciente.html', form=form, patologias=patologias)

            historia = form.historia.data
            ruta_historia = None  
            if historia:
                dni = form.dni.data  
                nombre_archivo = f"{secure_filename(dni)}.pdf"  
                if nombre_archivo.lower().endswith('.pdf'):
                    ruta_carpeta = os.path.join(current_app.config['UPLOAD_FOLDER'], 'historia')
                    os.makedirs(ruta_carpeta, exist_ok=True)
                    ruta_historia = os.path.join(ruta_carpeta, nombre_archivo)
                    if os.path.exists(ruta_historia):
                        flash('Ya existe un archivo con este DNI.', 'error')
                        return render_template('medico/registrar_paciente.html', form=form, patologias=patologias)
                    historia.save(ruta_historia)
                else:
                    flash('El archivo debe estar en formato PDF.', 'error')
                    return render_template('medico/registrar_paciente.html', form=form, patologias=patologias)
            
            id_medico = session.get('user_id')
            # Creación del nuevo usuario
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
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

            # Agregar las patologías seleccionadas
            patologias_seleccionadas = request.form.getlist('patologias')
          # Obtén las IDs de las patologías seleccionadas
            for patologia_id in patologias_seleccionadas:
                patologia = Patologia.query.get(patologia_id)
                new_user.patologias.append(patologia)  # Agregar patología al nuevo usuario

            # Guardado del usuario
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registro exitoso', 'success')
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
