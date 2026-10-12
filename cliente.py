
# Importamos requests para enviar solicitudes HTTP.
import requests

# Guardamos la dirección donde funciona nuestro servidor Flask.
URL_SERVIDOR = "http://127.0.0.1:5000"
# Creamos una sesión HTTP para conservar las cookies.
sesion = requests.Session()

# Creamos una función para comprobar la conexión.
def comprobar_conexion():

    # Intentamos comunicarnos con el servidor.
    try:
        # Enviamos una solicitud GET a la ruta principal.
        respuesta = requests.get(URL_SERVIDOR, timeout=5)

        # Mostramos el código de estado HTTP.
        print("Código HTTP:", respuesta.status_code)

        # Mostramos el contenido recibido del servidor.
        print("Respuesta:", respuesta.text)

    # Si ocurre un problema de conexión, lo capturamos.
    except requests.exceptions.RequestException as error:
        print("No se pudo conectar con el servidor.")
        print("Detalle:", error)


# Función para registrar un usuario nuevo.
def registrar_usuario():

    # Solicitamos los datos desde la consola.
    usuario = input("Ingresá un nombre de usuario: ")
    contraseña = input("Ingresá una contraseña: ")

    # Preparamos los datos que enviaremos al servidor.
    datos = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    try:
        # Enviamos una solicitud POST al endpoint /registro.
        respuesta = requests.post(
            URL_SERVIDOR + "/registro",
            json=datos,
            timeout=5
        )

        # Mostramos el código HTTP recibido.
        print("Código HTTP:", respuesta.status_code)

        # Convertimos la respuesta JSON en un diccionario.
        resultado = respuesta.json()

        # Mostramos el mensaje del servidor.
        if "mensaje" in resultado:
            print(resultado["mensaje"])
        else:
            print("Error:", resultado.get("error", "Error desconocido"))

    # Controlamos posibles errores de conexión.
    except requests.exceptions.RequestException as error:
        print("No se pudo comunicar con el servidor.")
        print("Detalle:", error)


# Función para iniciar sesión con un usuario registrado.
def iniciar_sesion():

    # Solicitamos las credenciales.
    usuario = input("Ingresá tu usuario: ")
    contraseña = input("Ingresá tu contraseña: ")

    # Preparamos el JSON que espera Flask.
    datos = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    try:
        # Enviamos las credenciales usando nuestra sesión HTTP.
        respuesta = sesion.post(
            URL_SERVIDOR + "/login",
            json=datos,
            timeout=5
        )

        # Interpretamos la respuesta JSON.
        resultado = respuesta.json()

        # Mostramos el código HTTP.
        print("Código HTTP:", respuesta.status_code)

        # Si el login fue exitoso, informamos al usuario.
        if respuesta.status_code == 200:
            print(resultado["mensaje"])
            print("Sesión iniciada correctamente.")

        # Si las credenciales son incorrectas, mostramos el error.
        else:
            print("Error:", resultado.get("error", "Error desconocido"))

    # Capturamos los problemas de comunicación.
    except requests.exceptions.RequestException as error:
        print("No se pudo comunicar con el servidor.")
        print("Detalle:", error)


# Función para consultar la página protegida de tareas.
def consultar_tareas():

    try:
        # Enviamos una solicitud GET a /tareas.
        # Usamos la misma sesión para conservar la cookie.
        respuesta = sesion.get(
            URL_SERVIDOR + "/tareas",
            timeout=5
        )

        # Mostramos el código HTTP recibido.
        print("Código HTTP:", respuesta.status_code)

        # Si estamos autenticados, mostramos el HTML.
        if respuesta.status_code == 200:
            print("Acceso autorizado.")
            print(respuesta.text)

        # Si no iniciamos sesión, mostramos el error.
        elif respuesta.status_code == 401:
            print("Acceso denegado. Debés iniciar sesión.")

        # Controlamos otras respuestas inesperadas.
        else:
            print("Respuesta del servidor:", respuesta.text)

    # Capturamos errores de comunicación.
    except requests.exceptions.RequestException as error:
        print("No se pudo comunicar con el servidor.")
        print("Detalle:", error)


# Función que muestra el menú principal del cliente.
def mostrar_menu():

    # Repetimos el menú hasta que el usuario decida salir.
    while True:

        print("\n===== GESTIÓN DE TAREAS =====")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Consultar tareas")
        print("4. Cerrar sesión")
        print("5. Salir")

        # Solicitamos una opción al usuario.
        opcion = input("Elegí una opción: ")

        # Ejecutamos la función correspondiente.
        if opcion == "1":
            registrar_usuario()

        elif opcion == "2":
            iniciar_sesion()

        elif opcion == "3":
            consultar_tareas()

        elif opcion == "4":
            cerrar_sesion()

        elif opcion == "5":
            print("¡Hasta pronto!")
            break

        # Si la opción no existe, informamos el error.
        else:
            print("Opción inválida. Intentá nuevamente.")


# Función para cerrar la sesión del cliente.
def cerrar_sesion():

    # Eliminamos las cookies almacenadas por requests.
    sesion.cookies.clear()

    # Informamos que se cerró la sesión local.
    print("Sesión cerrada correctamente.")


# Este bloque se ejecuta cuando iniciamos cliente.py.
if __name__ == "__main__":
    mostrar_menu()