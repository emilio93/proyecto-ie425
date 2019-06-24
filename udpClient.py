import socket

import sys

import util

DEBUG = True

# Se obtienen los parametros del Servidor UDP.
# Los parametros son seleccionados por defecto o bien pasados en
# la linea de comandos.
UDP_IP, UDP_PORT, BUFFER_SIZE, HELP_FLAG = util.parseParameters(
    sys.argv, DEBUG)

# En caso de solicitarse informacion de ayuda, se imprime y se termina el programa.
if (HELP_FLAG):
    print("Cliente UDP\n\nUSO:\n")
    print("  python ./udpClient.py -h hostIp -p puerto -s tamanoBufer")
    print("  python ./udpClient.py --host-ip hostIp --port puerto --buffer-size tamanoBufer\n\nEjemplo:\n")
    print("  python ./udpClient.py -h 127.0.0.1 -p 5005 -s 20\n")
    # Salir del programa
    sys.exit()

# Se indican datos del programa.
if (DEBUG):
    print("Servidor UDP")
    print("IP: %s \nPuerto: %s\nTamano de Buffer: %s" %
          (UDP_IP, UDP_PORT, BUFFER_SIZE))

while (1):
    MESSAGE = util.getMessage()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


    try:
        sock.settimeout(2)
        while (1):
            try:
                data, addr = sock.recvfrom(int(BUFFER_SIZE))
            except socket.error as err_msg:
                util.error_handler(err_msg, "Cliente UDP: No se recibio el mensaje.")
                break
            if not data: continue
            print "Mensaje Recibido:", data
            break
    except socket.timeout:
        print("Cliente UDP: Se cumplio el timeout sin recibir una respuesta, volver a intentar.")

    if (MESSAGE == "exit") :
        break
sock.close()
sys.exit()
