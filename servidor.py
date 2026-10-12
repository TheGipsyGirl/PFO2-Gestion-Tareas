
import os
import sqlite3

from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

# Clave secreta para las sesiones de Flask.
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")


def inicializar_base_datos():
    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()

    print("Base de datos inicializada correctamente.")


@app.route("/")
def inicio():
    return "¡Bienvenido al sistema de gestión de tareas!"


# Registro de usuarios.
@app.route("/registro", methods=["POST"])
def registrar_usuario():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "Se requiere un objeto JSON"}), 400

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if (not isinstance(usuario, str) or not usuario.strip()
            or not isinstance(contraseña, str) or not contraseña):
        return jsonify({"error": "Usuario y contraseña son obligatorios"}), 400

    usuario = usuario.strip()

    # La contraseña se almacena como hash, no en texto plano.
    password_hash = generate_password_hash(contraseña)

    conexion = sqlite3.connect("usuarios.db")

    try:
        # Consulta parametrizada para insertar el usuario.
        conexion.execute(
            "INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)",
            (usuario, password_hash)
        )

        conexion.commit()

    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

    finally:
        conexion.close()

    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201


# Autenticación de usuarios.
@app.route("/login", methods=["POST"])
def iniciar_sesion():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "Se requiere un objeto JSON"}), 400

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if (not isinstance(usuario, str) or not usuario.strip()
            or not isinstance(contraseña, str) or not contraseña):
        return jsonify({"error": "Usuario y contraseña son obligatorios"}), 400

    usuario = usuario.strip()

    conexion = sqlite3.connect("usuarios.db")

    try:
        cursor = conexion.execute(
            "SELECT password_hash FROM usuarios WHERE usuario = ?",
            (usuario,)
        )

        resultado = cursor.fetchone()

    finally:
        conexion.close()

    # Comprobamos las credenciales contra el hash almacenado.
    if resultado is None or not check_password_hash(resultado[0], contraseña):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    # Guardamos el usuario autenticado en la sesión.
    session.clear()
    session["usuario"] = usuario

    return jsonify({"mensaje": "Inicio de sesión exitoso"}), 200


# Ruta protegida: requiere una sesión iniciada.
@app.route("/tareas", methods=["GET"])
def mostrar_tareas():
    if "usuario" not in session:
        return jsonify({
            "error": "Debes iniciar sesión para acceder a las tareas"
        }), 401

    usuario = session["usuario"]

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


if __name__ == "__main__":
    inicializar_base_datos()
    app.run(debug=True)
