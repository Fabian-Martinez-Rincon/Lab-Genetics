from werkzeug.security import generate_password_hash
import json

# Lista de usuarios en formato JSON como string
# LA CONTRA DE LOS LABORATORIOS ES lab12345 ya se encuentra hasheada en la seed
usuarios_json = '''
[
{
        "nombre": "Owner",
        "apellido": "",
        "password": "owner1234",
        "email": "owner@gmail.com",
        "dni": "12345678",
        "fecha_nacimiento": "1990-05-24",
        "telefono": "1122334455"
},
{
        "nombre": "",
        "apellido": "Fabian",
        "password": "administrador1234",
        "email": "administrador@gmail.com",
        "dni": "12345678",
        "fecha_nacimiento": "1990-05-24",
        "telefono": "1122334455"
},
{
        "nombre": "",
        "apellido": "Fabian",
        "password": "laboratorio1234",
        "email": "laboratorio@gmail.com",
        "dni": "12345678",
        "fecha_nacimiento": "1990-05-24",
        "telefono": "1122334455"
},
{
        "nombre": "",
        "apellido": "Fabian",
        "password": "medico1234",
        "email": "medico@gmail.com",
        "dni": "12345678",
        "fecha_nacimiento": "1990-05-24",
        "telefono": "1122334455"
},
{
        "nombre": "",
        "apellido": "Fabian",
        "password": "paciente1234",
        "email": "paciente1234",
        "dni": "12345678",
        "fecha_nacimiento": "1990-05-24",
        "telefono": "1122334455"
},
{
        "nombre": "",
        "apellido": "Fabian",
        "password": "transportista1234",
        "email": "transportista@gmail.com",
        "dni": "12345678",
        "fecha_nacimiento": "1990-05-24",
        "telefono": "1122334455"
}

]
'''

# Convertir el string JSON a una estructura de datos de Python
usuarios = json.loads(usuarios_json)

# Hashear las contraseñas de cada usuario
for usuario in usuarios:
    usuario['password'] = generate_password_hash(usuario['password'], method='pbkdf2:sha256')

# Imprimir los usuarios con las contraseñas hasheadas
print(json.dumps(usuarios, indent=4))