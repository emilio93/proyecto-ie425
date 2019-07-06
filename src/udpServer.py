#!/usr/bin/env python

# Paquete de sockets.
import socket

# Paquete para llamadas a sistema.
import sys

# Paquete de utilidades compartidas en las aplicaciones.
import util

# Paquete de utilidades compartidas en las aplicaciones de servidor.
import serverUtil

# Se imprimen mensajes adicionales si se pone en True.
DEBUG = True

# Nombre de la aplicacion.
APP_NAME = "Servidor UDP"

# Comando de la aplicacion.
APP_CMD = "udpServer.py"

# Contadores de mensajes recibidos y enviados.
mssgReceivedCount = 0
mssgSentCount = 0

# Se obtienen los parametros del Servidor UDP.
# Los parametros son seleccionados por defecto o bien pasados en
# la linea de comandos.
connectionIp, connectionPort, bufferSize, helpFlag = util.parseParameters(
    sys.argv, DEBUG)

# En caso de solicitarse informacion de ayuda, se imprime y se termina el programa.
if (helpFlag):
    util.printHelp(APP_NAME, APP_CMD)
    sys.exit()

if (DEBUG):
    # Se indican datos del programa.
    util.printAppInfo(APP_NAME, connectionIp, connectionPort, bufferSize)

try:
    # Se crea el socket con direccion IPv4 y tipo datagrama(es decir, UDP).
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Se asignan valores de direccion y puerto al socket.
    sock.bind((connectionIp, connectionPort))

except socket.error as err_msg:
    # En caso de no poder crear la conexion, se indica y se termina el programa.
    util.error_handler(err_msg, ("%s: %s" % (APP_NAME, util.ERROR_CONN_INIT)))
    sys.exit()

# Se esperan datos indefinidamente.
while (1):
    # Se baja la bandera de salida.
    exitFlag = False

    try:
        # Se obtienen hasta bufferSize datos y direccion de conexion.
        receivedData, addr = sock.recvfrom(int(bufferSize))

    except socket.error as err_msg:
        # Se indica el error unicamente en el servidor,
        # dado que no se puede responder(no se dispone de addr).
        util.error_handler(
            err_msg, "%s: %s" % (APP_NAME, util.ERROR_CONN_RECIEVE))

        if (int(err_msg[0]) is 9):
            try:
                sock.close()
            except socket.error as err_msg:
                # Se indica el error unicamente en el servidor,
                # dado que no se puede responder(no se dispone de addr).
                util.error_handler(
                    err_msg, "%s: %s" % (APP_NAME, util.ERROR_CONN_CLOSE))

            sys.exit()

        continue

    # Se actualiza la cantidad de mensajes recibidos una vez que ha sido recibido un mensaje.
    mssgReceivedCount = mssgReceivedCount + 1

    if (DEBUG):
        # Se imprime direccion de conexion y mensaje recibidos.
        print("%s: %s" % (util.MESSAGE_CONN_ADDRESS, addr))
        print("%s: %s" % (util.MESSAGE_MSSG_RECEIVED_QTY, mssgReceivedCount))
        print("%s: %s" % (util.MESSAGE_MESSAGE_RECEIVED, receivedData))

    # Se manipula el mensaje, en caso que se trate de un comando, se le da el manejo adecuado.
    response, exitFlag, connectionIp, connectionPort, bufferSize, isCommand = serverUtil.parseMessageAsServer(
        receivedData, connectionIp, connectionPort, bufferSize)

    try:
        # Se envia la respuesta al cliente.
        sock.sendto(response, addr)

    except socket.error as err_msg:
        # En caso de error, se indica que no se mando el mensaje y se termina ciclo de ejecucion, es decir
        # atiende otra conexiones.
        util.error_handler(
            err_msg, ("%s: %s" % (APP_NAME, util.ERROR_CONN_SEND)))
        continue

    # Se actualiza la cantidad de mensajes enviados una vez que ha sido enviada.
    mssgSentCount =mssgSentCount + 1

    if (DEBUG):
        # Se indica el mensaje enviado
        if (isCommand):
            print("%s: %s" % (util.MESSAGE_CMD_RESPONSE, response))
        else:
            print("%s: %s" % (util.MESSAGE_MESSAGE_SENT, response))

        print("%s: %s" % (util.MESSAGE_MSSG_SENT_QTY, mssgSentCount))

    if (exitFlag):
        try:
            # Se cierra la conexion.
            sock.close()

            if (DEBUG):
                print("%s: %s" % (APP_NAME, util.MESSAGE_CONECTION_CLOSED))

        except socket.error as err_msg:
            # En caso de error se imprime el codigo y mensaje de error.
            util.error_handler(err_msg, ("%s: %s" %
                                            (APP_NAME, util.ERROR_CONN_CLOSE)))

        sys.exit()
