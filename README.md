# Sistema de Gestión de Tareas con API REST y Base de Datos - 

**Programación sobre Redes — PFO 2 - NATUCCI PAULA "COMISION D"**

## Descripción

Este proyecto consiste en una aplicación cliente-servidor desarrollada en Python que permite registrar usuarios, iniciar sesión y acceder a una página de bienvenida protegida mediante autenticación.

El servidor utiliza Flask para implementar una API REST, mientras que el cliente de consola utiliza la biblioteca Requests para realizar solicitudes HTTP.

Los usuarios se almacenan en una base de datos SQLite y las contraseñas se protegen mediante funciones de hash.

## Tecnologías utilizadas

- Python
- Flask
- SQLite
- Requests
- Werkzeug
- Git y GitHub

## Estructura del proyecto

```text
PFO2-Gestion-Tareas/
├── servidor.py
├── cliente.py
├── requirements.txt
├── .gitignore
└── README.md
```

La base de datos `usuarios.db` se genera automáticamente al iniciar el servidor.

## Funcionalidades

- Registro de nuevos usuarios.
- Validación de credenciales.
- Almacenamiento de contraseñas mediante hash.
- Autenticación basada en sesiones.
- Acceso protegido a una página HTML.
- Cliente de consola con menú interactivo.
- Manejo de respuestas HTTP y errores de conexión.
- Cierre local de sesión.

## Endpoints de la API

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Comprueba que el servidor funciona. |
| POST | `/registro` | Registra un nuevo usuario. |
| POST | `/login` | Verifica las credenciales e inicia una sesión. |
| GET | `/tareas` | Devuelve una página HTML para usuarios autenticados. |

### Registro de usuarios

**POST `/registro`**

Ejemplo de JSON:

```json
{
  "usuario": "vale",
  "contraseña": "1234"
}
```

Respuestas posibles:

- `201 Created`: usuario registrado correctamente.
- `400 Bad Request`: datos inválidos.
- `409 Conflict`: el usuario ya existe.

### Inicio de sesión

**POST `/login`**

Recibe las credenciales del usuario y verifica la contraseña contra el hash almacenado en SQLite.

Respuestas posibles:

- `200 OK`: inicio de sesión exitoso.
- `400 Bad Request`: datos inválidos.
- `401 Unauthorized`: credenciales incorrectas.

### Acceso a tareas

**GET `/tareas`**

- `200 OK`: devuelve el HTML de bienvenida si existe una sesión autenticada.
- `401 Unauthorized`: rechaza el acceso cuando no existe una sesión válida.

## Instalación y ejecución

### 1. Clonar el repositorio

```powershell
git clone URL_DEL_REPOSITORIO
cd PFO2-Gestion-Tareas
```

### 2. Crear el entorno virtual

```powershell
python -m venv .venv
```

Activarlo en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

### 4. Configurar la clave secreta de Flask

En la terminal donde se ejecutará el servidor:

```powershell
$env:FLASK_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
```

Esta clave se utiliza para firmar las cookies de sesión y no debe publicarse en GitHub.

### 5. Iniciar el servidor

```powershell
python servidor.py
```

El servidor estará disponible en:

`http://127.0.0.1:5000`

### 6. Ejecutar el cliente

Abrir otra terminal, activar el entorno virtual y ejecutar:

```powershell
python cliente.py
```

El programa mostrará un menú con las siguientes opciones:

1. Registrar usuario.
2. Iniciar sesión.
3. Consultar tareas.
4. Cerrar sesión.
5. Salir.

## Pruebas realizadas

Se verificaron los siguientes escenarios:

| Prueba | Resultado esperado |
|---|---|
| Registro de usuario nuevo | HTTP 201 |
| Registro de usuario duplicado | HTTP 409 |
| Login con credenciales correctas | HTTP 200 |
| Login con contraseña incorrecta | HTTP 401 |
| Acceso a `/tareas` sin autenticación | HTTP 401 |
| Acceso a `/tareas` con autenticación | HTTP 200 y HTML |
| Acceso después del cierre local de sesión | HTTP 401 |

## Seguridad

Las contraseñas no se almacenan en texto plano, sino mediante hashes generados con Werkzeug.

Las consultas SQL utilizan parámetros para evitar la concatenación directa de datos ingresados por el usuario.

Flask utiliza cookies de sesión firmadas para conservar el estado de autenticación.

El cierre de sesión implementado en el cliente elimina las cookies locales; no invalida una cookie previamente copiada.

**Nota:** el proyecto está preparado para ejecutarse localmente con fines educativos. Para su publicación en un entorno de producción sería necesario configurar HTTPS, desactivar el modo de depuración y revisar la gestión de sesiones y secretos.

## Preguntas conceptuales

### ¿Por qué es importante utilizar hash para las contraseñas?

Porque permite almacenar una representación de la contraseña en lugar de su valor original. De esta manera, si alguien obtiene acceso a la base de datos, no encuentra directamente las contraseñas en texto plano.

Además, las funciones utilizadas permiten verificar las credenciales sin recuperar la contraseña original.

### ¿Qué ventajas ofrece SQLite?

SQLite es una base de datos liviana que no requiere instalar ni administrar un servidor independiente.

Permite almacenar información en un archivo local, se integra fácilmente con Python y resulta adecuada para aplicaciones pequeñas, prototipos y proyectos educativos.

## Consideraciones finales

El proyecto permite aplicar conceptos de arquitectura cliente-servidor, comunicación HTTP, API REST, autenticación, persistencia de datos y manejo de errores.

La implementación demuestra cómo un cliente Python puede comunicarse con un servidor Flask y acceder a recursos protegidos mediante una sesión autenticada.
