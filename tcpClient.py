#!/usr/bin/env python

# Paquete de sockets.
import socket

# Paquete para llamadas a sistema.
import sys

# Paquete de utilidades compartidas en las aplicaciones.
import util

import clientUtil

# Se imprimen mensajes adicionales si se pone en True.
DEBUG = True

# Nombre de la aplicacion.
APP_NAME = "Cliente TCP"

# Comando de la aplicacion.
APP_CMD = "./tcpServer.py"

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

# Indefinidamente se espera un mensaje para enviar.
# El mensaje debe ser ingresado por el usuario.
# Luego se espera por la respuesta del servidor.
# Cuando llega la respuesta, se imprime, si el
# dato recibido o enviado es "exit", se termina
# la ejecucion del programa.
while(1):
    # Se obtiene el mensaje por el usuario.
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
                sys.exit()
            continue

    try:
        # Se crea un socket con direccion IPv4 de tipo stream.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Se intenta conectar el socket con la direccion y puerto asignados.
        s.connect((connectionIp, connectionPort))

    except socket.error as err_msg:
        # En caso de error se imprime el codigo y mensaje de error.
        util.error_handler(err_msg, "%s: %s" %
                           (APP_NAME, util.ERROR_CONN_INIT))

        # Se sale de la aplicacion si se habia indicado.
        if (exitFlag):
            sys.exit()

        # Se regresa a inicio del while.
        continue

    try:
        # Se envia el mensaje por el usuario.
        s.send(userMessage)

    except socket.error as err_msg:
        # En caso de error se imprime el codigo y mensaje de error.
        util.error_handler(err_msg, "%s: %s" %
                           (APP_NAME, util.ERROR_CONN_SEND))

        # Se sale de la aplicacion si se habia indicado.
        if (exitFlag):
            sys.exit()

        # Se regresa a inicio del while.
        continue

    # Se imprimen los datos enviados.
    if (DEBUG):
        print ("%s: %s" % (util.MESSAGE_MESSAGE_SENT, userMessage))

    # Se inicializa contador regresivo con cantidad de
    # caracteres en el mensaje enviado.
    k = len(userMessage)

    # Se inicializa la variable datos.
    data = ""
    fullResponse = ""
    # Se repite hasta que se haya recibido una cantidad
    # de datos igual(o mayor) a la enviada.
    while (k > 0):
        try:
            # Datos recibidos del servidor.
            data = s.recv(int(bufferSize))

        except socket.error as err_msg:
            # En caso de error se imprime el codigo y mensaje de error.
            util.error_handler(err_msg, "%s: %s" %
                               (APP_NAME, util.ERROR_CONN_RECIEVE))

            # Se sale de la aplicacion si se habia indicado o se cerro la
            # conexion en el servidor.
            if (exitFlag or int(err_msg[0]) is 10054):
                sys.exit()

            # Se regresa a inicio del while.
            continue

        fullResponse = fullResponse + data

        if not data:
            break

        # Se imprimen los datos recibidos.
        if (DEBUG):
            print ("  %s: %s" % (util.MESSAGE_MESSAGE_CHUNK_RECEIVED, data))

        # Se decrementa el contador de bytes restantes.
        k = k - len(data)

    # Se imprimen los datos recibidos.
    if (DEBUG):
        print ("%s: %s" % (util.MESSAGE_MESSAGE_RECEIVED, fullResponse))

    try:
        # Se cierra el socket.
        s.close()

    except socket.error as err_msg:
        # En caso de error se imprime el codigo y mensaje de error.
        util.error_handler(err_msg, "%s: $" %
                           (APP_NAME, util.ERROR_CONN_CLOSE))


    if (DEBUG):
        print ("  %s: %s" % (APP_NAME, util.MESSAGE_CONECTION_CLOSED))

    if (exitFlag):
        # Se sale de la aplicacion.
        sys.exit()