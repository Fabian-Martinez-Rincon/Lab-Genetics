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
            -- Dimensiones
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

            -- Tabla de hechos
            CREATE TABLE fact_estudios (
                id_estudio VARCHAR(255) PRIMARY KEY,
                id_tiempo INT NOT NULL,
                id_patologia INT,
                id_tipo_estudio INT NOT NULL,
                FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo),
                FOREIGN KEY (id_patologia) REFERENCES dim_patologia(id_patologia),
                FOREIGN KEY (id_tipo_estudio) REFERENCES dim_tipo_estudio(id_tipo_estudio)
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
