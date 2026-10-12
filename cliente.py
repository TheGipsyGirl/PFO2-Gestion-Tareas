
import requests


URL_SERVIDOR = "http://127.0.0.1:5000"

# La sesión conserva las cookies de autenticación.
sesion = requests.Session()


def comprobar_conexion():
    try:
        respuesta = requests.get(URL_SERVIDOR, timeout=5)

        print("Código HTTP:", respuesta.status_code)
        print("Respuesta:", respuesta.text)

    except requests.exceptions.RequestException as error:
        print("No se pudo conectar con el servidor.")
        print("Detalle:", error)


# Registro de usuarios mediante la API.
def registrar_usuario():
    usuario = input("Ingresá un nombre de usuario: ")
    contraseña = input("Ingresá una contraseña: ")

    datos = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    try:
        respuesta = requests.post(
            URL_SERVIDOR + "/registro",
            json=datos,
            timeout=5
        )

        print("Código HTTP:", respuesta.status_code)

        resultado = respuesta.json()

        if "mensaje" in resultado:
            print(resultado["mensaje"])
        else:
            print("Error:", resultado.get("error", "Error desconocido"))

    except requests.exceptions.RequestException as error:
        print("No se pudo comunicar con el servidor.")
        print("Detalle:", error)


# Inicio de sesión con las credenciales del usuario.
def iniciar_sesion():
    usuario = input("Ingresá tu usuario: ")
    contraseña = input("Ingresá tu contraseña: ")

    datos = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    try:
        # Usamos la sesión para conservar la cookie del login.
        respuesta = sesion.post(
            URL_SERVIDOR + "/login",
            json=datos,
            timeout=5
        )

        resultado = respuesta.json()

        print("Código HTTP:", respuesta.status_code)

        if respuesta.status_code == 200:
            print(resultado["mensaje"])
            print("Sesión iniciada correctamente.")
        else:
            print("Error:", resultado.get("error", "Error desconocido"))

    except requests.exceptions.RequestException as error:
        print("No se pudo comunicar con el servidor.")
        print("Detalle:", error)


# Consulta de la ruta protegida.
def consultar_tareas():
    try:
        # Reutilizamos la sesión para enviar la cookie.
        respuesta = sesion.get(
            URL_SERVIDOR + "/tareas",
            timeout=5
        )

        print("Código HTTP:", respuesta.status_code)

        if respuesta.status_code == 200:
            print("Acceso autorizado.")
            print(respuesta.text)

        elif respuesta.status_code == 401:
            print("Acceso denegado. Debés iniciar sesión.")

        else:
            print("Respuesta del servidor:", respuesta.text)

    except requests.exceptions.RequestException as error:
        print("No se pudo comunicar con el servidor.")
        print("Detalle:", error)


# Menú principal del cliente.
def mostrar_menu():
    while True:
        print("\n===== GESTIÓN DE TAREAS =====")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Consultar tareas")
        print("4. Cerrar sesión")
        print("5. Salir")

        opcion = input("Elegí una opción: ")

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

        else:
            print("Opción inválida. Intentá nuevamente.")


# Cierre local de sesión.
def cerrar_sesion():
    sesion.cookies.clear()
    print("Sesión cerrada correctamente.")


if __name__ == "__main__":
    mostrar_menu()
