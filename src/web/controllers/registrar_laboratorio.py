from flask import Flask, render_template, request, redirect, flash, Blueprint
from src.core.models.database import db
from src.core.models.laboratorio import Laboratorio
import random
import string
from werkzeug.security import generate_password_hash

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
        horarios = request.form.get('horarios')
        telefono = request.form.get('telefono')
        dias = request.form.get('dias')  
        lat = request.form.get('latitud')  
        lng = request.form.get('longitud')
        laboratorio_existente = Laboratorio.query.filter(
            (Laboratorio.email == email) | (Laboratorio.nombre == nombre)
        ).first()

        if laboratorio_existente:
            flash("Ya existe un laboratorio con ese nombre o email", "error")
            return redirect('owner/registrar_laboratorio')

        # Generar una contraseña aleatoria
        password_aleatoria = generar_password_aleatoria()
        password_hash = generate_password_hash(password_aleatoria)

        # Crear un nuevo laboratorio
        nuevo_laboratorio = Laboratorio(
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
        # Enviar la contraseña por correo electrónico
        #enviar_correo_contraseña(email, password_aleatoria)
        flash("Laboratorio registrado correctamente. La contraseña ha sido enviada por correo electrónico.", "success")
        return redirect('/listar_laboratorios')

    return render_template('owner/registrar_laboratorio.html')

