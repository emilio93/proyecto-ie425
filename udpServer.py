import socket

import re

import sys

import util

DEBUG = True

# Se obtienen los parametros del Servidor UDP.
# Los parametros son seleccionados por defecto o bien pasados en
# la linea de comandos.
UDP_IP, UDP_PORT, BUFFER_SIZE, HELP_FLAG = util.parseParameters(
    sys.argv, DEBUG)

# Respuesta cuando se cierra el servidor.
EXIT_MESSAGE = "Cerrando el servidor."
EXIT_FLAG = False

# En caso de solicitarse informacion de ayuda, se imprime y se termina el programa.
if (HELP_FLAG):
    print("Servidor UDP\n\nUSO:\n")
    print("  python ./udpServer.py -h hostIp -p puerto -s tamanoBufer")
    print("  python ./udpServer.py --host-ip hostIp --port puerto --buffer-size tamanoBufer\n\nEjemplo:\n")
    print("  python ./udpServer.py -h 127.0.0.1 -p 5005 -s 20\n")
    # Salir del programa
    sys.exit()

# Se indican datos del programa.
if (DEBUG):
    print("Servidor UDP")
    print("IP: %s \nPuerto: %s\nTamano de Buffer: %s" %
          (UDP_IP, UDP_PORT, BUFFER_SIZE))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while (1):
    # Se baja la bandera de salida
    EXIT_FLAG = False

    try:
        data, addr = sock.recvfrom(int(BUFFER_SIZE))
        if (DEBUG):
            print '\nDireccion de conexion:', addr
            print "\n  Mensaje recibido:", data

        if (data == "exit"):
            # Levantar la bandera de salida.
            EXIT_FLAG = True

            # Actualizar datos con mensaje de salida del servidor.
            data = EXIT_MESSAGE

        elif (data == "info"):
            data = ("IP: %s, Puerto: %s, Tamano de Buffer: %s" % (UDP_IP, UDP_PORT, BUFFER_SIZE))
        elif (data == "info -h"):
            data = ("%s" % (UDP_IP))
        elif (data == "info -p"):
            data = ("%s" % (UDP_PORT))
        elif (data == "info -s"):
            data = ("%s" % (BUFFER_SIZE))
        elif ("update -s " in data):
            data = re.sub('\s+', ' ', data)
            BUFFER_SIZE = int(re.sub('update -s ', '', data))
            data = ("Tamano de buffer actualizado: %s" % (BUFFER_SIZE))
        else:
            data = util.manipulateData(data)

        sock.sendto(data, addr)
        if (DEBUG):
            print "  Mensaje enviado:", data

    except socket.error as err_msg:
        data = "Mensaje muy largo. Intentar de nuevo."
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (UDP_IP, UDP_PORT))
        util.error_handler(err_msg, "Servidor UDP: Mensaje recibido es muy largo, aumentar buffer para permitir mensajes mas largos.")

    if (EXIT_FLAG):
        try:
            # Se cierra la conexion.
            sock.close()
        except socket.error as err_msg:
            # En caso de error se imprime el codigo y mensaje de error.
            util.error_handler(err_msg, "Servidor TCP: No se cerro la conexion.")
        sys.exit()

sock.close()