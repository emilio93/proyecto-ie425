#!/usr/bin/env python

import socket
import sys

connectionIp='127.0.0.1'
connectionPort=5005
bufferSize=32

while(1):
    userMessage = raw_input("\nMensaje: ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((connectionIp, connectionPort))
    s.send(userMessage)
    k = len(userMessage)
    fullResponse = ""
    while (k > 0):
        data = s.recv(int(bufferSize))
        if not data: break
        fullResponse = fullResponse + data
        k = k - len(data)
    print("%s" % (fullResponse))
    s.close()
