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
                INSERT INTO hechos_estudios (
                    id_estudio, id_tiempo, id_patologia, id_tipo_estudio
                ) VALUES (%s, %s, %s, %s) 
                ON CONFLICT (id_estudio) DO NOTHING;
                """,
                (estudio_id, id_tiempo, id_patologia, id_tipo_estudio)
            )

        print("Migrando datos de 'Tiempos de Demora'...")
        source_cursor.execute("""
            SELECT 
                he.estudio_id, 
                he.estado AS estado_origen, 
                LEAD(he.estado) OVER (PARTITION BY he.estudio_id ORDER BY he.fecha_hora) AS estado_destino,
                he.fecha_hora AS fecha_inicio,
                LEAD(he.fecha_hora) OVER (PARTITION BY he.estudio_id ORDER BY he.fecha_hora) AS fecha_fin
            FROM historial_estados he;
        """)

        historial = source_cursor.fetchall()
        for registro in historial:
            estudio_id = registro[0]
            estado_origen = registro[1]
            estado_destino = registro[2]
            fecha_inicio = registro[3]
            fecha_fin = registro[4]

            if not estado_destino or not fecha_fin:
                continue

            dest_cursor.execute(
                """
                INSERT INTO dim_estado (nombre_estado) 
                VALUES (%s) 
                ON CONFLICT (nombre_estado) DO NOTHING;
                """,
                (estado_origen,)
            )

            dest_cursor.execute(
                "INSERT INTO dim_estado (nombre_estado) VALUES (%s) ON CONFLICT (nombre_estado) DO NOTHING;",
                (estado_destino,)
            )

            dest_cursor.execute(
                "SELECT id_estado FROM dim_estado WHERE nombre_estado = %s;",
                (estado_origen,)
            )
            id_estado_origen = dest_cursor.fetchone()[0]

            dest_cursor.execute(
                "SELECT id_estado FROM dim_estado WHERE nombre_estado = %s;",
                (estado_destino,)
            )
            id_estado_destino = dest_cursor.fetchone()[0]

            dest_cursor.execute(
                "INSERT INTO dim_tiempo (fecha, mes, trimestre, anio) VALUES (%s, %s, %s, %s) ON CONFLICT (fecha) DO NOTHING;",
                (
                    fecha_inicio.date(),
                    fecha_inicio.month,
                    (fecha_inicio.month - 1) // 3 + 1,
                    fecha_inicio.year
                )
            )

            dest_cursor.execute(
                "INSERT INTO dim_tiempo (fecha, mes, trimestre, anio) VALUES (%s, %s, %s, %s) ON CONFLICT (fecha) DO NOTHING;",
                (
                    fecha_fin.date(),
                    fecha_fin.month,
                    (fecha_fin.month - 1) // 3 + 1,
                    fecha_fin.year
                )
            )

            dest_cursor.execute(
                "SELECT id_tiempo FROM dim_tiempo WHERE fecha = %s;",
                (fecha_inicio.date(),)
            )
            id_tiempo_inicio = dest_cursor.fetchone()[0]

            dest_cursor.execute(
                "SELECT id_tiempo FROM dim_tiempo WHERE fecha = %s;",
                (fecha_fin.date(),)
            )
            id_tiempo_fin = dest_cursor.fetchone()[0]

            tiempo_demora = int((fecha_fin - fecha_inicio).total_seconds() / 60)

            dest_cursor.execute(
                "SELECT id_patologia, id_tipo_estudio FROM hechos_estudios WHERE id_estudio = %s;",
                (estudio_id,)
            )
            estudio_info = dest_cursor.fetchone()
            id_patologia = estudio_info[0] if estudio_info else None
            id_tipo_estudio = estudio_info[1] if estudio_info else None

            dest_cursor.execute(
                """
                INSERT INTO hechos_tiempos_demora (
                    estudio_id, id_estado_origen, id_estado_destino, id_tiempo_inicio, id_tiempo_fin, tiempo_demora, id_patologia, id_tipo_estudio
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (estudio_id, id_estado_origen, id_estado_destino, id_tiempo_inicio, id_tiempo_fin, tiempo_demora, id_patologia, id_tipo_estudio)
            )

        print("Migrando datos de 'Revenue'...")
        source_cursor.execute(
            """
            SELECT 
                p.id AS id_presupuesto, 
                p.fecha_pago, 
                p."montoFinal", 
                e.tipo_estudio, 
                ep.patologia_id, 
                COALESCE(l.nombre, 'Sin Definir') AS nombre_localidad
            FROM presupuestos p
            INNER JOIN estudios e ON p.id = e.id_presupuesto
            LEFT JOIN estudios_patologias ep ON e.id = ep.estudio_id
            LEFT JOIN turnos t ON e.id = t.id_estudio AND t.estado = (SELECT id FROM estados WHERE nombre = 'ACEPTADO')
            LEFT JOIN laboratorios l ON t.id_laboratorio = l.id
            WHERE p.id_estado = (SELECT id FROM estados WHERE nombre = 'PAGADO');
            """
        )

        presupuestos = source_cursor.fetchall()

        for presupuesto in presupuestos:
            id_presupuesto = presupuesto[0]
            fecha_pago = presupuesto[1]
            monto_final = presupuesto[2]
            tipo_estudio = presupuesto[3]
            id_patologia = presupuesto[4]
            nombre_localidad = presupuesto[5]

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
            id_tipo_estudio = dest_cursor.fetchone()[0]

            dest_cursor.execute(
                """
                INSERT INTO dim_tiempo (fecha, mes, trimestre, anio)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (fecha) DO NOTHING;
                """,
                (
                    fecha_pago,
                    fecha_pago.month,
                    (fecha_pago.month - 1) // 3 + 1,
                    fecha_pago.year,
                ),
            )

            dest_cursor.execute(
                "SELECT id_tiempo FROM dim_tiempo WHERE fecha = %s;",
                (fecha_pago,)
            )
            id_tiempo = dest_cursor.fetchone()[0]

            dest_cursor.execute(
                """
                INSERT INTO dim_localidad (nombre_localidad)
                VALUES (%s)
                ON CONFLICT (nombre_localidad) DO NOTHING;
                """,
                (nombre_localidad,)
            )

            dest_cursor.execute(
                "SELECT id_localidad FROM dim_localidad WHERE nombre_localidad = %s;",
                (nombre_localidad,)
            )
            id_localidad = dest_cursor.fetchone()[0]

            dest_cursor.execute(
                """
                INSERT INTO hechos_revenue (
                    id_presupuesto, id_tiempo, id_patologia, id_tipo_estudio, id_localidad, monto_final
                ) VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_presupuesto) DO NOTHING;
                """,
                (
                    id_presupuesto, id_tiempo, id_patologia, id_tipo_estudio, id_localidad, monto_final
                ),
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
