import socket
import threading

# Configuración del cliente
HOST = '127.0.0.1'
PORT = 59420
nombre_usuario = input("Nombre de usuario: ")

# Recibir mensajes del servidor
def recibir_mensajes():
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            tipo, contenido = mensaje.split(':', 1)
            if tipo == "USER_LIST":
                print(f"Usuarios conectados: {contenido}")
            elif tipo == "MESSAGE":
                print(contenido)
            elif tipo == "DISCONNECT":
                print("Desconectado del servidor")
                cliente.close()
                break
        except:
            print("Desconectado del servidor")
            cliente.close()
            break

# Conexión al servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))
cliente.send(f"CONNECT:{nombre_usuario}".encode('utf-8'))

# Iniciar hilo para recibir mensajes
hilo_recibir = threading.Thread(target=recibir_mensajes)
hilo_recibir.start()

# Enviar mensajes al servidor
def enviar_mensaje():
    while True:
        mensaje = input()
        print(f"{nombre_usuario}: {mensaje}")
        cliente.send(f"MESSAGE:{mensaje}".encode('utf-8'))

# Iniciar hilo para enviar mensajes
hilo_enviar = threading.Thread(target=enviar_mensaje)
hilo_enviar.start()