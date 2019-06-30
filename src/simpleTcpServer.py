#!/usr/bin/env python

import socket
import sys

connectionIp='127.0.0.1'
connectionPort=5005
bufferSize=32

while(1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((connectionIp, connectionPort))
    s.listen(1)
    conn, addr = s.accept()
    receivedData = ""
    fullResponse = ""
    while(1):
        data = conn.recv(int(bufferSize))
        if not data: break
        receivedData = receivedData + data
        response = data.upper()
        conn.send(response)
        fullResponse = fullResponse + response
    conn.close()
