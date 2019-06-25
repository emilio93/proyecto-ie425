#!/usr/bin/env python

# Paquete de expresiones regulares.
import re

# Tamano minimo de buffer.
MIN_BUFFER_SIZE = 16

def parseParameters(argv, DEBUG):
    "Obtener parametros ingresados mediante argumentos."

    # Bandera de debug en esta funcion
    FN_DEBUG = False

    # Parametros por defecto para el servidor y cliente.
    TCP_IP = '127.0.0.1' # Direccion Ip
    TCP_PORT = 5005      # Puerto
    BUFFER_SIZE = 32     # Tamano del buffer
    HELP_FLAG = True     # Bandera de ayuda(para imprimir texto de ayuda).

    # Imprimir informacion de argumentos y valores por defecto.
    if (DEBUG and FN_DEBUG):
        print ("argv:")
        print argv
        print ("\nValores por Defecto:")
        print ("  Ip: %s" % (TCP_IP))
        print ("  Puerto: %s" % (TCP_PORT))
        print ("  Tamano de buffer: %s" % (BUFFER_SIZE))
        print ("  Help Flag: %s\n" % (HELP_FLAG))

    # Contador para while.
    i = 0

    # Limite para while.
    argvLen = len(argv)

    # Se itera por los argumentos pasados al comando.
    while i < argvLen:
        # Si el argumento es la bandera -h o --host-ip, se asigna nuevo
        # valor a direccion IP, el nuevo valor corresponde al argumento
        # luego de la bandera, si este argumento no existe, la direccion IP
        # no cambia.
        if ((i < argvLen-1) and (argv[i] == '-h' or argv[i] == '--host-ip')):
            TCP_IP = argv[i+1]
            HELP_FLAG = False

        # Del mismo modo, las bandera -p o --port, cambian el puerto.
        elif ((i < argvLen-1) and (argv[i] == '-p' or argv[i] == '--port')):
            TCP_PORT = argv[i+1]
            HELP_FLAG = False

        # Del mismo modo, las bandera -s o --buffer-size, cambian el tamano del buffer.
        elif ((i < argvLen-1) and (argv[i] == '-s' or argv[i] == '--buffer-size')):
            BUFFER_SIZE = argv[i+1]
            HELP_FLAG = False

        # Por defecto el valor de la bandera de ayuda es True,
        # si no ha sido bajada, se mantiene en alto.
        # Para imprimir la ayuda, solo esta bandera debe estar.
        elif (argv[i] == '--help'):
            HELP_FLAG = HELP_FLAG

        # Se incrementa el contador de argumentos.
        i = i+1

    # Bajar la bandera de ayuda si no se han pasado argumentos.
    if (argvLen <= 1):
        HELP_FLAG = False

    # Imprimir la informacion de los datos a utilizar posterior a procesar los
    # argumentos.
    if (DEBUG and FN_DEBUG):
        print ("Valores a Utilizar:\n  Ip: %s\n  Puerto: %s" %
               (TCP_IP, TCP_PORT))
        print ("  Tamano de buffer: %s\n  Help Flag: %s\n" %
               (BUFFER_SIZE, HELP_FLAG))

    # Se devuelve los tados de direccion ip, puerto, tamano de buffer y bandera de ayuda.
    return [TCP_IP, TCP_PORT, BUFFER_SIZE, HELP_FLAG]


def getMessage():
    "Mensaje a enviar"

    # Se lee el mensaje.
    MESSAGE = raw_input('\nMensaje: ')
    # Se devuelve el mensaje.
    return MESSAGE


def manipulateData(data):
    "Manipulacion de los datos por parte del servidor."

    # Se devuelven los caracteres recibidos en mayuscula
    # cuando aplica(ie, solo en letras).
    return data.upper()


def error_handler(err_msg, source):
    "Manejo de errores. Se imprimen los datos del error."

    print ("\nERROR")
    print ('    ' + str(source))
    try:
        err_msg[0], err_msg[1]
        print ('    Codigo de Error: ' + str(err_msg[0]))
        print ('    Mensaje de Error: ' + err_msg[1] + '\n')
    except IndexError:
        print '    Informacion de Error: ', err_msg, "\n"

    pass


def commandCleanup(commandString):
    "Limpia el comando, elimina indicador de comando y espacios en blanco multiples"

    # Eliminar $$ y espacios en blanco luego de esto.
    commandString = re.sub('^\$\$\s+', '', commandString)

    # Eliminar espacios en blanco al final del comando.
    commandString = re.sub('\s+$', '', commandString)

    # Eliminar multiples espacios seguidos.
    commandString = re.sub('\s+', ' ', commandString)

    return commandString


def getCommandScope(commandString, baseCommandRe):
    "Indica en que ambitos funciona el comando."

    # Se asume que no es local
    isLocal = False

    # Se asume que no es remoto
    isRemote = False

    # Se elimina comando base(eg, exit, info, ...).
    commandString = re.sub(baseCommandRe, "", commandString)

    # Se verifica si es local
    if (re.match("^local\s*", commandString)):
        isLocal = True
        # Se elimina indicador del comando
        commandString = re.sub("^local\s*", "", commandString)

    # Se verifica si es remoto
    elif (re.match("^remote\s*", commandString)):
        isRemote = True
        # Se elimina indicador del comando
        commandString = re.sub("^remote\s*", "", commandString)

    # Si no se indica, se aplica a local y remoto
    else:
        isLocal = True
        isRemote = True

    return commandString, isLocal, isRemote


#
# Ejecucion de comandos
#

def executeInfoCommand(commandString, bufferSize, connectionIp, connectionPort, MESSAGE_NO_ACTION):
    "Ejecuta el comando de informacion"

    if (commandString == ""):
        # Se devuelve toda la informacion
        commandString = ("IP: %s, Puerto: %s, Tamano de Buffer: %s" %
                         (connectionIp, connectionPort, bufferSize))
    elif (commandString == "-h"):
        # Se devuelve el ip.
        commandString = ("%s" % (connectionIp))

    elif (commandString == "-p"):
        # Se envia el puerto.
        commandString = ("%s" % (connectionPort))
    elif (commandString == "-s"):
        # Se envia el tamano de buffer.
        commandString = ("%s" % (bufferSize))
    else:
        # No se aplica accion en casos distintos
        commandString = MESSAGE_NO_ACTION

    return commandString


def executeUpdateCommand(commandString, connectionIp, connectionPort, bufferSize, MESSAGE_NO_ACTION):
    "Ejecuta el comando de actualizar"

    # Inicio del mensaje de respuesta
    commandString = ""

    # Bandera -h y --host-ip
    if (re.match("^(-h|--host-ip)\s*(\d{1,3}\.){3}\d{1,3}$", commandString)):

        # Se obtiene el valor de ip
        commandString = re.sub("^(-h|--host-ip)\s*", "", commandString)

        # Se actualiza valor de ip
        connectionIp = commandString

        # Se finaliza mensaje de respuesta
        commandString = ("Ip se actualiza a %s" %
                         (connectionIp)) + commandString

    # Bandera -p y --port
    if (re.match("^(-p|--port)\s*\d+$", commandString)):

        # Se obtiene el valor de puerto
        commandString = re.sub("^(-p|--port)\s*", "", commandString)

        # Se actualiza valor de puerto
        connectionPort = int(commandString)

        # Se finaliza mensaje de respuesta
        commandString = ("Puerto se actualiza a %s" %
                         (connectionPort)) + commandString

    # Bandera -s y --buffer-size
    elif (re.match("^(-s|--buffer-size)\s*\d+$", commandString)):

        # Se obtiene el valor de buffer
        commandString = re.sub("^(-s|--buffer-size)\s*", "", commandString)

        # Se actualiza valor de buffer
        bufferSize = int(commandString)

        # Se verifica tamano minimo de buffer
        if (bufferSize < MIN_BUFFER_SIZE):
            # Se aplica limite minimo de tamano de buffer
            bufferSize = MIN_BUFFER_SIZE
            # Se indica tamano minimo del buffer si se selecciono un valor menor
            commandString = ("(Minimo es %s)" % (MIN_BUFFER_SIZE))

        # Se finaliza mensaje de respuesta
        commandString = ("Tamano de buffer se actualiza a %s" %
                         (bufferSize)) + commandString

    else:
        # No se aplica accion en casos distintos
        commandString = MESSAGE_NO_ACTION

    return commandString, connectionIp, connectionPort, bufferSize
