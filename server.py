import socket
from hangman import play
import json

IP = 'localhost'
port = 55987
players = {} 

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((IP,port))
s.listen()

conn,addr = s.accept()

players[]

