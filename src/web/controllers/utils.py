from flask import session, flash, redirect, url_for
from functools import wraps
from src.core.models.usuario import Usuario
from src.core.models.laboratorio import Laboratorio
from datetime import datetime
from src.core.models.presupuesto import Presupuesto
from src.core.models.estudio import Estudio
from src.core.models.historialEstado import HistorialEstado
from src.core.models.database import db
from src.core.models.notificacion import Notificacion
from src.core.models.turno import Turno
from src.core.models.exterior import Exterior
from .api import SnippetsAPI 
import csv
import tempfile
import requests
import os

def verificar_autenticacion(f):
    """
    Decorador que verifica si el usuario ha iniciado sesión.
    Si no está autenticado, redirige al usuario a la página principal.
    Si esta autenticado y su cuenta está inactiva, redirige al usuario a la página principal.(Excepto si es un laboratorio)
    Si esta autenticado, verifica si el usuario debe actualizar su contraseña.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash('Debes iniciar sesión para realizar esta operación.', 'error')
            return redirect(url_for('root.index_get'))
        
        usuario = Usuario.query.get(user_id)
        if usuario:
            if usuario.estado == 'INACTIVO':
                flash('Tu cuenta está inactiva. Por favor, contacta con soporte.', 'error')
                return redirect(url_for('root.index_get'))
        else:
            usuario = Laboratorio.query.get(user_id)
        if usuario.token == False:
            flash('Bienvenido a la plataforma, por favor actualice su contraseña.', 'success')
            return redirect(url_for('editar_perfil.editar_perfil', usuario_id=usuario.id))
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

def actualizar_presupuestos_vencidos(f):
    """
    Decorador para verificar presupuestos vencidos y actualizar su estado.
    """
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        fecha_actual = datetime.now().date()
        presupuestos_vencidos = Presupuesto.query.filter(
            Presupuesto.fecha_vencimiento < fecha_actual,
            Presupuesto.id_estado != 2, Presupuesto.id_estado != 3, Presupuesto.id_estado != 5  
        ).all()

        for presupuesto in presupuestos_vencidos:
            presupuesto.id_estado = 5  # Presupuesto vencido / cancelado  
            estudio = Estudio.query.filter_by(id_presupuesto=presupuesto.id).first()
            estudio.historial.append(HistorialEstado(estado="PRESUPUESTO VENCIDO"))
            Notificacion.send_mail(estudio.id_paciente, f"El presupuesto {presupuesto.id} para el estudio {estudio.id} ha vencido.")
        db.session.commit()
        return f(*args, **kwargs)
    return wrapped_function

def actualizar_turnos_vencidos(f):
    """
    Decorador para verificar turnos vencidos y actualizar su estado.
    """
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        fecha_actual = datetime.now().date()
        turnos_vencidos = Turno.query.filter(
            Turno.fecha < fecha_actual,
            Turno.estado != 5 , Turno.estado_interno != "LIBRE"
        ).all()

        for turno in turnos_vencidos:
            turno.estado = 5  # Presupuesto vencido / cancelado  
            turno.estado_interno = "LIBRE"
            estudio = Estudio.query.filter_by(id=turno.id_estudio).first()
            estudio.historial.append(HistorialEstado(estado="TURNO CANCELADO"))
            Notificacion.send_mail(estudio.id_paciente, f"El Turno para el estudio {estudio.id} ha vencido.")
        db.session.commit()
        return f(*args, **kwargs)
    return wrapped_function

def enviar_estudios_automaticamente(f):
    """
    Decorador que verifica si hay 100 estudios esperando envío,
    los procesa automáticamente y genera un archivo CSV con los IDs y las patologías.
    Guarda el PDF recibido de la api en la carpeta static/enviados_exterior y actualiza la tabla Exterior.
    """
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        print("Verificando si hay estudios para procesar automáticamente...")
        estudios = Estudio.query \
            .join(HistorialEstado, Estudio.id == HistorialEstado.estudio_id) \
            .filter(HistorialEstado.estado == "ESPERANDO ENVIO AL EXTERIOR") \
            .filter(Estudio.fecha_ingreso_central != None) \
            .order_by(Estudio.fecha_ingreso_central.asc()) \
            .limit(3) \
            .all()
        
        if len(estudios) == 3:
            csv_folder = os.path.join(os.getcwd(),'src', 'static', 'csv_files')  
            os.makedirs(csv_folder, exist_ok=True) 
            csv_file_path = os.path.join(csv_folder, 'estudios.csv')
            with open(csv_file_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['code', 'pathology']) 
                for estudio in estudios:
                    if estudio.tipo_estudio == "familiar":
                        for patologia in estudio.patologias:
                            csv_writer.writerow([estudio.id, patologia.nombre])
                    else:
                        csv_writer.writerow([estudio.id, "N/A" if not estudio.patologias else estudio.patologias[0].nombre])

            try:
                api = SnippetsAPI()
                pdf_content = api.crear_pdf(csv_file_path)
                if not pdf_content:
                    raise ValueError("No se pudo crear el PDF desde el endpoint.")
                
                exterior = Exterior(estado="ENVIADO AL EXTERIOR")
                db.session.add(exterior)
                db.session.flush()

                pdf_folder = os.path.join(os.getcwd(),'src', 'static', 'enviados_exterior')
                os.makedirs(pdf_folder, exist_ok=True)
                pdf_path = os.path.join(pdf_folder, f"{exterior.id}.pdf")
                with open(pdf_path, 'wb') as pdf_file:
                    pdf_file.write(pdf_content)

                exterior.enviados_path = pdf_path

                for estudio in estudios:
                    estudio.historial.append(HistorialEstado(estado="ENVIADO AL EXTERIOR"))
                    Notificacion.send_mail(estudio.id_paciente, f"Su estudio {estudio.id} ha sido enviado al exterior.")
                    exterior.estudios.append(estudio)

                db.session.commit()
                #flash(f'Estudios enviados y PDF guardado como {exterior.id}.pdf.', 'success')

            except Exception as e:
                db.session.rollback()
                #flash(f"Error al procesar los estudios: {str(e)}", 'error')

        return f(*args, **kwargs)
    return wrapped_function