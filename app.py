from src.web import create_app

def main() -> int:
    """
    Función principal que ejecuta la aplicación Flask en modo de desarrollo.

    Esta función crea una instancia de la aplicación Flask utilizando la función
    `create_app` y la ejecuta con un certificado SSL autogenerado (adhoc) para 
    pruebas locales en un entorno de desarrollo.

    Returns:
        int: Código de salida. Retorna 0 si la aplicación se ejecuta correctamente.
    """
    app = create_app()
    app.run(ssl_context="adhoc")

    return 0
