import psycopg2
import os
from datetime import datetime

def crear_base_de_datos():
    try:
        # Conexión a la base de datos "postgres" para crear una nueva base de datos
        connection = psycopg2.connect(
            dbname="postgres",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port="5432"
        )
        cursor = connection.cursor()

        # Crear la base de datos "kpi_db"
        cursor.execute("COMMIT;")
        cursor.execute("CREATE DATABASE kpi_db;")

        # Confirmar y cerrar conexión inicial
        connection.commit()
        cursor.close()
        connection.close()

        print("Base de datos 'kpi_db' creada exitosamente.")

        # Conexión a la nueva base de datos "kpi_db"
        connection = psycopg2.connect(
            dbname="kpi_db",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port="5432"
        )
        cursor = connection.cursor()

        # Crear tablas del modelo estrella
        cursor.execute("""
            -- Dimensiones
            CREATE TABLE dim_tiempo (
                id_tiempo SERIAL PRIMARY KEY,
                fecha TIMESTAMP NOT NULL,
                mes INT NOT NULL,
                trimestre INT NOT NULL,
                anio INT NOT NULL,
                CONSTRAINT unique_fecha UNIQUE (fecha)
            );

            CREATE TABLE dim_paciente (
                id_paciente SERIAL PRIMARY KEY,
                nombre VARCHAR(255),
                apellido VARCHAR(255)
            );

            CREATE TABLE dim_medico (
                id_medico SERIAL PRIMARY KEY,
                nombre VARCHAR(255),
                apellido VARCHAR(255)
            );

            CREATE TABLE dim_estado_estudio (
                id_estado SERIAL PRIMARY KEY,
                nombre_estado VARCHAR(50) NOT NULL,
                id_estudio VARCHAR(50) NOT NULL,
                fecha_hora TIMESTAMP NOT NULL,
                CONSTRAINT unique_estado_estudio UNIQUE (nombre_estado, id_estudio, fecha_hora)
            );

            CREATE TABLE dim_presupuesto_estado (
                id_estado SERIAL PRIMARY KEY,
                nombre_estado VARCHAR(50) NOT NULL,
                CONSTRAINT unique_presupuesto_estado UNIQUE (nombre_estado)
            );

            CREATE TABLE dim_patologia (
                id_patologia SERIAL PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                descripcion TEXT
            );

            CREATE TABLE dim_presupuesto (
                id_presupuesto SERIAL PRIMARY KEY,
                monto FLOAT NOT NULL,
                fecha_vencimiento DATE NOT NULL,
                observaciones TEXT
            );

            -- Tablas de hechos
            CREATE TABLE fact_estudios (
                id_estudio VARCHAR(50) PRIMARY KEY,
                id_paciente INT NOT NULL,
                id_medico INT NOT NULL,
                id_estado INT NOT NULL,
                id_tiempo INT NOT NULL,
                id_patologia INT,
                fecha_solicitud TIMESTAMP,
                FOREIGN KEY (id_paciente) REFERENCES dim_paciente(id_paciente),
                FOREIGN KEY (id_medico) REFERENCES dim_medico(id_medico),
                FOREIGN KEY (id_estado) REFERENCES dim_estado_estudio(id_estado),
                FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo),
                FOREIGN KEY (id_patologia) REFERENCES dim_patologia(id_patologia)
            );

            CREATE TABLE fact_presupuestos (
                id_presupuesto SERIAL PRIMARY KEY,
                id_estado INT NOT NULL,
                id_tiempo INT NOT NULL,
                monto_final FLOAT NOT NULL,
                fecha_vencimiento DATE NOT NULL,
                FOREIGN KEY (id_estado) REFERENCES dim_presupuesto_estado(id_estado),
                FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo)
            );
        """)

        # Confirmar la creación de las tablas
        connection.commit()
        cursor.close()
        connection.close()

        print("Tablas creadas exitosamente en la base de datos 'kpi_db'.")

    except Exception as e:
        print(f"Error durante la creación de la base de datos: {e}")

# Ejecutar la función principal
if __name__ == "__main__":
    crear_base_de_datos()
