import psycopg2
import os

def crear_base_de_datos():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port="5432"
        )
        cursor = connection.cursor()

        cursor.execute("COMMIT;")
        cursor.execute("CREATE DATABASE kpi_db;")

        connection.commit()
        cursor.close()
        connection.close()

        print("Base de datos 'kpi_db' creada exitosamente.")

        connection = psycopg2.connect(
            dbname="kpi_db",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port="5432"
        )
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE dim_tiempo (
                id_tiempo SERIAL PRIMARY KEY,
                fecha DATE NOT NULL,
                mes INT NOT NULL,
                trimestre INT NOT NULL,
                anio INT NOT NULL,
                CONSTRAINT unique_fecha UNIQUE (fecha)
            );

            CREATE TABLE dim_patologia (
                id_patologia SERIAL PRIMARY KEY,
                nombre_patologia VARCHAR(255) NOT NULL,
                descripcion TEXT
            );

            CREATE TABLE dim_tipo_estudio (
                id_tipo_estudio SERIAL PRIMARY KEY,
                tipo_estudio VARCHAR(50) NOT NULL UNIQUE,
                descripcion TEXT
            );

            CREATE TABLE dim_localidad (
                id_localidad SERIAL PRIMARY KEY,
                nombre_localidad VARCHAR(255) NOT NULL UNIQUE
            );

            -- Tabla de hechos cantidad de estudios
            CREATE TABLE hechos_estudios (
                id_estudio VARCHAR(255) PRIMARY KEY,
                id_tiempo INT NOT NULL,
                id_patologia INT,
                id_tipo_estudio INT NOT NULL,
                FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo),
                FOREIGN KEY (id_patologia) REFERENCES dim_patologia(id_patologia),
                FOREIGN KEY (id_tipo_estudio) REFERENCES dim_tipo_estudio(id_tipo_estudio)
            );

            CREATE TABLE dim_estado (
                id_estado SERIAL PRIMARY KEY,
                nombre_estado VARCHAR(50) UNIQUE NOT NULL,
                descripcion TEXT
            );

            -- Tabla de hechos para tiempos de demora
            CREATE TABLE hechos_tiempos_demora (
                id_tiempo_demora SERIAL PRIMARY KEY,
                estudio_id VARCHAR(255) NOT NULL,
                id_estado_origen INT NOT NULL,
                id_estado_destino INT NOT NULL,
                id_tiempo_inicio INT NOT NULL,
                id_tiempo_fin INT NOT NULL,
                tiempo_demora INT NOT NULL, -- Tiempo en minutos
                id_patologia INT,
                id_tipo_estudio INT,
                FOREIGN KEY (estudio_id) REFERENCES hechos_estudios(id_estudio),
                FOREIGN KEY (id_estado_origen) REFERENCES dim_estado(id_estado),
                FOREIGN KEY (id_estado_destino) REFERENCES dim_estado(id_estado),
                FOREIGN KEY (id_tiempo_inicio) REFERENCES dim_tiempo(id_tiempo),
                FOREIGN KEY (id_tiempo_fin) REFERENCES dim_tiempo(id_tiempo),
                FOREIGN KEY (id_patologia) REFERENCES dim_patologia(id_patologia),
                FOREIGN KEY (id_tipo_estudio) REFERENCES dim_tipo_estudio(id_tipo_estudio)
            );

            -- Tabla de hechos para calcular las ganancias
            CREATE TABLE hechos_revenue (
                id_presupuesto INT PRIMARY KEY,
                id_tiempo INT NOT NULL,
                id_patologia INT,
                id_tipo_estudio INT NOT NULL,
                id_localidad INT NOT NULL,
                monto_final FLOAT NOT NULL,
                FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo),
                FOREIGN KEY (id_patologia) REFERENCES dim_patologia(id_patologia),
                FOREIGN KEY (id_tipo_estudio) REFERENCES dim_tipo_estudio(id_tipo_estudio),
                FOREIGN KEY (id_localidad) REFERENCES dim_localidad(id_localidad)
            );
        """)

        connection.commit()
        cursor.close()
        connection.close()

        print("Tablas creadas exitosamente en la base de datos 'kpi_db'.")

    except Exception as e:
        print(f"Error durante la creación de la base de datos: {e}")

if __name__ == "__main__":
    crear_base_de_datos()