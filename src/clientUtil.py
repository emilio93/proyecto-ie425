#!/usr/bin/env python

import re

import util


def parseMessageAsClient(data, connectionIp, connectionPort, bufferSize):
    "Procesamiento del mensaje en el cliente"

    # Se asume que no se sale de la aplicacion.
    exitFlag = False

    # Se asume que no se trata de un comando.
    isCommand = False

    # Se asume que no es un comando local.
    isLocalOnly = False

    # Inicializacion del string de comando.
    commandString = data

    # Se chequean datos que comienzan con "$$ ".
    if (re.match("^\$\$\s+", data) is not None):
        # En caso que se comienza con "$$ ", se trata de un camando.
        isCommand = True

        # Se eliminan espacios blancos multiples de los datos.
        commandString = util.commandCleanup(data)

        while (1):
            # Comando de salida.
            commandString, exitFlag, isLocalOnly, commandFound = exitCommand(
                commandString)
            # Si se encuentra el comando, se termina el chequeo del comando
            if (commandFound):
                break

            # Comandos de informacion.
            commandString, isLocalOnly, commandFound = infoCommand(
                commandString, connectionIp, connectionPort, bufferSize)
            # Si se encuentra el comando, se termina el chequeo del comando
            if (commandFound):
                break

            # Comandos de actualizacion de parametros
            commandString, connectionIp, connectionPort, bufferSize, isLocalOnly, commandFound = updateCommand(
                commandString, connectionIp, connectionPort, bufferSize)
            # Si se encuentra el comando, se termina el chequeo del comando
            if (commandFound):
                break

            # Para otros casos se indica comando incorrecto.
            commandString = util.MESSAGE_CLIENT_INCORRECT_COMMAND
            break

    return commandString, exitFlag, connectionIp, connectionPort, bufferSize, isCommand, isLocalOnly


def exitCommand(commandString):
    "Chequea y ejecuta el comando de salir."

    isLocal = False
    isRemote = False

    # Se asume que no se termina la ejecucion del la aplicacion
    exitFlag = False

    # Se asume que no se ejecuta el comando
    commandFound = False

    # Se verifica si se trata del comando.
    if (re.match(util.EXIT_RE, commandString)):

        # Se indica que se ejecuta el comando.
        commandFound = True

        # Se indica si se trata de un comando local(para cliente) o remoto(para servidor).
        # Tambien puede ser un comando local y remoto.
        commandString, isLocal, isRemote = util.getCommandScope(
            commandString, util.EXIT_RE)

        if (isRemote):
            # Si se trata de un comando remoto, no se aplica accion
            commandString = util.MESSAGE_CLIENT_NO_ACTION

        if (isLocal):
            # Si se trata de un comando local,
            # se indica mensaje de salida de la aplicacion
            # y se levanta bandera de salida
            commandString = util.MESSAGE_CLIENT_EXIT
            exitFlag = True

    isLocalOnly = isLocal and not isRemote
    return commandString, exitFlag, isLocalOnly, commandFound


def infoCommand(commandString, connectionIp, connectionPort, bufferSize):
    "Verifica y ejecuta comando de informacion"

    # Se asume que no se ejecuta el comando
    commandFound = False

    isLocal = False
    isRemote = False

    # Se verifica si se trata del comando.
    if (re.match(util.INFO_RE, commandString)):

        # Se indica que se ejecuta el comando.
        commandFound = True

        # Se indica si se trata de un comando local(para cliente) o remoto(para servidor).
        # Tambien puede ser un comando local y remoto.
        commandString, isLocal, isRemote = util.getCommandScope(
            commandString, util.INFO_RE)

        # Si se trata de un comando local, se indica la informacion solicitada
        if (isLocal):
            commandString = util.executeInfoCommand(
                commandString, connectionIp, connectionPort, bufferSize)

        # Si se trata unicamente de un comando remoto, no se aplica accion.
        elif (isRemote):
            commandString = util.MESSAGE_CLIENT_NO_ACTION

    isLocalOnly = isLocal and not isRemote
    return commandString, isLocalOnly, commandFound


def updateCommand(commandString, connectionIp, connectionPort, bufferSize):
    "Verifica y ejecuta el comando de actualizar"

    # Se asume que no se ejecuta el comando
    commandFound = False

    isLocal = False
    isRemote = False

    # Se verifica si se trata del comando.
    if (re.match(util.UPDATE_RE, commandString)):

        # Se indica que se ejecuta el comando.
        commandFound = True

        # Se indica si se trata de un comando local(para cliente) o remoto(para servidor).
        # Tambien puede ser un comando local y remoto.
        commandString, isLocal, isRemote = util.getCommandScope(
            commandString, util.UPDATE_RE)

        # Si se trata de un comando local, se verifica la bandera y se actualiza el valor
        if (isLocal):
            commandString, connectionIp, connectionPort, bufferSize = util.executeUpdateCommand(
                commandString, connectionIp, connectionPort, bufferSize)

        # Si se trata unicamente de un comando remoto, no se aplica accion.
        elif (isRemote):
            commandString = util.MESSAGE_CLIENT_NO_ACTION

    isLocalOnly = isLocal and not isRemote
    return commandString, connectionIp, connectionPort, bufferSize, isLocalOnly, commandFound
