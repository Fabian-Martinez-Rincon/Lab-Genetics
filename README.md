<div align="center">

## 🥼 Lab-Genetics 🧪

<img src='https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjhzb3drcDhtaTZjNGtyaXJzdXNoYmdiYmQ4MTA5N2lxMDZjN3lwbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/d31vEN2v9DzBqEx2/giphy.gif'>

</div>

---

Marco de indagación para generar “Prototipo de solución”:

> “Un laboratorio que centraliza muestras biológicas (de otros laboratorios) para mandarlas a analizarlas al exterior quiere digitalizar su funcionamiento ya que actualmente no cuentan con un soporte digital”

- [🤝🏼 Para Colaborar](#-para-colaborar)
- [🧰 Recursos](#-recursos)
- [⚙️ Instalación](#️-instalación)
- [🕹️ Ejecución](#️-ejecución)
- [👨‍💻 Variables de Entorno](#-variables-de-entorno)
- [👤 Usuarios](#-usuarios)
    - [Administrador General](#administrador-general)
    - [Administrador de Laboratorio](#administrador-de-laboratorio)
    - [Medico](#medico)
    - [Paciente](#paciente)
    - [Transportista](#transportista)

---

### 🤝🏼 Para Colaborar

Para asegurarnos de que estamos en la rama main, antes de crear una mara

```bash
git branch
```

Si ya creamos una rama y queremos ir a esa, usamos

```bash
git checkout {nombre-rama}
```

Si no existe la rama, la creamos con un nombre descriptivo

```bash
git checkout -b {nombre-rama}
```

Una vez que estamos en la rama, hacemos un pull para asegurarnos de que estamos actualizados

```bash
git pull origin main
```

Hacemos la pull request

```bash
git add .
git commit -m "Mensaje descriptivo"
git push origin {nombre-rama}
```

---

### 🧰 Recursos

- [Python 3.8.10](https://www.python.org/downloads/release/python-3810/)
- [PGAdmin](https://www.pgadmin.org/download/pgadmin-4-windows/)

---

### ⚙️ Instalación

Creamos el entorno Virtual

```bash
python -m venv .venv
```

Activamos el entorno

```bash
.venv\Scripts\activate
```

En caso de no tener permisos

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Instalamos las dependencias (Solo hace falta la primera vez)

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

---

### 🕹️ Ejecución

```bash
flask resetdb
flask seeddb
```

Para correr la aplicación

```bash
livetw dev
```

O los siguientes dos

```bash
flask run --debug
livetw dev --no-flask
```

----

### 👨‍💻 Variables de Entorno

Para configurar las variables de entorno, copiamos y renombramos el archivo `.env.example` a `.env` y configuramos las variables de entorno.

```json
DB_PASS = "postgres"
DB_USER = "postgres"
DB_NAME = "localhost"
DB_HOST = "grupo08"
```

---

### 👤 Usuarios

- [Owner](#administrador-general)
- [Administrador de Laboratorio](#administrador-de-laboratorio)
- [Laboratorio](#laboratorio)
- [Medico](#medico)
- [Paciente](#paciente)
- [Transportista](#transportista)

> [!NOTE]  
> Las enfermedades raras son enfermedades geneticas

---

### Cuentas

- **Owner**
    - **Correo:**owner@gmail.com
    - **Contraseña:**owner1234
- **Administrador de Laboratorio**
    - **Correo:**administrador@gmail.com
    - **Contraseña:**administrador1234
- **Laboratorio**
    - **Correo:**laboratorio@gmail.com
    - **Contraseña:**laboratorio1234
- **Medico**
    - **Correo:**medico@gmail.com
    - **Contraseña:**medico1234
- **Paciente**
    - **Correo:**paciente@gmail.com
    - **Contraseña:**paciente1234
- **Transportista**
    - **Correo:**transportista@gmail.com
    - **Contraseña:**transportista1234

---