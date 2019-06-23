#!/usr/bin/env python

# Paquete de sockets.
import socket

# Paquete para llamadas a sistema.
import sys

# Paquete de utilidades compartidas en las aplicaciones.
import util

# Se imprimen mensajes adicionales si se pone en True.
DEBUG = True

# Se obtienen los parametros del Servidor TCP.
# Los parametros son seleccionados por defecto o bien pasados en
# la linea de comandos.
TCP_IP, TCP_PORT, BUFFER_SIZE, HELP_FLAG = util.parseParameters(
    sys.argv, DEBUG)

# Respuesta cuando se cierra el servidor.
EXIT_MESSAGE = "Cerrando el servidor."
EXIT_FLAG = False

# En caso de solicitarse informacion de ayuda, se imprime y se termina el programa.
if (HELP_FLAG):
    print("Servidor TCP\n\nUSO:\n")
    print("  python ./tcpServer.py -h hostIp -p puerto -s tamanoBufer")
    print("  python ./tcpServer.py --host-ip hostIp --port puerto --buffer-size tamanoBufer\n\nEjemplo:\n")
    print("  python ./tcpServer.py -h 127.0.0.1 -p 5005 -s 20\n")
    # Salir del programa
    sys.exit()

# Se indican datos del programa.
if (DEBUG):
    print("Servidor TCP")
    print("IP: %s \nPuerto: %s\nTamano de Buffer: %s" %
          (TCP_IP, TCP_PORT, BUFFER_SIZE))


# Indefinidamente se escucha por nuevas conexiones.
while(1):

    # Se baja la bandera de salida
    EXIT_FLAG = False

    try:
        # Se crea un socket con direccion IPv4 de tipo stream.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Se le asigna la direccion IP y puerto al socket.
        s.bind((TCP_IP, TCP_PORT))

        # Se espera por una conexion.
        s.listen(1)

    except socket.error as err_msg:
        # En caso de error se imprime el codigo y mensaje de error.
        util.error_handler(err_msg, "Servidor TCP: Socket no creado.")

        # Se cierra el programa
        sys.exit()

    try:
        # Se acepta la coneccion, se guarda un objeto de conexion y la direccion.
        conn, addr = s.accept()
        if (DEBUG):
            print '\nDireccion de conexion:', addr

    except socket.error as err_msg:
        # En caso de error se imprime el codigo y mensaje de error.
        util.error_handler(err_msg, "Servidor TCP: Conexion no establecida.")

        # Se regresa a inicio del while.
        continue

    while(1):
        try:
            # Se almacena los datos recibidos en trozos de tamano
            # BUFFER_SIZE.
            data = conn.recv(int(BUFFER_SIZE))

        except socket.error as err_msg:
            # En caso de error se imprime el codigo y mensaje de error.
            util.error_handler(
                err_msg, "Servidor TCP: No se recibio el mensaje.")
            break

        # Si no hay mas datos, se sale del while.
        if not data:
            break

        # Se imprime el ultimo trozo capturado.
        if (DEBUG): print "    Datos Recibidos:", data

        if (data == "exit"):
            # Levantar la bandera de salida.
            EXIT_FLAG = True

            # Actualizar datos con mensaje de salida del servidor.
            data = EXIT_MESSAGE

        else:
            # Se realiza la manipulacion de los datos, en este caso se
            # pasa el texto a mayusculas.
            data = util.manipulateData(data)

        try:
            # Se envia los datos al cliente.
            conn.send(data)
        except socket.error as err_msg:
            # En caso de error se imprime el codigo y mensaje de error.
            util.error_handler(
                err_msg, "Servidor TCP: No se envio la respuesta.")

        # Se imprime datos enviados al cliente
        if (DEBUG): print "    Datos Enviados:", data, "\n"

    try:
        # Se cierra la conexion.
        conn.close()
        if (EXIT_FLAG):
            sys.exit()

    except socket.error as err_msg:
        # En caso de error se imprime el codigo y mensaje de error.
        util.error_handler(err_msg, "Servidor TCP: No se cerro la conexion.")
