#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) #binds it to a specific ip and port so that it can listen to incoming requests on that ip and port
    s.listen() #puts the server into listen mode, allows the server to listen to incoming connections. Passing an empty string means that the server can listen to incoming connections from other computers as well.
    conn, addr = s.accept() #block and wait for an incoming connection
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)