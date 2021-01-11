import socket
from hangman import Hangman
import json
import threading

IP = 'localhost'
port = 55987
players = {}

def handle_client(conn,addr):
    msg = ''

    while msg != 'q':
        msg = conn.recv(1024).decode('ascii')
    
    conn.close()


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((IP,port))
s.listen()

while True:

    conn,addr = s.accept()
    players[addr[0]] = list((list(),0))
    threading._start_new_thread(handle_client,(conn,addr))




