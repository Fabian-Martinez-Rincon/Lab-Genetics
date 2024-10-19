from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash
from functools import wraps
from src.core.models.database import db
from src.web.formularios.registrar_medico import RegisterMedicoForm
from src.web.formularios.registrar_administrador import RegisterAdministradorForm
from src.web.formularios.registrar_transportista import RegisterTransportistaForm
from src.core.models.usuario import Usuario
from flask import Blueprint
from src.web.controllers.utils import verificar_rol, verificar_autenticacion

bp = Blueprint("registrar", __name__)

# Decorador para manejar el proceso de registro
def manejar_registro(form_class, template_path, id_rol):
    def decorador(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            form = form_class()
            if form.validate_on_submit():
                validar_formulario(form, template_path)
                new_user = crear_usuario(form, id_rol)
                return guardar_usuario(new_user)
            else:
                password = request.form.get('password', '')
                mostrar_errores(form)
                return render_template(template_path, form=form, password=password)
        return wrapped
    return decorador

# Funciones de validación y creación
def validar_formulario(form, path):
    """Valida los campos del formulario: email, dni, y contraseña."""
    if Usuario.query.filter_by(email=form.email.data).first():
        flash('Ya existe un usuario registrado con ese email', 'error')
        form.email.data = ''
        return render_template(path, form=form, password=request.form['password'])

    if Usuario.query.filter_by(dni=form.dni.data).first():
        flash('Ya existe un usuario registrado con ese dni', 'error')
        form.dni.data = ''
        return render_template(path, form=form, password=request.form['password'])

    if len(form.password.data) < 8:
        flash('La contraseña debe tener mínimo 8 caracteres', 'error')
        form.password.data = ''
        return render_template(path, form=form, password=request.form['password'])

def crear_usuario(form, id_rol):
    """Crea un nuevo usuario a partir del formulario."""
    hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
    new_user = Usuario(
        nombre=form.nombre.data,
        apellido=form.apellido.data,
        email=form.email.data,
        password=hashed_password,
        dni=form.dni.data,
        fecha_nacimiento=form.fecha_nacimiento.data,
        telefono=form.telefono.data,
        historia_path='historia_clinica.pdf',
        id_rol=id_rol,
    )
    return new_user

def guardar_usuario(new_user):
    """Guarda un usuario en la base de datos con manejo de errores."""
    try:
        db.session.add(new_user)
        db.session.commit()
        flash('Registro exitoso', 'success')
        return redirect(url_for('root.index_get'))
    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error: {e}', 'error')
        return None

def mostrar_errores(form):
    """Muestra los errores de validación del formulario."""
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


@bp.route('/registrar_medico', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(1)
@manejar_registro(RegisterMedicoForm, '/registros/registrar_medico.html', 4)
def register_medico():
    pass

@bp.route('/registrar_administrador', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(1)
@manejar_registro(RegisterAdministradorForm, '/registros/registrar_administrador.html', 2)
def register_administrador():
    pass

@bp.route('/registrar_transportista', methods=['GET', 'POST'])
@verificar_autenticacion
@verificar_rol(1)
@manejar_registro(RegisterTransportistaForm, '/registros/registrar_transportista.html', 6)
def register_transportista():
    pass
