from src.core.models.database import db
from src.core.models.usuario import Usuario
from src.web.formularios.editar_perfil import EditarPerfilForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, Blueprint, flash, redirect, url_for, render_template
from src.core.models.notificacion import Notificacion
from src.core.models.laboratorio import Laboratorio

bp = Blueprint("editar_perfil", __name__)

@bp.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    form = EditarPerfilForm()  # Asegúrate de crear este formulario en tu aplicación
    usuario_actual = Usuario.query.get(session.get('user_id'))
    if usuario_actual is None:
        usuario_actual = Laboratorio.query.get(session.get('user_id'))
        if usuario_actual is None:
            flash('No se encontró al usuario. Por favor, vuelve a iniciar sesión.', 'error')
            # Puedes redirigir al usuario a una página de inicio de sesión o a cualquier otra página de tu elección
            return redirect(url_for('root.login'))

    if form.validate_on_submit():
        if len(form.nueva_password.data) < 8:
            flash('La contraseña debe tener mínimo 8 caracteres', 'error')
            return render_template('/comunes/editar_perfil.html', form=form, user=usuario_actual)
        if check_password_hash(usuario_actual.password, form.password_actual.data):
            # La contraseña actual es correcta, procede a actualizar la contraseña
            hashed_password = generate_password_hash(form.nueva_password.data, method='pbkdf2:sha256')
            usuario_actual.password = hashed_password
            if usuario_actual.token == False:
                usuario_actual.token = True
                session.setdefault('token', True)
                session['token'] = True
            db.session.commit()
            Notificacion.send_mail(usuario_actual.id, "Se ha actualizado su contraseña.")
            flash('¡Perfil actualizado correctamente!', 'success')
            return redirect(url_for('root.perfil', usuario_id=usuario_actual.id))
        else:
            flash('Contraseña actual incorrecta. Inténtalo de nuevo.', 'error')
        
    return render_template('/comunes/editar_perfil.html', form=form, user=usuario_actual)
