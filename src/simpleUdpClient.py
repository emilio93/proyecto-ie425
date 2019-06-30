#!/usr/bin/env python

import socket
import sys

connectionIp='127.0.0.1'
connectionPort=5005
bufferSize=32

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while (1):
    userMessage = raw_input("\nMensaje: ")
    sock.sendto(userMessage, (connectionIp, connectionPort))
    try:
        sock.settimeout(2)
        while (1):
            data, addr = sock.recvfrom(int(bufferSize))
            if not data: continue
            break
    except socket.timeout:
        print("ERROR: Timeout.")
        continue

    print("%s" % (data))

sock.close()
sys.exit()
