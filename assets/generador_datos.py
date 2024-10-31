from faker import Faker
import random
import json

fake = Faker('es_ES')  # Generador de datos falsos en español de España

def generate_lab_data(n):
    cities = [
        {"city": "Buenos Aires", "lat_range": (-34.6037, -34.6037), "lon_range": (-58.3816, -58.3816)},
        {"city": "La Plata", "lat_range": (-34.9215, -34.9215), "lon_range": (-57.9545, -57.9545)},
        {"city": "Capital Federal", "lat_range": (-34.6037, -34.6037), "lon_range": (-58.3816, -58.3816)}
    ]
    labs = []

    for _ in range(n):
        city_info = random.choice(cities)
        lat = random.uniform(*city_info["lat_range"])
        lon = random.uniform(*city_info["lon_range"])
        lab = {
            "nombre": "Laboratorio " + fake.company(),
            "direccion": fake.street_address() + ", " + city_info["city"],
            "horarios": "8:00 a 16:00",
            "dias": "lunes a viernes",
            "telefono": fake.phone_number(),
            "email": fake.email(),
            "password": fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
            "address": city_info["city"],
            "id_rol": "3",
            "latitud": lat,
            "longitud": lon
        }
        labs.append(lab)

    return labs

# Generar 100 laboratorios
laboratorios = generate_lab_data(100)

# Guardar el resultado en un archivo JSON
with open('laboratorios.json', 'w', encoding='utf-8') as f:
    json.dump(laboratorios, f, ensure_ascii=False, indent=4)

print("Archivo 'laboratorios.json' creado y guardado exitosamente.")
