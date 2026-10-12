# Sistema de Gestión de Tareas con API REST y Base de Datos

**Programación sobre Redes – PFO 2**  
**Alumna:** Paula Valeria Natucci  
**Comisión:** D

## Descripción del proyecto

Para este trabajo práctico desarrollé una aplicación cliente-servidor en Python que permite registrar usuarios, iniciar sesión y acceder a una página de bienvenida.

El servidor está desarrollado con Flask y utiliza una base de datos SQLite para guardar los usuarios registrados. Las contraseñas se almacenan mediante hash utilizando Werkzeug, para evitar guardarlas directamente.

También desarrollé un cliente de consola con la biblioteca Requests, que permite interactuar con el servidor a través de un menú.

## Tecnologías utilizadas

- **Python:** lenguaje utilizado para desarrollar el servidor y el cliente.
- **Flask:** framework utilizado para crear la API REST.
- **SQLite:** base de datos donde se almacenan los usuarios.
- **Werkzeug:** permite generar y verificar los hashes de las contraseñas.
- **Requests:** biblioteca que utiliza el cliente para realizar solicitudes HTTP.
- **Git y GitHub:** control de versiones y publicación del proyecto.

## Estructura del proyecto

```text
PFO2-Gestion-Tareas/
├── servidor.py
├── cliente.py
├── requirements.txt
├── .gitignore
├── README.md
└── capturas/
```

El archivo `usuarios.db` se crea automáticamente cuando se inicia el servidor por primera vez.

## Funcionamiento

La aplicación cuenta con tres operaciones principales: registro de usuarios, inicio de sesión y acceso a la página de tareas.

### Registro de usuarios

**POST `/registro`**

Permite registrar un usuario nuevo. El servidor recibe los datos en formato JSON, comprueba que sean válidos y guarda el usuario en SQLite junto con el hash de su contraseña.

Ejemplo:

```json
{
  "usuario": "vale",
  "contraseña": "1234"
}
```

Posibles respuestas:

- **201:** usuario registrado correctamente.
- **400:** faltan datos o el formato es incorrecto.
- **409:** el usuario ya existe.

### Inicio de sesión

**POST `/login`**

Recibe el usuario y la contraseña, busca el usuario en la base de datos y verifica la contraseña con Werkzeug.

Si las credenciales son correctas, Flask crea una sesión para permitir el acceso a la página protegida.

Posibles respuestas:

- **200:** inicio de sesión exitoso.
- **400:** datos inválidos.
- **401:** credenciales incorrectas.

### Acceso a tareas

**GET `/tareas`**

Muestra una página HTML de bienvenida, pero solamente si el usuario inició sesión correctamente.

- **200:** acceso autorizado.
- **401:** acceso denegado.

También se incluye la ruta **GET `/`**, que permite comprobar que el servidor está funcionando.

## Instalación y ejecución

### 1. Clonar el repositorio

```powershell
git clone https://github.com/TheGipsyGirl/PFO2-Gestion-Tareas.git
cd PFO2-Gestion-Tareas
```

### 2. Crear y activar el entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

### 4. Configurar la clave secreta

Antes de ejecutar el servidor, configurar la variable de entorno que Flask utiliza para las sesiones:

```powershell
$env:FLASK_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Ejecutar el servidor

```powershell
python servidor.py
```

El servidor funciona localmente en `http://127.0.0.1:5000`.

### 6. Ejecutar el cliente

En otra terminal, con el entorno virtual activado:

```powershell
python cliente.py
```

El cliente muestra el siguiente menú:

```text
===== GESTIÓN DE TAREAS =====
1. Registrar usuario
2. Iniciar sesión
3. Consultar tareas
4. Cerrar sesión
5. Salir
```

Desde este menú se pueden realizar las operaciones sin necesidad de escribir manualmente las solicitudes HTTP.

## Pruebas realizadas

Para comprobar el funcionamiento del programa realicé las siguientes pruebas:

| Prueba | Resultado |
|---|---|
| Registro de un usuario nuevo | HTTP 201 |
| Registro de un usuario existente | HTTP 409 |
| Inicio de sesión correcto | HTTP 200 |
| Inicio de sesión con contraseña incorrecta | HTTP 401 |
| Acceso a tareas sin iniciar sesión | HTTP 401 |
| Acceso a tareas con sesión iniciada | HTTP 200 |
| Acceso a tareas después de cerrar sesión | HTTP 401 |

Las capturas de estas pruebas se encuentran en la carpeta `capturas`.

## Seguridad

Para las contraseñas utilicé las funciones `generate_password_hash()` y `check_password_hash()` de Werkzeug.

También utilicé consultas SQL parametrizadas y sesiones de Flask para controlar el acceso a `/tareas`.

El cierre de sesión del cliente elimina las cookies guardadas localmente. No invalida una cookie que se hubiera copiado anteriormente.

La aplicación está desarrollada para ejecutarse de manera local y con fines educativos. No está configurada para utilizarse directamente en producción.

## Preguntas conceptuales

### ¿Por qué es importante utilizar hash para las contraseñas?

Porque permite guardar una representación de la contraseña en lugar de almacenarla directamente. Esto ayuda a proteger los datos de los usuarios si alguien accede a la base de datos.

Cuando el usuario inicia sesión, se verifica la contraseña ingresada comparándola con el hash almacenado, sin necesidad de recuperar la contraseña original.

### ¿Qué ventajas ofrece SQLite?

SQLite es una base de datos sencilla que no necesita un servidor independiente. Toda la información se guarda en un archivo y se puede utilizar directamente desde Python.

Para este trabajo práctico resultó útil porque permite almacenar los usuarios sin tener que instalar o configurar un sistema de base de datos más complejo.

## Conclusión

Con este trabajo pude poner en práctica la comunicación entre un cliente y un servidor utilizando Python y solicitudes HTTP.

También trabajé con una API REST, una base de datos SQLite y un sistema básico de autenticación para controlar el acceso a determinadas rutas.

Las pruebas me permitieron comprobar tanto el funcionamiento correcto de las operaciones como las respuestas del servidor cuando se ingresan datos incorrectos o se intenta acceder sin iniciar sesión.