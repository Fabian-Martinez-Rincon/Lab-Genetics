from flask import Blueprint, render_template, redirect, url_for, session, flash, make_response
from flask_login import login_user
from src.core.models.laboratorio import Laboratorio
from src.core.models.usuario import Usuario, antecedentes_usuarios
from src.core.models.patologia import Patologia
from src.core.models.database import db
from src.web.formularios.inicio_sesion import LoginForm
from werkzeug.security import check_password_hash
from flask import (
    Blueprint,
    render_template
)

bp = Blueprint("root", __name__)

# @bp.before_request # Este metodo nunca se usa xd
# def check_user():
#     user_id = session.get('user_id')
#     if user_id:
#         user = Usuario.query.get(user_id)
#         if not user:
#             # Si el user_id no coincide con un usuario en la base de datos,
#             # eliminar el user_id de la sesión
#             session.clear()
#             flash('Tu sesión ha sido cerrada.', 'success')
#             response = make_response(redirect(url_for('root.index_get')))
#             response.delete_cookie('session')  # Borrar la cookie de la sesión
#             return response 
        
@bp.get("/")
def index_get():
    if not session.get('logged_in'):
        return redirect(url_for('root.login'))
    if session.get('token') == False:
        flash('Bienvenido a la plataforma, por favor actualice su contraseña.', 'success')
        return redirect(url_for('editar_perfil.editar_perfil', usuario_id=session['user_id']))
    try:
        todas_las_filiales = Laboratorio.query.all()
        return render_template("index.html", filiales=todas_las_filiales)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if not user:
            user = Laboratorio.query.filter_by(email=form.email.data).first()
            user_type = 'laboratorio'
        else:
            user_type = 'usuario'
        
        if user:
            if user.estado != 'ACTIVO' and user_type == 'usuario':
                flash('Tu cuenta está inactiva. Por favor, contacta con soporte.', 'error')
                return redirect(url_for('root.index_get'))
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                session['user_id'] = user.id
                session['user_type'] = user_type
                session['logged_in'] = True
                session['rol_id'] = user.id_rol
                session['token'] = user.token
                if 'jornada_activa' not in session:
                    session['jornada_activa'] = False
                if user.token == False:
                    flash('Bienvenido a la plataforma, por favor actualice su contraseña.', 'success')
                    return redirect(url_for('editar_perfil.editar_perfil', usuario_id=user.id))
                flash('Inicio de sesión Exitoso', 'success')
                return redirect(url_for('root.index_get'))
        else:
            flash('El mail o contraseña son incorrectos.', 'error')
        flash('El mail o contraseña son incorrectos.', 'error')
    return render_template('/comunes/login.html', form=form)



@bp.route('/logout')
def logout():
    if not(session.get('user_id')):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.login'))
    session.pop('user_id', None)
    session['logged_in'] = False
    flash('Se ha cerrado la sesión correctamente.', 'success')
    return redirect(url_for('root.login'))
    
@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@bp.route('/perfil')
def perfil():
    if not session.get('user_id') or not session.get('user_type'):
        flash('Debes iniciar sesión para realizar esta operación.', 'error')
        return redirect(url_for('root.index_get'))
    if session['token'] == False:
        flash('Bienvenido a la plataforma, por favor actualice su contraseña.', 'success')
        return redirect(url_for('editar_perfil.editar_perfil', usuario_id=session['user_id']))
    antecedentes = []
    if session['user_type'] == 'usuario':
        user = Usuario.query.get(session['user_id'])
        antecedentes = db.session.query(
            Patologia.nombre,
            antecedentes_usuarios.c.relacion
        ).join(antecedentes_usuarios, Patologia.id == antecedentes_usuarios.c.patologia_id).filter(
            antecedentes_usuarios.c.usuario_id == user.id
        ).all()
    elif session['user_type'] == 'laboratorio':
        user = Laboratorio.query.get(session['user_id'])
    else:
        flash('Tipo de usuario no reconocido.', 'error')
        return redirect(url_for('root.index_get'))

    if user:
        return render_template('/comunes/perfil.html', user=user, antecedentes=antecedentes)
    else:
        flash('No se pudo encontrar el perfil del usuario.', 'error')
        return redirect(url_for('root.index_get'))
