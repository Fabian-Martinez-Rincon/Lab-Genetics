from werkzeug.security import generate_password_hash
import json

# Lista de usuarios en formato JSON como string
usuarios_json = '''
[
{
        "nombre": "Administrador General",
        "apellido": "Fabian",
        "password": "hola12345",
        "email": "fabianmartinezrincon.123@gmail.com",
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