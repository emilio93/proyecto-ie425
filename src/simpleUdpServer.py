#!/usr/bin/env python

import socket
import sys

connectionIp = '127.0.0.1'
connectionPort = 5005
bufferSize = 32

while (1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((connectionIp, connectionPort))
    receivedData, addr = sock.recvfrom(int(bufferSize))
    response = receivedData.upper()
    sock.sendto(response, addr)