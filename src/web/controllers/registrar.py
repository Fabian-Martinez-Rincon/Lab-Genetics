from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash
from src.core.models.database import db
from src.web.formularios.registrar import RegisterForm
from src.web.formularios.registrar_medico import RegisterMedicoForm
from src.web.formularios.registrar_administrador import RegisterAdministradorForm
from src.web.formularios.registrar_transportista import RegisterTransportistaForm
from src.core.models.usuario import Usuario
from flask import Blueprint

bp = Blueprint("registrar", __name__)

def validar_mail(form, path):
    existing_user = Usuario.query.filter_by(email=form.email.data).first()
    if existing_user:
        flash('Ya existe un usuario registrado con ese mail', 'error')
        form.email.data = ''
        return render_template(path, form=form, password=request.form['password'])

def validar_dni(form, path):
    existing_user_dni = Usuario.query.filter_by(dni=form.dni.data).first()
    if existing_user_dni:
        flash('Ya existe un usuario registrado con ese dni', 'error')
        form.dni.data = ''
        return render_template(path, form=form, password=request.form['password'])

def validar_contrasenia(form, path):
    if len(form.password.data) < 8:
        flash('La contraseña debe tener mínimo 8 caracteres', 'error')
        form.password.data = ''
        return render_template(path, form=form, password=request.form['password'])

def crear_usuario(form, id):
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
        id_rol=id,
    )
    return new_user

def mostrar_errores(form):
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            if (err == "Por favor ingrese un correo electrónico válido."):
                form.email.data = ""                 
                flash(f'{err}', 'error')        
                continue               
            if (err == 'This field is required.'):
                flash(f'El campo {fieldName} es obligatorio', 'error')                
            else:
                form.fecha_nacimiento.data = None
                form.fecha_nacimiento.data = ''       
                flash(f'{err}', 'error')

@bp.route('/registrar_usuario', methods=['GET', 'POST'])
def register():
    path = '/comunes/registrar.html'
    form = RegisterForm()
    if form.validate_on_submit():
        validar_mail(form, path)
        validar_dni(form, path)
        validar_contrasenia(form, path)
        new_user = crear_usuario(form)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Fue registrado correctamente', 'success')
            return redirect(url_for('root.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'ups ocurrio un error: {e}', 'error')
    else:
        password = request.form.get('password', '')
        mostrar_errores(form)
        return render_template('/comunes/registrar.html', form=form, password=password)
    return render_template('/comunes/registrar.html', form=form, password='')

@bp.route('/registrar_medico', methods=['GET', 'POST'])
def register_medico():
    path = '/registros/registrar_medico.html'
    form = RegisterMedicoForm()
    if form.validate_on_submit():
        validar_mail(form, path)
        validar_dni(form, path)
        validar_contrasenia(form, path)
        new_medico = crear_usuario(form, 4) # 4 es el id del rol médico
        try:
            db.session.add(new_medico)
            db.session.commit()
            flash('El médico ha sido registrado correctamente', 'success')
            return redirect(url_for('root.index_get'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error: {e}', 'error')
    else:
        password = request.form.get('password', '')
        mostrar_errores(form)
        return render_template('/registros/registrar_medico.html', form=form, password=password)
    return render_template('/registros/registrar_medico.html', form=form, password='')

@bp.route('/registrar_administrador', methods=['GET', 'POST'])
def register_administrador():
    path = '/registros/registrar_administrador.html'
    form = RegisterAdministradorForm()
    if form.validate_on_submit():
        validar_mail(form, path)
        validar_dni(form, path)
        validar_contrasenia(form, path)
        new_medico = crear_usuario(form, 2) # 2 es el id del rol administrador
        try:
            db.session.add(new_medico)
            db.session.commit()
            flash('El administrador ha sido registrado correctamente', 'success')
            return redirect(url_for('root.index_get'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error: {e}', 'error')
    else:
        password = request.form.get('password', '')
        mostrar_errores(form)
        return render_template('/registros/registrar_administrador.html', form=form, password=password)
    return render_template('/registros/registrar_administrador.html', form=form, password='')

@bp.route('/registrar_transportista', methods=['GET', 'POST'])
def register_transportista():
    path = '/registros/registrar_transportista.html'
    form = RegisterTransportistaForm()
    if form.validate_on_submit():
        validar_mail(form, path)
        validar_dni(form, path)
        validar_contrasenia(form, path)
        new_medico = crear_usuario(form, 6) # 2 es el id del rol transportista
        try:
            db.session.add(new_medico)
            db.session.commit()
            flash('El administrador ha sido registrado correctamente', 'success')
            return redirect(url_for('root.index_get'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error: {e}', 'error')
    else:
        password = request.form.get('password', '')
        mostrar_errores(form)
        return render_template('/registros/registrar_transportista.html', form=form, password=password)
    return render_template('/registros/registrar_transportista.html', form=form, password='')