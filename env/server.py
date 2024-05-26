import socket
import threading

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 59420

# Clientes conectados
clientes = {}

# Comunicación con el cliente
def manejar_cliente(cliente_socket, direccion):
    try:
        nombre_usuario = cliente_socket.recv(1024).decode('utf-8').split(':', 1)[1]
        clientes[cliente_socket] = nombre_usuario
        print(f"{nombre_usuario} se ha conectado desde {direccion}")
        actualizar_clientes()

        while True:
            mensaje = cliente_socket.recv(1024).decode('utf-8')
            tipo, contenido = mensaje.split(':', 1)
            if tipo == "MESSAGE":
                if contenido.strip().lower() == "chao":
                    print(f"{nombre_usuario} abandonó la conversación")
                    cliente_socket.send("DISCONNECT:".encode('utf-8'))
                    cliente_socket.close()
                    del clientes[cliente_socket]
                    actualizar_clientes()
                    break
                enviar_mensaje(nombre_usuario, contenido.strip())
            elif tipo == "DISCONNECT":
                print(f"{nombre_usuario} se ha desconectado")
                cliente_socket.send("DISCONNECT:".encode('utf-8'))
                cliente_socket.close()
                del clientes[cliente_socket]
                actualizar_clientes()
                break
    except:
        cliente_socket.close()
        del clientes[cliente_socket]
        actualizar_clientes()

# Enviar mensajes a todos los clientes excepto al emisor
def enviar_mensaje(emisor, mensaje):
    mensaje_enviar = f"{emisor}: {mensaje}"
    for cliente_socket, nombre_usuario in clientes.items():
        if nombre_usuario != emisor:
            cliente_socket.send(f"MESSAGE:{mensaje_enviar}".encode('utf-8'))

# Actualizar la lista de clientes conectados
def actualizar_clientes():
    lista_usuarios = ",".join(clientes.values())
    for cliente_socket in clientes.keys():
        cliente_socket.send(f"USER_LIST:{lista_usuarios}".encode('utf-8'))

# Iniciar el servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
print("Servidor iniciado y esperando conexiones...")

while True:
    cliente_socket, direccion = servidor.accept()
    hilo = threading.Thread(target=manejar_cliente, args=(cliente_socket, direccion))
    hilo.start()
