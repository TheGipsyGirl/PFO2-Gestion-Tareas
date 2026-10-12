
# Importamos Flask para crear nuestro servidor web.
from flask import Flask, request, jsonify, session

# Importamos sqlite3 para trabajar con nuestra base de datos.
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


# Creamos la aplicación Flask.
app = Flask(__name__)

# Importamos herramientas para leer variables de entorno.
import os

# Clave utilizada por Flask para firmar las cookies de sesión.
# La leemos desde una variable de entorno por seguridad.
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")


# Esta función prepara la base de datos.
def inicializar_base_datos():

    # Conectamos con el archivo de base de datos.
    # Si no existe, SQLite lo crea automáticamente.
    conexion = sqlite3.connect("usuarios.db")

    # Creamos un cursor para ejecutar instrucciones SQL.
    cursor = conexion.cursor()

    # Creamos la tabla solamente si todavía no existe.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    # Guardamos los cambios realizados.
    conexion.commit()

    # Cerramos la conexión para liberar recursos.
    conexion.close()

    print("Base de datos inicializada correctamente.")


# Ruta principal para comprobar que Flask funciona.
@app.route("/")
def inicio():
    return "¡Bienvenido al sistema de gestión de tareas!"


# Endpoint para registrar nuevos usuarios.
# methods=["POST"] indica que recibe datos enviados por el cliente.
@app.route("/registro", methods=["POST"])
def registrar_usuario():

    # Obtenemos los datos JSON enviados por el cliente.
    datos = request.get_json(silent=True)

    # Verificamos que se haya enviado un objeto JSON.
    if not isinstance(datos, dict):
        return jsonify({"error": "Se requiere un objeto JSON"}), 400

    # Extraemos el usuario y la contraseña.
    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    # Validamos que ambos sean textos no vacíos.
    if (not isinstance(usuario, str) or not usuario.strip()
            or not isinstance(contraseña, str) or not contraseña):
        return jsonify({"error": "Usuario y contraseña son obligatorios"}), 400

    # Eliminamos espacios innecesarios del nombre de usuario.
    usuario = usuario.strip()

    # Generamos un hash seguro de la contraseña.
    password_hash = generate_password_hash(contraseña)

    # Abrimos una conexión con SQLite.
    conexion = sqlite3.connect("usuarios.db")

    try:
        # Insertamos los datos mediante una consulta parametrizada.
        # Los signos ? evitan concatenar datos directamente al SQL.
        conexion.execute(
            "INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)",
            (usuario, password_hash)
        )

        # Confirmamos los cambios.
        conexion.commit()

    except sqlite3.IntegrityError:
        # UNIQUE impide registrar dos usuarios con el mismo nombre.
        return jsonify({"error": "El usuario ya existe"}), 409

    finally:
        # Cerramos la conexión incluso si ocurre un error.
        conexion.close()

    # Respondemos indicando que el usuario fue creado.
    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201


# Endpoint para iniciar sesión.
# Solo acepta solicitudes HTTP POST.
@app.route("/login", methods=["POST"])
def iniciar_sesion():

    # Obtenemos los datos enviados por el cliente.
    datos = request.get_json(silent=True)

    # Comprobamos que recibimos un objeto JSON válido.
    if not isinstance(datos, dict):
        return jsonify({"error": "Se requiere un objeto JSON"}), 400

    # Extraemos las credenciales.
    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    # Verificamos que los campos sean textos no vacíos.
    if (not isinstance(usuario, str) or not usuario.strip()
            or not isinstance(contraseña, str) or not contraseña):
        return jsonify({"error": "Usuario y contraseña son obligatorios"}), 400

    # Quitamos espacios innecesarios del usuario.
    usuario = usuario.strip()

    # Abrimos la base de datos.
    conexion = sqlite3.connect("usuarios.db")

    try:
        # Buscamos el usuario mediante una consulta parametrizada.
        cursor = conexion.execute(
            "SELECT password_hash FROM usuarios WHERE usuario = ?",
            (usuario,)
        )

        # fetchone() devuelve una fila o None si no existe.
        resultado = cursor.fetchone()

    finally:
        # Cerramos la conexión con SQLite.
        conexion.close()

    # Verificamos si el usuario existe y la contraseña coincide.
    if resultado is None or not check_password_hash(resultado[0], contraseña):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    
    # Si las credenciales son correctas, limpiamos
    # cualquier información de una sesión anterior.
    session.clear()

    # Guardamos el nombre del usuario en la sesión.
    # Flask lo recordará mediante una cookie firmada.
    session["usuario"] = usuario

    # Confirmamos que inició sesión correctamente.
    return jsonify({"mensaje": "Inicio de sesión exitoso"}), 200


# Endpoint que muestra la página de bienvenida.
# Solamente permite solicitudes GET.
@app.route("/tareas", methods=["GET"])
def mostrar_tareas():

    # Comprobamos si existe un usuario autenticado.
    if "usuario" not in session:
        return jsonify({
            "error": "Debes iniciar sesión para acceder a las tareas"
        }), 401

    # Recuperamos el nombre del usuario desde la sesión.
    usuario = session["usuario"]

    # Construimos el HTML de bienvenida.
    # Flask devuelve este contenido como una página web.
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Gestión de Tareas</title>
    </head>
    <body>
        <h1>¡Bienvenido al sistema de gestión de tareas!</h1>
        <p>Has iniciado sesión correctamente.</p>
    </body>
    </html>
    """, 200, {"Content-Type": "text/html; charset=utf-8"}


# Punto de entrada de nuestro programa.
if __name__ == "__main__":

    # Preparamos la base de datos antes de iniciar el servidor.
    inicializar_base_datos()

    # Iniciamos Flask en modo desarrollo.
    app.run(debug=True)
