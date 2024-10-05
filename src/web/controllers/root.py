from flask import Blueprint, render_template, redirect, url_for, session, flash, make_response
from flask_login import login_user
from src.core.models.filial import Filial
from src.core.models.usuario import Usuario
from src.web.formularios.inicio_sesion import LoginForm
from werkzeug.security import check_password_hash
from flask import (
    Blueprint,
    render_template
)

bp = Blueprint("root", __name__)

@bp.before_request
def check_user():
    user_id = session.get('user_id')
    if user_id:
        user = Usuario.query.get(user_id)
        if not user:
            # Si el user_id no coincide con un usuario en la base de datos,
            # eliminar el user_id de la sesión
            session.clear()
            flash('Tu sesión ha sido cerrada.', 'info')
            response = make_response(redirect(url_for('root.index_get')))
            response.delete_cookie('session')  # Borrar la cookie de la sesión
            return response 
        
@bp.get("/")
def index_get(): 
    try:
        todas_las_filiales = Filial.query.all()
        return render_template("index.html", filiales=todas_las_filiales)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if user.penaltis < 3:  # Verifica si el usuario no ha sido eliminado (penalizado 3 veces)
                login_user(user)
                session['user_id'] = user.id
                session['logged_in'] = True
                #session['rol_id'] = user.id_rol
                flash('Inicio de sesión Exitoso', 'success')
                return redirect(url_for('root.index_get'))
            else:
                flash('Este usuario ha sido eliminado.', 'error')
        else:
            flash('El mail o contraseña son incorrectos.', 'error')
    return render_template('/comunes/login.html', form=form)


@bp.route('/logout')
def logout():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    session.pop('user_id', None)
    session['logged_in'] = False
    flash('Se ha cerrado la sesión correctamente.', 'success')
    return redirect(url_for('root.index_get'))
    
@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
