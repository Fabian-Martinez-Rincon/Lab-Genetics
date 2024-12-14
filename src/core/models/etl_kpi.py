import psycopg2
import os
from datetime import datetime

def migrar_datos():
    try:
        print("Conectando a las bases de datos...")
        source_connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port="5432"
        )
        dest_connection = psycopg2.connect(
            dbname="kpi_db",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port="5432"
        )

        source_cursor = source_connection.cursor()
        dest_cursor = dest_connection.cursor()

        print("Conexión establecida.")

        print("Migrando datos de 'Patologias'...")
        source_cursor.execute("SELECT id, nombre FROM patologias;")
        patologias = source_cursor.fetchall()
        for patologia in patologias:
            dest_cursor.execute(
                """
                INSERT INTO dim_patologia (id_patologia, nombre_patologia) 
                VALUES (%s, %s) 
                ON CONFLICT (id_patologia) DO NOTHING;
                """,
                (patologia[0], patologia[1])
            )

        print("Migrando datos de 'Estudios'...")
        source_cursor.execute("""
            SELECT 
                e.id, e.fecha_solicitud, e.tipo_estudio, ep.patologia_id
            FROM estudios e
            LEFT JOIN estudios_patologias ep ON e.id = ep.estudio_id;
        """)

        estudios = source_cursor.fetchall()
        for estudio in estudios:
            estudio_id = estudio[0]
            fecha_solicitud = estudio[1]
            tipo_estudio = estudio[2]
            id_patologia = estudio[3]

            if not fecha_solicitud or not tipo_estudio:
                print(f"Datos faltantes en el estudio {estudio_id}: fecha_solicitud={fecha_solicitud}, tipo_estudio={tipo_estudio}")
                continue

            fecha_solicitud_truncada = fecha_solicitud.date()  

            dest_cursor.execute(
                """
                INSERT INTO dim_tipo_estudio (tipo_estudio) 
                VALUES (%s) 
                ON CONFLICT (tipo_estudio) DO NOTHING;
                """,
                (tipo_estudio,)
            )

            dest_cursor.execute(
                "SELECT id_tipo_estudio FROM dim_tipo_estudio WHERE tipo_estudio = %s;",
                (tipo_estudio,)
            )
            tipo_estudio_row = dest_cursor.fetchone()
            if tipo_estudio_row is None:
                print(f"Error: No se pudo obtener id_tipo_estudio para tipo_estudio='{tipo_estudio}'")
                continue
            id_tipo_estudio = tipo_estudio_row[0]

            dest_cursor.execute(
                """
                INSERT INTO dim_tiempo (fecha, mes, trimestre, anio) 
                VALUES (%s, %s, %s, %s) 
                ON CONFLICT (fecha) DO NOTHING;
                """,
                (
                    fecha_solicitud_truncada,
                    fecha_solicitud_truncada.month,
                    (fecha_solicitud_truncada.month - 1) // 3 + 1,
                    fecha_solicitud_truncada.year
                )
            )

            dest_cursor.execute(
                "SELECT id_tiempo FROM dim_tiempo WHERE fecha = %s;",
                (fecha_solicitud_truncada,)
            )
            tiempo_row = dest_cursor.fetchone()
            if tiempo_row is None:
                print(f"Error: No se pudo obtener id_tiempo para fecha='{fecha_solicitud_truncada}'")
                continue
            id_tiempo = tiempo_row[0]

            dest_cursor.execute(
                """
                INSERT INTO fact_estudios (
                    id_estudio, id_tiempo, id_patologia, id_tipo_estudio
                ) VALUES (%s, %s, %s, %s) 
                ON CONFLICT (id_estudio) DO NOTHING;
                """,
                (estudio_id, id_tiempo, id_patologia, id_tipo_estudio)
            )

        dest_connection.commit()
        print("Migración completada exitosamente.")

        source_cursor.close()
        dest_cursor.close()
        source_connection.close()
        dest_connection.close()

    except Exception as e:
        print(f"Error durante la migración de datos: {e}")

if __name__ == "__main__":
    migrar_datos()
