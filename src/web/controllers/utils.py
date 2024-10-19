from flask import session, flash, redirect, url_for
from functools import wraps 
from src.core.models.usuario import Usuario

def verificar_rol(rol_permitido):
    """
    Decorador que restringe el acceso a una ruta según el rol del usuario autenticado.

    Parámetros:
    rol_permitido (int): El rol permitido para acceder a la ruta.

    Lista de roles disponibles:
    - 1: Owner
    - 2: Administrador
    - 3: Laboratorio
    - 4: Medico
    - 5: Paciente
    - 6: Transportista

    Si el usuario no está autenticado o su rol no coincide con el rol permitido,
    se redirige al usuario a la página principal y se muestra un mensaje de error.

    Uso:
    @verificar_rol(2)
    def listar_turnos():
        # Código de la vista
        pass

    En este ejemplo, solo los usuarios con el rol de "Administrador" (rol 2)
    pueden acceder a la ruta decorada.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verifica si el usuario ha iniciado sesión
            user_id = session.get('user_id')
            if not user_id:
                flash('Debes iniciar sesión para realizar esta operación.', 'error')
                return redirect(url_for('root.index_get'))

            # Obtén el rol del usuario actual
            usuario = Usuario.query.get(user_id)
            if not usuario or usuario.id_rol != rol_permitido:
                flash('No tienes permiso para realizar esta operación.', 'error')
                return redirect(url_for('root.index_get'))

            # Si el rol es correcto, continúa con la función decorada
            return f(*args, **kwargs)
        return decorated_function
    return decorator
