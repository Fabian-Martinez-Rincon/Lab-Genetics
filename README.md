<div align="center">

## 🥼 Lab-Genetics 🧪

<img src='https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjhzb3drcDhtaTZjNGtyaXJzdXNoYmdiYmQ4MTA5N2lxMDZjN3lwbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/d31vEN2v9DzBqEx2/giphy.gif'>

</div>

---

Marco de indagación para generar “Prototipo de solución”:

> “Un laboratorio que centraliza muestras biológicas (de otros laboratorios) para mandarlas a analizarlas al exterior quiere digitalizar su funcionamiento ya que actualmente no cuentan con un soporte digital”

---

### Para Colaborar

- Para asegurarnos de que estamos en la rama main, antes de crear una mara
    ```bash
    git branch
    ```
- Si ya creamos una rama y queremos ir a esa, usamos
    ```bash
    git checkout {nombre-rama}
    ```
- Si no existe la rama, la creamos con un nombre descriptivo
    ```bash
    git branch {nombre-rama} o git checkout -b {nombre-rama}  //Para movernos despues de crearla
    ```
- Una vez que estamos en la rama, hacemos un pull para asegurarnos de que estamos actualizados
    ```bash
    git pull origin main
    ```
- Hacemos la pull request
    ```bash
    git add .
    git commit -m "Mensaje descriptivo"
    git push origin {nombre-rama}
    ```

---

### Requirements

- [Python 3.8.10](https://www.python.org/downloads/release/python-3810/)

---

### Instalación

- Paso 1 Creamos el entorno Virtual
    ```bash
    python -m venv .venv
    ```
- Paso 2 Activamos el entorno
    ```bash
    .venv\Scripts\activate
    ```
- Dependiendo el idioma
    ```bash
    .venv/Scripts/activate
    ```
- En caso de no tener permisos
    ```bash
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    ```
- Instalamos las dependencias (Solo hace falta la primera vez)
    ```bash
    pip install -r requirements.txt -r requirements-dev.txt
    ```
- No hace falta
    ```bash
    livetw init -d
    livetw build
    ```

---

### Ejecución

```bash
flask resetdb
flask seeddb
```

Para correr la aplicación

```bash
livetw dev
```

o los siguientes dos
```bash
flask run --debug
livetw dev --no-flask
```

----

Para configurar las variables de entorno, copiamos y renombramos el archivo `.env.example` a `.env` y configuramos las variables de entorno.

```json
DB_PASS = "password_example"
DB_USER = "user_example"
DB_NAME = "database_example"
DB_HOST = "host_example"
```

---

### Extensiones Recomendadas

- Pretier - Code formatter
- Headwind
- Error Lens
- Auto Close Tag
- Auto Rename Tag
- Image preview

---

#### Rutas para la primera demo

- `/eliminar_publicaciones`
- `/eliminar_colaboradores`
- `/eliminar_generales`