from flask import render_template, redirect, url_for, flash, request, Blueprint
from werkzeug.security import generate_password_hash
from src.core.models.database import db
from src.core.models.usuario import Usuario
from src.core.models.notificacion import Notificacion
from src.web.formularios.registrar_medico import RegisterMedicoForm
from src.web.formularios.registrar_administrador import RegisterAdministradorForm
from src.web.formularios.registrar_transportista import RegisterTransportistaForm
from src.web.controllers.utils import verificar_rol, verificar_autenticacion
import random
import string

bp = Blueprint("registrar", __name__)

# Función para generar una contraseña aleatoria
def generar_password_aleatoria(length=10):
    """Genera una contraseña aleatoria segura."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Ruta para registrar un médico
@bp.route('/registrar_medico', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(1)
def registrar_medico():
    form = RegisterMedicoForm()
    if request.method == 'POST' and form.validate_on_submit():
        return manejar_registro_usuario(form, id_rol=4, template_path='/registros/registrar_medico.html')
    return render_template('/registros/registrar_medico.html', form=form)

# Ruta para registrar un administrador
@bp.route('/registrar_administrador', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(1)
def registrar_administrador():
    form = RegisterAdministradorForm()
    if request.method == 'POST' and form.validate_on_submit():
        return manejar_registro_usuario(form, id_rol=2, template_path='/registros/registrar_administrador.html')
    return render_template('/registros/registrar_administrador.html', form=form)

# Ruta para registrar un transportista
@bp.route('/registrar_transportista', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(1)
def registrar_transportista():
    form = RegisterTransportistaForm()
    if request.method == 'POST' and form.validate_on_submit():
        return manejar_registro_usuario(form, id_rol=6, template_path='/registros/registrar_transportista.html')
    return render_template('/registros/registrar_transportista.html', form=form)

# Función común para manejar el registro de usuarios
def manejar_registro_usuario(form, id_rol, template_path):
    # Validar email y DNI
    if Usuario.query.filter_by(email=form.email.data).first():
        flash('Ya existe un usuario registrado con ese email', 'error')
        return render_template(template_path, form=form)

    if Usuario.query.filter_by(dni=form.dni.data).first():
        flash('Ya existe un usuario registrado con ese DNI', 'error')
        return render_template(template_path, form=form)

    # Generar una contraseña automática
    password_aleatoria = generar_password_aleatoria()
    hashed_password = generate_password_hash(password_aleatoria, method='pbkdf2:sha256')

    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        nombre=form.nombre.data,
        apellido=form.apellido.data,
        email=form.email.data,
        password=hashed_password,
        dni=form.dni.data,
        fecha_nacimiento=form.fecha_nacimiento.data,
        telefono=form.telefono.data,
        historia_path='historia_clinica.pdf',
        id_rol=id_rol
    )

    # Guardar usuario y enviar correo
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        descripcion = f"Su contraseña es: {password_aleatoria}"
        Notificacion.send_mail_User(nuevo_usuario.id, descripcion)
        flash('Registro exitoso. La contraseña ha sido enviada por correo electrónico.', 'success')
        return redirect(url_for('root.index_get'))
    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error: {e}', 'error')
        return render_template(template_path, form=form)
