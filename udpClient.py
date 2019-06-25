#!/usr/bin/env python

# Paquete de sockets.
import socket

# Paquete para llamadas a sistema.
import sys

# Paquete de utilidades compartidas en las aplicaciones.
import util

# Paquete de utilidades compartidas en las aplicaciones de cliente.
import clientUtil

# Se imprimen mensajes adicionales si se pone en True.
DEBUG = True

# Nombre de la aplicacion.
APP_NAME = "Cliente UDP"

# Comando de la aplicacion.
APP_CMD = "./udpClient.py"

# Tiempo que se espera por la respuesta del servidor.
WAIT_FOR_RESPONSE = 2

# Se obtienen los parametros del Servidor UDP, ip, puerto y
# tamano de buffer en bytes.
# Los parametros son seleccionados por defecto o bien pasados en
# la linea de comandos.
connectionIp, connectionPort, bufferSize, helpFlag = util.parseParameters(
    sys.argv, DEBUG)

# En caso de solicitarse informacion de ayuda, se imprime y se termina el programa.
if (helpFlag):
    util.printHelp(APP_NAME, APP_CMD)
    # Se sale del programa
    sys.exit()

# Se indican datos del programa.
if (DEBUG):
    util.printAppInfo(APP_NAME, connectionIp, connectionPort, bufferSize)

try:
    # Se crea el socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

except socket.error as err_msg:
    # En caso de no poder crear la conexion, se indica y se termina el programa.
    util.error_handler(err_msg, ("%s: %s" % (APP_NAME, util.ERROR_CONN_INIT)))
    sys.exit()

while (1):

    # Se obtiene mensaje del usuario.
    userMessage = raw_input(util.MESSAGE_MESSAGE_REQUEST)

    # Se procesa el mensaje a enviar.
    parsedMessage, exitFlag, connectionIp, connectionPort, bufferSize, isCommand, isLocalOnly = clientUtil.parseMessageAsClient(
        userMessage, connectionIp, connectionPort, bufferSize)

    if (isCommand):
        # Si el mensaje es un comando, se indica la respuesta de ejecutarlo.
        if (DEBUG):
            print ("%s: %s" % (util.MESSAGE_CMD_RESPONSE, parsedMessage))

        # Si el comando es solo local, no hace falta enviarlo al servidor.
        if (isLocalOnly):
            if (exitFlag):
                # Se sale de la aplicacion.
                break
            continue

    try:
        # Se envia mensaje al servidor.
        sock.sendto(userMessage, (connectionIp, connectionPort))

    except socket.error as err_msg:
        # En caso de error, se indica que no se mando el mensaje y se termina ciclo de ejecucion.
        util.error_handler(
            err_msg, ("%s: %s" % (APP_NAME, util.ERROR_CONN_SEND)))
        continue

    # Se indica el mensaje enviado.
    if (DEBUG):
        print("%s: %s" % (util.MESSAGE_MESSAGE_SENT, userMessage))

    try:
        # Se espera un tiempo por la respuesta del servidor.
        sock.settimeout(WAIT_FOR_RESPONSE)
        while (1):
            try:
                # Se obtienen hasta bufferSize datos y direccion de conexion.
                data, addr = sock.recvfrom(int(bufferSize))
            except socket.error as err_msg:
                util.error_handler(
                    err_msg, ("%s: %s" % (APP_NAME, util.ERROR_CONN_RECIEVE)))
                break

            # Se espera hasta tener una respuesta.
            if not data:
                continue

            # Cuando llega la respuesta, se imprime y se deja de esperar.
            if (DEBUG):
                print("%s: %s" % (util.MESSAGE_MESSAGE_RECEIVED, data))
            break
    except socket.timeout:
        print("%s: %s" % (
            APP_NAME, util.ERROR_CONN_TIMEOUT))

    if (exitFlag):
        # Se sale de la aplicacion.
        break

try:
    # Se cierra la conexion.
    sock.close()
except socket.error as err_msg:
    # En caso de error se imprime el codigo y mensaje de error.
    util.error_handler(err_msg, ("%s: %s" % (APP_NAME, util.ERROR_CONN_CLOSE)))

# Se sale del programa.
sys.exit()
