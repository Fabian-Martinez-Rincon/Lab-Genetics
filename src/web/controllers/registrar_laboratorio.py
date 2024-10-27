from flask import Flask, render_template, request, redirect, flash, Blueprint
from src.core.models.database import db
from src.core.models.laboratorio import Laboratorio
import random
import string
from werkzeug.security import generate_password_hash
from src.core.models.notificacion import Notificacion
bp = Blueprint('registrar_laboratorio', __name__)

# Función para generar una contraseña aleatoria
def generar_password_aleatoria(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

@bp.route('/registrar_laboratorio', methods=['GET', 'POST'])
def registrar_laboratorio():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        direccion = request.form.get('direccion')
        hora_inicio = request.form.get('hora_inicio')
        hora_fin = request.form.get('hora_fin')
        horarios = f"{hora_inicio} - {hora_fin}"
        telefono = request.form.get('telefono')
        dias_seleccionados = request.form.getlist('dias')
        dias = ", ".join(dias_seleccionados)  
        lat = request.form.get('latitud')  
        lng = request.form.get('longitud')
        if not lat and not lng:
            flash("Debe seleccionar una ubicación en el mapa", "error")
            return render_template('owner/registrar_laboratorio.html', form=request.form)
        if hora_fin < hora_inicio:
            flash("La hora de cierre debe ser mayor a la hora de apertura", "error")
            return render_template('owner/registrar_laboratorio.html', form=request.form)
        laboratorio_existente = Laboratorio.query.filter(
            (Laboratorio.email == email) | (Laboratorio.nombre == nombre)
        ).first()

        if laboratorio_existente:
            flash("Ya existe un laboratorio con ese nombre o email", "error")
            return redirect('/registrar_laboratorio')

        # Generar una contraseña aleatoria
        password_aleatoria = generar_password_aleatoria()
        password_hash = generate_password_hash(password_aleatoria)
        id = str(Laboratorio.query.count() +1 ) + "743"
        # Crear un nuevo laboratorio
        nuevo_laboratorio = Laboratorio(
            id = int(id),
            nombre=nombre,
            direccion=direccion,
            horarios=horarios,
            dias=dias,
            telefono=telefono,
            email=email,
            password=password_hash,
            address=f"{lat},{lng}"
        )
        db.session.add(nuevo_laboratorio)
        db.session.commit()
        lab = Laboratorio.query.filter_by(email=email).first()
        descripcion = f"Su contraseña es: {password_aleatoria}"
        Notificacion.send_mail_Lab(lab.id, descripcion)
        # Enviar la contraseña por correo electrónico
        #enviar_correo_contraseña(email, password_aleatoria)
        flash("Laboratorio registrado correctamente. La contraseña ha sido enviada por correo electrónico.", "success")
        return redirect('/listar_laboratorios')

    return render_template('owner/registrar_laboratorio.html')

