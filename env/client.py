import socket

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 59420

# Función para enviar operaciones al servidor
def enviar_operacion(operacion, *args):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))
        mensaje = f"{operacion},{','.join(args)}"
        cliente.sendall(mensaje.encode())
        respuesta = cliente.recv(1024).decode()
        print(respuesta)
        cliente.close()
    except Exception as e:
        print(f"Error al enviar operación al servidor: {e}")

if __name__ == "__main__":
    print("Ejecuta las operaciones en el siguiente orden:")
    print("1. Agregar país")
    print("2. Agregar ciudad")
    print("3. Agregar localización")
    print("4. Agregar departamento")
    print("5. Agregar cargo")
    print("6. Agregar empleado")
    print("7. Consultar empleados")
    print("8. Eliminar empleado")
    print("9. Editar empleado")
    print("10. Salir")

    while True:
        opcion = input("Ingrese el número de la operación que desea realizar: ")

        if opcion == "1":
            nombre_pais = input("Ingrese el nombre del país: ")
            enviar_operacion("INSERT,paises", nombre_pais)
        elif opcion == "2":
            id_pais = input("Ingrese el ID del país al que pertenece la ciudad: ")
            nombre_ciudad = input("Ingrese el nombre de la ciudad: ")
            enviar_operacion("INSERT,ciudades", id_pais, nombre_ciudad)
        elif opcion == "3":
            id_ciudad = input("Ingrese el ID de la ciudad donde se encuentra la localización: ")
            direccion = input("Ingrese la dirección de la localización: ")
            enviar_operacion("INSERT,localizaciones", id_ciudad, direccion)
        elif opcion == "4":
            nombre_departamento = input("Ingrese el nombre del departamento: ")
            enviar_operacion("INSERT,departamentos", nombre_departamento)
        elif opcion == "5":
            nombre_cargo = input("Ingrese el nombre del cargo: ")
            sueldo_minimo = input("Ingrese el sueldo mínimo del cargo: ")
            sueldo_maximo = input("Ingrese el sueldo máximo del cargo: ")
            enviar_operacion("INSERT,cargos", nombre_cargo, sueldo_minimo, sueldo_maximo)
        elif opcion == "6":
            primer_nombre = input("Ingrese el primer nombre del empleado: ")
            segundo_nombre = input("Ingrese el segundo nombre del empleado (opcional): ")
            email = input("Ingrese el correo electrónico del empleado: ")
            fecha_nac = input("Ingrese la fecha de nacimiento del empleado (YYYY-MM-DD): ")
            sueldo = input("Ingrese el sueldo del empleado: ")
            comision = input("Ingrese la comisión del empleado (opcional): ")
            direccion = input("Ingrese la dirección del empleado: ")
            ciudad = input("Ingrese la ciudad del empleado: ")
            cargo_id = input("Ingrese el ID del cargo del empleado: ")
            gerente_id = input("Ingrese el ID del gerente del empleado (opcional): ")
            dpto_id = input("Ingrese el ID del departamento del empleado (opcional): ")
            enviar_operacion("INSERT,empleados", primer_nombre, segundo_nombre, email, fecha_nac, sueldo, comision, direccion, ciudad, cargo_id, gerente_id, dpto_id)
        elif opcion == "7":
            enviar_operacion("SELECT")
        elif opcion == "8":
            id_empleado = input("Ingrese el ID del empleado que desea eliminar: ")
            enviar_operacion("DELETE", id_empleado)
        elif opcion == "9":
            id_empleado = input("Ingrese el ID del empleado que desea editar: ")
            direccion = input("Ingrese la nueva dirección del empleado: ")
            ciudad = input("Ingrese la nueva ciudad del empleado: ")
            enviar_operacion("UPDATE", id_empleado, direccion, ciudad)
        elif opcion == "10":
            break
        else:
            print("Opción no válida. Por favor, ingrese un número del 1 al 10.")