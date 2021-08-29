import socket
from hangman import Hangman
import json
import threading

IP = 'localhost'
port = 55987
players = {}

def handle_client(conn,addr,players):
    msg = ''

    print(f"Received connection from {addr[0]} on address {addr[1]}.")
    print(f"Player list is {players}.")
    while msg != 'q':
        msg = conn.recv(1024).decode('ascii')
        print(f"Received \"{msg}\" from client {addr[0]}.")
    
    conn.close()
    players.pop(addr[0])
    print(f"Player list {players}.")


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((IP,port))
s.listen()

while True:

    conn,addr = s.accept()
    players[addr[0]] = []
    threading._start_new_thread(handle_client,(conn,addr,players))




