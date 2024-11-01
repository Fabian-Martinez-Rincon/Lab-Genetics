import requests

class SnippetsAPI:
    BASE_URL = "https://api.claudioraverta.com"

    def __init__(self):
        pass

    def obtener_genes_por_patologia(self, nombre_patologia):
        """
        Obtiene genes asociados a la patología especificada.
        
        :param nombre_patologia: Nombre de la patología
        :return: Lista de genes asociados o None en caso de error
        """
        url = f"{self.BASE_URL}/genes-analizar/{nombre_patologia}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx o 5xx
            return response.json()  # Retorna la respuesta JSON
        except requests.exceptions.HTTPError as err:
            print(f"Error al consultar la API: {err}")
            return None
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None

    def obtener_hallazgos_secundarios(self):
        """
        Obtiene la lista de hallazgos secundarios.
        
        :return: Lista de hallazgos secundarios o None en caso de error
        """
        url = f"{self.BASE_URL}/genes-hallazgos-secundarios/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"Error al consultar la API: {err}")
            return None
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None

    def crear_pdf(self, csv_file_path):
        """
        Crea un PDF a partir de un archivo CSV.
        
        :param csv_file_path: Ruta al archivo CSV
        :return: Respuesta de la API o None en caso de error
        """
        url = f"{self.BASE_URL}/pdf/"
        with open(csv_file_path, 'rb') as f:
            try:
                response = requests.post(url, files={'file': f})
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as err:
                print(f"Error al crear el PDF: {err}")
                return None
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                return None
