#!/usr/bin/env python

# Paquete de sockets.
import socket

# Paquete para llamadas a sistema.
import sys

# Paquete de utilidades compartidas en las aplicaciones.
import util

import serverUtil

# Se imprimen mensajes adicionales si se pone en True.
DEBUG = True

# Nombre de la aplicacion.
APP_NAME = "Servidor TCP"

# Comando de la aplicacion.
APP_CMD = "./udpServer.py"

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

# Indefinidamente se escucha por nuevas conexiones.
while(1):

    # Se baja la bandera de salida.
    exitFlag = False

    try:
        # Se crea un socket con direccion IPv4 de tipo stream.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Se le asigna la direccion IP y puerto al socket.
        s.bind((connectionIp, connectionPort))

        # Se espera por una conexion.
        s.listen(1)

    except socket.error as err_msg:
        # En caso de error se imprime el codigo y mensaje de error.
        util.error_handler(err_msg, "%s: Socket no creado." % (APP_NAME))

        # Se cierra el programa.
        sys.exit()

    try:
        # Se acepta la coneccion, se guarda un objeto de conexion y la direccion.
        conn, addr = s.accept()
        if (DEBUG):
            print '\nDireccion de conexion:', addr

    except socket.error as err_msg:
        # En caso de error se imprime el codigo y mensaje de error.
        util.error_handler(err_msg, "%s: %s", (APP_NAME, util.ERROR_CONN_INIT))

        # Se regresa a inicio del while.
        continue

    # Se inicializan los mensajes recibido y enviados completos.
    receivedData = ""
    fullResponse = ""

    # Se indica que se trata del primer pedazo recibido.
    isFirstChunk = True

    # Se asume que no se trata de un comando.
    isCommand = False

    while(1):
        try:
            # Se almacena los datos recibidos en trozos de tamano
            # BUFFER_SIZE.
            data = conn.recv(int(bufferSize))

        except socket.error as err_msg:
            # En caso de error se imprime el codigo y mensaje de error.
            util.error_handler(
                err_msg, "%s: %s", (APP_NAME, util.ERROR_CONN_RECIEVE))
            break

        # Si no hay mas datos, se sale del while.
        if not data:
            break

        # Se imprime el ultimo trozo capturado.
        if (DEBUG):
            if (not isFirstChunk):
                print("")
            print("  %s: %s" % (util.MESSAGE_MESSAGE_CHUNK_RECEIVED, data))

        # Se actualiza el valor de los datos recibidos completos.
        receivedData = receivedData + data

        # Se manipula el mensaje, en caso que se trate de un comando, se le da el manejo adecuado.
        response, exitFlag, connectionIp, connectionPort, bufferSize, isCommand = serverUtil.parseMessageAsServer(
            data, connectionIp, connectionPort, bufferSize)

        try:
            # Se envia los datos al cliente.
            conn.send(response)

        except socket.error as err_msg:
            # En caso de error se imprime el codigo y mensaje de error.
            util.error_handler(
                err_msg, "%s: %s", (APP_NAME, util.ERROR_CONN_SEND))
            continue

        # Se acualiza el valor de la respuesta completa.
        fullResponse = fullResponse + response

        # Se imprime datos recibidos del cliente.
        if (DEBUG):
            print("  %s: %s" % (util.MESSAGE_CHUNK_SENT, response))

        # Si se trata de un comando, solo se lee el primer pedazo.
        if (isFirstChunk and isCommand):
            isFirstChunk = False
            break

        # Se indica que ya no se trata del primer pedazo.
        isFirstChunk = False

    # Se imprime datos recibidos del cliente.
    if (DEBUG):
        print("%s: %s" % (util.MESSAGE_MESSAGE_RECEIVED, receivedData))

    # Se imprime datos recibidos del cliente.
    if (DEBUG):
        print("%s: %s" % (util.MESSAGE_MESSAGE_SENT, fullResponse))

    try:
        # Se cierra la conexion.
        conn.close()

    except socket.error as err_msg:
        # En caso de error se imprime el codigo y mensaje de error.
        util.error_handler(err_msg, "  %s: %s",
                           (APP_NAME, util.ERROR_CONN_CLOSE))
        sys.exit()

    # Se imprime datos recibidos del cliente.
    if (DEBUG):
        print("  %s: %s.\n" % (APP_NAME, util.MESSAGE_CONECTION_CLOSED))

    # Si la bandera de salida esta en alto, se sale del programa.
    if (exitFlag):
        sys.exit()
