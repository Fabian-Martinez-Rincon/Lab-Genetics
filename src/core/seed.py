import os
import json
from datetime import datetime
from src.core.models.database import db
from src.core.models import Laboratorio, Usuario, Rol, Turno, Estado, Resultado, Estudio, Presupuesto, Pedido, Patologia
from src.core.models import HistorialEstado

def cargar_datos(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(dir_path, 'data', filename)
    with open(full_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def eliminar_y_agregar(entidad, datos):
    db.session.query(entidad).delete()
    for data in datos:
        # Si el campo 'fecha' está vacío, asigna la fecha actual
        if 'fecha' in data and not data['fecha']:
            data['fecha'] = datetime.today().date()
        
        # Si hay 'fecha_nacimiento', conviértela a datetime
        if 'fecha_nacimiento' in data:
            data['fecha_nacimiento'] = datetime.fromisoformat(data['fecha_nacimiento'])

        # Manejar la creación del ID para `Estudio`
        if entidad == Estudio:
            apellido_paciente = db.session.query(Usuario).filter_by(id=data["id_paciente"]).first().apellido
            #data["id"] = Estudio().generar_id(apellido_paciente)  # Genera el ID basado en el apellido del paciente
            data["fecha_solicitud"] = datetime.fromisoformat(data["fecha_solicitud"])
            data["fecha_ingreso_central"] = datetime.strptime(data["fecha_ingreso_central"], "%Y-%m-%d").date()
        db.session.add(entidad(**data))

def seed_db():
    try:
        entidades_datos = {
            Rol: 'roles.json',
            Usuario: 'usuarios.json',
            Laboratorio: 'laboratorios.json',
            Estado: 'estados.json',
            Resultado: 'resultados.json',
            #Presupuesto: 'presupuestos.json',
            Pedido: 'pedidos.json',
            #Estudio: 'estudios.json',
            #Turno: 'turnos.json',
            Patologia: 'patologias.json'
        }

        for entidad, archivo in entidades_datos.items():
            datos = cargar_datos(archivo)
            eliminar_y_agregar(entidad, datos)

        #historial_datos = cargar_datos('historial_estados.json')
        #eliminar_y_agregar_historial(HistorialEstado, historial_datos)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")

def eliminar_y_agregar_historial(entidad, datos):
    db.session.query(entidad).delete()
    for data in datos:
        # Convertir `fecha_hora` a datetime
        data['fecha_hora'] = datetime.fromisoformat(data['fecha_hora'])
        db.session.add(entidad(**data))