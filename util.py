#!/usr/bin/env python

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
    print ('    Codigo de Error: ' + str(err_msg[0]))
    print ('    Mensaje de Error: ' + err_msg[1] + '\n')
    pass
