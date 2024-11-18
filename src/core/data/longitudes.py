import json
import random

def generar_coordenadas(base_latitud, base_longitud):
    """Genera coordenadas ligeramente modificadas para mantenerlas únicas."""
    return (
        round(base_latitud + random.uniform(-0.01, 0.01), 6),
        round(base_longitud + random.uniform(-0.01, 0.01), 6),
    )

def modificar_json(input_file, output_file):
    """Modifica el JSON existente para garantizar latitudes y longitudes únicas."""
    with open(input_file, 'r', encoding='utf-8') as f:
        laboratorios = json.load(f)

    # Diccionario para evitar duplicados en las coordenadas
    coordenadas_usadas = set()

    for laboratorio in laboratorios:
        base_latitud = laboratorio.get("latitud")
        base_longitud = laboratorio.get("longitud")

        if base_latitud is not None and base_longitud is not None:
            # Generar nuevas coordenadas hasta que sean únicas
            while True:
                nueva_latitud, nueva_longitud = generar_coordenadas(base_latitud, base_longitud)
                if (nueva_latitud, nueva_longitud) not in coordenadas_usadas:
                    coordenadas_usadas.add((nueva_latitud, nueva_longitud))
                    laboratorio["latitud"] = nueva_latitud
                    laboratorio["longitud"] = nueva_longitud
                    break

    # Guardar el nuevo JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(laboratorios, f, ensure_ascii=False, indent=4)

    print(f"Archivo modificado guardado como: {output_file}")

# Ejecución del programa
input_file = "laboratorios.json"  # Archivo original
output_file = "laboratorios2.json"  # Archivo modificado
modificar_json(input_file, output_file)
