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
            response.raise_for_status()
            return response.json()
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
        :return: Contenido binario del PDF o None en caso de error
        """
        url = f"{self.BASE_URL}/pdf/"
        with open(csv_file_path, 'rb') as f:
            try:
                files = {'csv_file': (csv_file_path, f, 'text/csv')}
                response = requests.post(url, files=files)
                response.raise_for_status() 
                return response.content
            except requests.exceptions.HTTPError as err:
                print(f"Error al crear el PDF: {err}")
                return None
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                return None

    def confirmar_diagnostico(self, patologia, variantes):
        """
        Confirma si la patología está en la lista de variantes.
        
        :param patologia: Nombre de la patología
        :param variantes: Lista de variantes
        :return: True si la patología está en la lista de variantes, False en caso contrario o None en caso de error
        """
        url = f"{self.BASE_URL}/confirma-diagnostico/"
        data = {"patologia": patologia, "variantes": variantes}
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"Error al confirmar diagnóstico: {err}")
            return None
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None

    def obtener_lista_genes(self, page=None, page_size=None):
        """
        Obtiene la lista de genes.
        
        :param page: Número de página (opcional)
        :param page_size: Tamaño de página (opcional)
        :return: Lista de genes o None en caso de error
        """
        url = f"{self.BASE_URL}/lista-genes/"
        params = {"page": page, "page_size": page_size}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return [gene['nombre'] for gene in data.get("results", [])]
        except requests.exceptions.HTTPError as err:
            print(f"Error al obtener lista de genes: {err}")
            return None
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None

    def obtener_lista_sintomas(self, nombre=None, page=None, page_size=None):
        """
        Obtiene la lista de síntomas.
        
        :param nombre: Nombre del síntoma (opcional)
        :param page: Número de página (opcional)
        :param page_size: Tamaño de página (opcional)
        :return: Lista de síntomas o None en caso de error
        """
        url = f"{self.BASE_URL}/lista-sintomas/"
        params = {"nombre": nombre, "page": page, "page_size": page_size}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return [sintoma['nombre'] for sintoma in data.get("results", [])]
        except requests.exceptions.HTTPError as err:
            print(f"Error al obtener lista de síntomas: {err}")
            return None
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None

    def obtener_variantes_por_gen(self, nombre_gen):
        """
        Obtiene los nombres de las variantes asociadas al gen especificado.
        
        :param nombre_gen: Nombre del gen
        :return: Lista de nombres de variantes o None en caso de error
        """
        url = f"{self.BASE_URL}/variantes/{nombre_gen}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            variantes = response.json()
            nombres_variantes = [variante['nombre'] for variante in variantes]
            return nombres_variantes
        except requests.exceptions.HTTPError as err:
            print(f"Error al obtener variantes: {err}")
            return None
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None


    def obtener_hallazgos_secundarios_por_patologias(self, patologias):
        """
        Obtiene hallazgos secundarios basados en una lista de patologías diagnosticadas.
        
        :param patologias: Lista de patologías diagnosticadas
        :return: Lista de hallazgos secundarios o None en caso de error
        """
        url = f"{self.BASE_URL}/hallazgos-secundarios/"
        data = {"patologias": patologias}
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"Error al obtener hallazgos secundarios: {err}")
            return None
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None

    def sintomas_validos(self, patologia, sintomas):
            """
            Verifica si la lista de síntomas es válida con respecto a la patología.
            Devuelve True si la lista de síntomas es par, False si es impar.
            
            :param patologia: Nombre de la patología
            :param sintomas: Lista de síntomas
            :return: Un diccionario con 'valido': True/False o un mensaje de error
            """
            url = f"{self.BASE_URL}/sintomas-validos/"
            data = {
                "patologia": patologia,
                "sintomas": sintomas
            }
            try:
                response = requests.post(url, json=data)
                response.raise_for_status()
                return response.json() 
            except requests.exceptions.HTTPError as err:
                print(f"Error en el endpoint síntomas válidos: {err}")
                return {"error": str(err)}
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                return {"error": str(e)}