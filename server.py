#!/usr/bin/python

import socket
from termcolor import colored

ip = "127.0.0.1"
port = 54321

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((ip,port))
s.listen(5)

print(colored("[+] Listening For Incoming Connections"))

target, ip = s.accept()
print(colored("[+] Connection Established From : {}".format(ip)))