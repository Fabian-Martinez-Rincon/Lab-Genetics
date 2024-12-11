import psycopg2
import os
from datetime import datetime

def migrar_datos():
    try:
        # Conexión a las bases de datos fuente y destino
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

        # Migrar Dimensión de Tiempo
        print("Migrando dimensión de tiempo...")
        source_cursor.execute("SELECT DISTINCT fecha_solicitud FROM estudios")
        fechas = source_cursor.fetchall()
        print(f"Fechas obtenidas: {fechas}")
        for (fecha,) in fechas:
            if fecha:
                mes = fecha.month
                trimestre = (mes - 1) // 3 + 1
                anio = fecha.year
                print(f"Insertando fecha: {fecha}, mes: {mes}, trimestre: {trimestre}, año: {anio}")
                dest_cursor.execute(
                    """
                    INSERT INTO dim_tiempo (fecha, mes, trimestre, anio)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (fecha) DO NOTHING;
                    """,
                    (fecha, mes, trimestre, anio)
                )

        # Migrar Dimensión de Pacientes
        print("Migrando dimensión de pacientes...")
        source_cursor.execute("""
            SELECT DISTINCT id, nombre, apellido FROM usuarios 
            WHERE id_rol = (SELECT id FROM roles WHERE nombre = 'Paciente')
        """)
        pacientes = source_cursor.fetchall()
        print(f"Pacientes obtenidos: {pacientes}")
        for id_paciente, nombre, apellido in pacientes:
            print(f"Insertando paciente: {id_paciente}, {nombre}, {apellido}")
            dest_cursor.execute(
                """
                INSERT INTO dim_paciente (id_paciente, nombre, apellido)
                VALUES (%s, %s, %s)
                ON CONFLICT (id_paciente) DO NOTHING;
                """,
                (id_paciente, nombre, apellido)
            )

        # Migrar Dimensión de Médicos
        print("Migrando dimensión de médicos...")
        source_cursor.execute("""
            SELECT DISTINCT id, nombre, apellido FROM usuarios 
            WHERE id_rol = (SELECT id FROM roles WHERE nombre = 'Medico')
        """)
        medicos = source_cursor.fetchall()
        print(f"Médicos obtenidos: {medicos}")
        for id_medico, nombre, apellido in medicos:
            print(f"Insertando médico: {id_medico}, {nombre}, {apellido}")
            dest_cursor.execute(
                """
                INSERT INTO dim_medico (id_medico, nombre, apellido)
                VALUES (%s, %s, %s)
                ON CONFLICT (id_medico) DO NOTHING;
                """,
                (id_medico, nombre, apellido)
            )

        # Migrar Dimensión de Estados de Estudios
        print("Migrando dimensión de estados de estudios...")
        source_cursor.execute("SELECT DISTINCT id, estudio_id, estado, fecha_hora FROM historial_estados")
        historial_estados = source_cursor.fetchall()
        print(f"Historial de estados obtenidos: {historial_estados}")
        for id, estudio_id, estado, fecha_hora in historial_estados:
            print(f"Insertando estado: {estado}, estudio_id: {estudio_id}, fecha_hora: {fecha_hora}")
            dest_cursor.execute(
                """
                INSERT INTO dim_estado_estudio (id_estado, nombre_estado, id_estudio, fecha_hora)
                VALUES (DEFAULT, %s, %s, %s)
                ON CONFLICT (id, nombre_estado, id_estudio, fecha_hora) DO NOTHING;
                """,
                (id, estado, estudio_id, fecha_hora)
            )

        # Migrar Dimensión de Patologías
        print("Migrando dimensión de patologías...")
        source_cursor.execute("SELECT id, nombre FROM patologias")
        patologias = source_cursor.fetchall()
        print(f"Patologías obtenidas: {patologias}")
        for id_patologia, nombre in patologias:
            print(f"Insertando patología: {id_patologia}, {nombre}")
            dest_cursor.execute(
                """
                INSERT INTO dim_patologia (id_patologia, nombre)
                VALUES (%s, %s)
                ON CONFLICT (id_patologia) DO NOTHING;
                """,
                (id_patologia, nombre)
            )

        # Migrar Tabla de Hechos: Estudios
        print("Migrando tabla de hechos: estudios...")
        source_cursor.execute(
            """
            SELECT e.id, e.id_paciente, e.id_medico, e.fecha_solicitud, ep.patologia_id
            FROM estudios e
            LEFT JOIN estudios_patologias ep ON e.id = ep.estudio_id
            """
        )
        estudios = source_cursor.fetchall()
        print(f"Estudios obtenidos: {estudios}")
        for id_estudio, id_paciente, id_medico, fecha_solicitud, id_patologia in estudios:
            print(f"Procesando estudio: {id_estudio}, paciente: {id_paciente}, médico: {id_medico}, fecha: {fecha_solicitud}, patología: {id_patologia}")
            dest_cursor.execute(
                "SELECT id_tiempo FROM dim_tiempo WHERE fecha = %s",
                (fecha_solicitud,)
            )
            id_tiempo = dest_cursor.fetchone()
            if not id_tiempo:
                print(f"No se encontró id_tiempo para la fecha {fecha_solicitud}, omitiendo estudio...")
                continue
            dest_cursor.execute(
                """
                INSERT INTO fact_estudios (id_estudio, id_paciente, id_medico, id_tiempo, id_patologia, fecha_solicitud)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_estudio) DO NOTHING;
                """,
                (id_estudio, id_paciente, id_medico, id_tiempo[0], id_patologia, fecha_solicitud)
            )

        # Migrar Tabla de Hechos: Presupuestos
        print("Migrando tabla de hechos: presupuestos...")
        source_cursor.execute("SELECT id, fecha_vencimiento, montoFinal, id_estado FROM presupuestos")
        presupuestos = source_cursor.fetchall()
        print(f"Presupuestos obtenidos: {presupuestos}")
        for id_presupuesto, fecha_vencimiento, monto_final, id_estado in presupuestos:
            print(f"Procesando presupuesto: {id_presupuesto}, fecha_vencimiento: {fecha_vencimiento}, monto_final: {monto_final}, estado: {id_estado}")
            dest_cursor.execute(
                "SELECT id_tiempo FROM dim_tiempo WHERE fecha = %s",
                (fecha_vencimiento,)
            )
            id_tiempo = dest_cursor.fetchone()
            if not id_tiempo:
                print(f"No se encontró id_tiempo para la fecha {fecha_vencimiento}, omitiendo presupuesto...")
                continue
            dest_cursor.execute(
                """
                INSERT INTO fact_presupuestos (id_presupuesto, id_tiempo, monto_final, fecha_vencimiento, id_estado)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id_presupuesto) DO NOTHING;
                """,
                (id_presupuesto, id_tiempo[0], monto_final, fecha_vencimiento, id_estado)
            )

        # Confirmar migración
        dest_connection.commit()
        print("Datos migrados exitosamente.")

    except Exception as e:
        print(f"Error durante la migración: {e}")

    finally:
        source_cursor.close()
        source_connection.close()
        dest_cursor.close()
        dest_connection.close()

# Ejecutar migración
if __name__ == "__main__":
    migrar_datos()
