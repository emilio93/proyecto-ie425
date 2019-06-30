#!/usr/bin/env python

# Paquete de expresiones regulares.
import re

# Tamano minimo de buffer.
MIN_BUFFER_SIZE = 16

# Mensajes a utilizar en la aplicacion.
MESSAGE_MESSAGE_REQUEST = "\nMensaje: "

MESSAGE_CONN_ADDRESS = "\nDireccion de conexion"
MESSAGE_MESSAGE_RECEIVED = "  Mensaje recibido"
MESSAGE_MESSAGE_CHUNK_RECEIVED = "  Trozo recibido"
MESSAGE_MESSAGE_SENT = "  Mensaje enviado"
MESSAGE_CHUNK_SENT = "  Trozo enviado"
MESSAGE_CMD_RESPONSE = "  Respuesta a comando"
MESSAGE_CONECTION_CLOSED = "Conexion cerrada"

ERROR_CONN_INIT = "Conexion no creada."
ERROR_CONN_SEND = "Mensaje no enviado."
ERROR_CONN_RECIEVE = "Mensaje no recibido."
ERROR_CONN_CLOSE = "Conexion no cerrada."
ERROR_CONN_TIMEOUT = "Se cumplio el timeout sin recibir una respuesta del servidor."

# Salir de aplicacion.
MESSAGE_EXIT = "Cerrando la aplicacion."
# Comando sin efectos.
MESSAGE_NO_ACTION = "Comando no aplica."
MESSAGE_INCORRECT_COMMAND = "Comando incorrecto."         # Comando incorrecto.

# Respuestas del servidor.
MESSAGE_SERVER_EXIT = "Cerrando el servidor."
MESSAGE_SERVER_NO_ACTION = MESSAGE_NO_ACTION
MESSAGE_SERVER_INCORRECT_COMMAND = MESSAGE_INCORRECT_COMMAND

# Respuestas del cliente.
MESSAGE_CLIENT_EXIT = "Cerrando el cliente."
MESSAGE_CLIENT_NO_ACTION = MESSAGE_NO_ACTION
MESSAGE_CLIENT_INCORRECT_COMMAND = MESSAGE_INCORRECT_COMMAND

# Expresion regular para comando exit.
EXIT_RE = "^exit\s*"
# Expresion regular para comando info.
INFO_RE = "^info\s*"
# Expresion regular para comando update.
UPDATE_RE = "^(update\s*|ud\s*)*"


def parseParameters(argv, DEBUG):
    "Obtener parametros ingresados mediante argumentos."

    # Bandera de debug en esta funcion
    FN_DEBUG = False

    # Parametros por defecto para el servidor y cliente.
    connectionIp = '127.0.0.1'  # Direccion Ip
    connectionPort = 5005      # Puerto
    bufferSize = 32     # Tamano del buffer
    helpFlag = True     # Bandera de ayuda(para imprimir texto de ayuda).

    # Imprimir informacion de argumentos y valores por defecto.
    if (DEBUG and FN_DEBUG):
        print ("argv:")
        print argv
        print ("\nValores por Defecto:")
        print ("  Ip: %s" % (connectionIp))
        print ("  Puerto: %s" % (connectionPort))
        print ("  Tamano de buffer: %s" % (bufferSize))
        print ("  Help Flag: %s\n" % (helpFlag))

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
            connectionIp = argv[i+1]
            helpFlag = False

        # Del mismo modo, las bandera -p o --port, cambian el puerto.
        elif ((i < argvLen-1) and (argv[i] == '-p' or argv[i] == '--port')):
            connectionPort = argv[i+1]
            helpFlag = False

        # Del mismo modo, las bandera -s o --buffer-size, cambian el tamano del buffer.
        elif ((i < argvLen-1) and (argv[i] == '-s' or argv[i] == '--buffer-size')):
            bufferSize = argv[i+1]
            helpFlag = False

        # Por defecto el valor de la bandera de ayuda es True,
        # si no ha sido bajada, se mantiene en alto.
        # Para imprimir la ayuda, solo esta bandera debe estar.
        elif (argv[i] == '--help'):
            helpFlag = helpFlag

        # Se incrementa el contador de argumentos.
        i = i+1

    # Bajar la bandera de ayuda si no se han pasado argumentos.
    if (argvLen <= 1):
        helpFlag = False

    # Imprimir la informacion de los datos a utilizar posterior a procesar los
    # argumentos.
    if (DEBUG and FN_DEBUG):
        print ("Valores a Utilizar:\n  Ip: %s\n  Puerto: %s" %
               (connectionIp, connectionPort))
        print ("  Tamano de buffer: %s\n  Help Flag: %s\n" %
               (bufferSize, helpFlag))

    # Se verifica tamano minimo de buffer
    if (bufferSize < MIN_BUFFER_SIZE):
        # Se aplica limite minimo de tamano de buffer
        bufferSize = MIN_BUFFER_SIZE

    # Se devuelve los tados de direccion ip, puerto, tamano de buffer y bandera de ayuda.
    return connectionIp, connectionPort, bufferSize, helpFlag


def printHelp(applicationName, command):
    "Imprime informacion de ayuda del programa."

    print("%s\nUSO:\n" % (applicationName))
    print("  python %s -h hostIp -p puerto -s tamanoBufer" % (command))
    print("  python %s --host-ip hostIp --port puerto --buffer-size tamanoBufer\n\nEjemplo:\n" % (command))
    print("  python %s -h 127.0.0.1 -p 5005 -s 20\n" % (command))
    pass


def printAppInfo(applicationName, ip, port, bufferSize):
    "Imprime la informacion del programa"

    print("%s" % (applicationName))
    print("  IP: %s" % (ip))
    print("  Puerto: %s" % (port))
    print("  Tamano de Buffer: %s" % (bufferSize))
    pass


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
    "Indica en que ambitos(cliente, servidor) funciona el comando."

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


def executeInfoCommand(commandString, connectionIp, connectionPort, bufferSize):
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


def executeUpdateCommand(commandString, connectionIp, connectionPort, bufferSize):
    "Ejecuta el comando de actualizar"

    # Bandera -s y --buffer-size
    if (re.match("^(-s|--buffer-size)\s*\d+$", commandString)):

        # Se obtiene el valor de buffer
        commandString = re.sub("^(-s|--buffer-size)\s*", "", commandString)

        # Se actualiza valor de buffer
        bufferSize = int(commandString)

        # Inicio del mensaje de respuesta
        commandString = ""

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
