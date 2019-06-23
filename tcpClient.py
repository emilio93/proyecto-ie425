#!/usr/bin/env python

# Paquete de sockets.
import socket

# Paquete para llamadas a sistema.
import sys

# Paquete de utilidades compartidas en las aplicaciones.
import util

# Se imprimen mensajes adicionales si se pone en True.
DEBUG = True

# Se obtienen los parametros del Cliente TCP.
# Los parametros son seleccionados por defecto o bien pasados en
# la linea de comandos.
TCP_IP, TCP_PORT, BUFFER_SIZE, HELP_FLAG = util.parseParameters(
    sys.argv, DEBUG)

# En caso de solicitarse informacion de ayuda, se imprime y se termina el programa.
if (HELP_FLAG):
    print("Cliente TCP\n\nUSO:\n")
    print("  python ./tcpClient.py -h hostIp -p puerto -s tamanoBufer")
    print("  python ./tcpClient.py --host-ip hostIp --port puerto --buffer-size tamanoBufer")
    print("\nEjemplo:\n")
    print("  python ./tcpClient.py -h 127.0.0.1 -p 5005 -s 1024\n")
    # Salir del programa
    sys.exit()

if (DEBUG):
    print("Cliente TCP")
    print("IP: %s \nPuerto: %s" % (TCP_IP, TCP_PORT))
    print("Tamano de Buffer: %s" % (BUFFER_SIZE))

# Indefinidamente se espera un mensaje para enviar.
# El mensaje debe ser ingresado por el usuario.
# Luego se espera por la respuesta del servidor.
# Cuando llega la respuesta, se imprime, si el
# dato recibido o enviado es "exit", se termina
# la ejecucion del programa.
while(1):
    # Se obtiene el mensaje por el usuario.
    MESSAGE = util.getMessage()

    # Si el mensaje es "exit -f", se termina ejecucion del programa sin
    # comunicarse con el servidor.
    if (MESSAGE == "exit -f"):
        if (DEBUG): print "\nCerrando el Cliente.\n"
        sys.exit()

    # Se crea un socket con direccion IPv4 de tipo stream.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Se intenta conectar el socket con la direccion y puerto asignados.
        s.connect((TCP_IP, TCP_PORT))

    except socket.error as err_msg:
        # En caso de error se imprime el codigo y mensaje de error.
        util.error_handler(err_msg, "Cliente TCP: Conexion no establecida.")

        # Se regresa a inicio del while.
        continue

    try:
        # Se envia el mensaje por el usuario.
        s.send(MESSAGE)

        # Se imprimen los datos enviados.
        if (DEBUG): print "    Datos Enviados:", MESSAGE

    except socket.error as err_msg:
        # En caso de error se imprime el codigo y mensaje de error.
        util.error_handler(err_msg, "Cliente TCP: Mensaje no enviado.")

        # Se regresa a inicio del while.
        continue

    # Se obtiene la longitud de los datos a enviar.
    MESSAGE_LENGTH = len(MESSAGE)

    # Se inicializa contador regresivo con cantidad de
    # caracteres en el mensaje enviado
    k = MESSAGE_LENGTH

    # Se inicializa la variable datos
    data = ''

    try:
        # Se repite hasta que se haya recibido una cantidad
        # de datos igual(o mayor) a la enviada.
        while (k > 0):
            # Datos recibidos del servidor.
            data = s.recv(int(BUFFER_SIZE))

            # Se imprimen los datos recibidos.
            if (DEBUG): print "    Datos Recibidos:", data

            # Se decrementa el contador de bytes restantes.
            k = k - len(data)

    except socket.error as err_msg:
        # En caso de error se imprime el codigo y mensaje de error.
        util.error_handler(err_msg, "Cliente TCP: Mensaje no recibido.")

        # Se regresa a inicio del while.
        continue

    try:
        # Se cierra el socket.
        s.close()

    except socket.error as err_msg:
        # En caso de error se imprime el codigo y mensaje de error.
        util.error_handler(err_msg, "Cliente TCP: No se cerro la conexion.")

    # Si los datos enviados o recibidos son "exit", se termina ejecucion del programa.
    if (MESSAGE == "exit" or data == "exit"):
        if (DEBUG): print "\nCerrando el Cliente.\n"
        sys.exit()
