import socket
import threading
import mysql.connector
from datetime import datetime

# Configuración de la base de datos
database = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="recursos_humanos",
    port=3306,
)

# Configuración del servidor socket
HOST = '127.0.0.1'
PORT = 59420

# Función para manejar las operaciones recibidas desde el cliente
def manejar_operacion(cliente_socket, direccion, mensaje):
    operacion, *args = mensaje.split(',')
    if operacion == "INSERT":
        tabla, *valores = args
        if tabla == "paises":
            respuesta = insertar_pais(*valores)
        elif tabla == "ciudades":
            respuesta = insertar_ciudad(*valores)
        elif tabla == "localizaciones":
            respuesta = insertar_localizacion(*valores)
        elif tabla == "departamentos":
            respuesta = insertar_departamento(*valores)
        elif tabla == "cargos":
            respuesta = insertar_cargo(*valores)
        elif tabla == "empleados":
            respuesta = agregar_empleado(*valores)
        else:
            respuesta = "Tabla no válida"
    elif operacion == "DELETE":
        respuesta = eliminar_empleado(*args)
    elif operacion == "UPDATE":
        respuesta = editar_empleado(*args)
    elif operacion == "SELECT":
        empleados = consultar_empleados()
        respuesta = "Empleados:\n"
        for empleado in empleados:
            respuesta += f"{empleado}\n"
    else:
        respuesta = "Operación no válida"
    
    cliente_socket.sendall(respuesta.encode())
    cliente_socket.close()

# Función para insertar un país en la base de datos
def insertar_pais(nombre_pais):
    try:
        cursor = database.cursor()
        sql = "INSERT INTO paises (pais_nombre) VALUES (%s)"
        cursor.execute(sql, (nombre_pais,))
        database.commit()
        id_pais = cursor.lastrowid
        cursor.close()
        return f"País agregado correctamente con ID {id_pais}"
    except Exception as e:
        return f"Error al agregar país: {e}"

# Función para insertar una ciudad en la base de datos
def insertar_ciudad(id_pais, nombre_ciudad):
    try:
        cursor = database.cursor()
        sql = "INSERT INTO ciudades (ciud_pais_id, ciud_nombre) VALUES (%s, %s)"
        cursor.execute(sql, (id_pais, nombre_ciudad,))
        database.commit()
        id_ciudad = cursor.lastrowid
        cursor.close()
        return f"Ciudad agregada correctamente con ID {id_ciudad}"
    except Exception as e:
        return f"Error al agregar ciudad: {e}"

# Función para insertar una localización en la base de datos
def insertar_localizacion(id_ciudad, direccion):
    try:
        cursor = database.cursor()
        sql = "INSERT INTO localizaciones (localiz_ciudad_id, localiz_direccion) VALUES (%s, %s)"
        cursor.execute(sql, (id_ciudad, direccion,))
        database.commit()
        id_localizacion = cursor.lastrowid
        cursor.close()
        return f"Localización agregada correctamente con ID {id_localizacion}"
    except Exception as e:
        return f"Error al agregar localización: {e}"

# Función para insertar un departamento en la base de datos
def insertar_departamento(nombre_departamento):
    try:
        cursor = database.cursor()
        sql = "INSERT INTO departamentos (depto_nombre) VALUES (%s)"
        cursor.execute(sql, (nombre_departamento,))
        database.commit()
        id_departamento = cursor.lastrowid
        cursor.close()
        return f"Departamento agregado correctamente con ID {id_departamento}"
    except Exception as e:
        return f"Error al agregar departamento: {e}"
    
# Función para insertar un cargo en la base de datos
def insertar_cargo(nombre_cargo, sueldo_minimo, sueldo_maximo):
    try:
        cursor = database.cursor()
        sql = "INSERT INTO cargos (cargo_nombre, cargo_sueldo_minimo, cargo_sueldo_maximo) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre_cargo, sueldo_minimo, sueldo_maximo,))
        database.commit()
        id_cargo = cursor.lastrowid
        cursor.close()
        return f"Cargo agregado correctamente con ID {id_cargo}"
    except Exception as e:
        return f"Error al agregar cargo: {e}"
    
# Función para consultar empleados en la base de datos
def consultar_empleados():
    try:
        cursor = database.cursor()
        cursor.execute("SELECT * FROM empleados")
        empleados = cursor.fetchall()
        cursor.close()
        return empleados
    except Exception as e:
        return f"Error al consultar empleados: {e}"

# Función para agregar un empleado a la base de datos
def agregar_empleado(primer_nombre, segundo_nombre, email, fecha_nac, sueldo, comision, direccion, ciudad, cargo_id, gerente_id, dpto_id):
    segundo_nombre = segundo_nombre if segundo_nombre.strip() else None
    comision = float(comision) if comision.strip() else None
    direccion = direccion if direccion.strip() else None
    ciudad = ciudad if ciudad.strip() else None
    cargo_id = int(cargo_id) if cargo_id.strip() else None
    gerente_id = int(gerente_id) if gerente_id.strip() else None
    dpto_id = int(dpto_id) if dpto_id.strip() else None

    try:
        cursor = database.cursor()
        sql = "INSERT INTO empleados (empl_primer_nombre, empl_segundo_nombre, empl_email, empl_fecha_nac, empl_sueldo, empl_comision, empl_direccion, empl_ciudad, empl_cargo_id, empl_gerente_id, empl_dpto_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (primer_nombre, segundo_nombre, email, fecha_nac, sueldo, comision, direccion, ciudad, cargo_id, gerente_id, dpto_id)
        cursor.execute(sql, data)
        database.commit()
        id_empleado = cursor.lastrowid
        cursor.close()
        return f"Empleado agregado correctamente con ID {id_empleado}"
    except Exception as e:
        return f"Error al agregar empleado: {e}"

# Función para eliminar un empleado de la base de datos
def eliminar_empleado(id_empleado):
    try:
        cursor = database.cursor()
        # Consulta para obtener los datos del empleado antes de eliminarlo
        cursor.execute("SELECT * FROM empleados WHERE empl_id = %s", (id_empleado,))
        empleado = cursor.fetchone()

        # Verificar la tupla del empleado antes de continuar
        print(empleado)

        # Insertar en la tabla historico
        fecha_retiro = datetime.now().date()  # Fecha actual como fecha de retiro
        sql_historico = "INSERT INTO historico (emphist_fecha_retiro, emphist_cargo_id, emphist_dpto_id) VALUES (%s, %s, %s)"
        data_historico = (fecha_retiro, empleado[9], empleado[11])
        cursor.execute(sql_historico, data_historico)

        # Eliminar al empleado de la tabla empleados
        sql_empleado = "DELETE FROM empleados WHERE empl_id = %s"
        cursor.execute(sql_empleado, (id_empleado,))
        
        database.commit()
        cursor.close()
        return "Empleado eliminado correctamente"
    except Exception as e:
        return f"Error al eliminar empleado: {e}"

# Función para editar los datos de un empleado en la base de datos
def editar_empleado(id_empleado, direccion, ciudad):
    try:
        cursor = database.cursor()
        sql = "UPDATE empleados SET empl_direccion = %s, empl_ciudad = %s WHERE empl_id = %s"
        data = (direccion, ciudad, id_empleado)
        cursor.execute(sql, data)
        database.commit()
        cursor.close()
        return "Empleado actualizado correctamente"
    except Exception as e:
        return f"Error al editar empleado: {e}"

# Función principal para manejar conexiones entrantes
def manejar_conexiones():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"Servidor socket iniciado y esperando conexiones en {HOST}:{PORT}")

    while True:
        cliente_socket, direccion = servidor.accept()
        print(f"Cliente conectado desde {direccion}")
        hilo = threading.Thread(target=atender_cliente, args=(cliente_socket, direccion))
        hilo.start()

# Función para atender las solicitudes del cliente
def atender_cliente(cliente_socket, direccion):
    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode()
            if mensaje:
                manejar_operacion(cliente_socket, direccion, mensaje)
            else:
                break
        except Exception as e:
            print(f"Error al recibir datos del cliente {direccion}: {e}")
            break

if __name__ == "__main__":
    manejar_conexiones()