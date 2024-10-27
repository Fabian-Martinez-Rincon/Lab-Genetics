from flask import session, flash, redirect, url_for
from functools import wraps
from src.core.models.usuario import Usuario
from src.core.models.laboratorio import Laboratorio

def verificar_autenticacion(f):
    """
    Decorador que verifica si el usuario ha iniciado sesión.
    Si no está autenticado, redirige al usuario a la página principal.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash('Debes iniciar sesión para realizar esta operación.', 'error')
            return redirect(url_for('root.index_get'))
        return f(*args, **kwargs)
    return decorated_function

def verificar_rol(rol_permitido):
    """
    Decorador que verifica si el usuario autenticado tiene el rol adecuado.
    
    Parámetros:
    rol_permitido (int): El rol permitido para acceder a la ruta.

    Lista de roles disponibles:
    - 1: Owner
    - 2: Administrador
    - 3: Laboratorio
    - 4: Medico
    - 5: Paciente
    - 6: Transportista

    Si el rol del usuario no coincide con el rol permitido, redirige
    al usuario a la página principal y muestra un mensaje de error.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            user_type = session.get('user_type')
            if user_type == 'usuario':
                usuario = Usuario.query.get(user_id)
            elif user_type == 'laboratorio':
                usuario = Laboratorio.query.get(user_id)
            if  usuario.id_rol != rol_permitido:
                flash('No tienes permiso para realizar esta operación.', 'error')
                return redirect(url_for('root.index_get'))

            # Si el rol es correcto, continúa con la función decorada
            return f(*args, **kwargs)
        return decorated_function
    return decorator
