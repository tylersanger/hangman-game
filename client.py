import socket
IP = 'localhost'
port = 55987

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((IP,port))

while True:
    msg = input("=> ")
    s.send(msg.encode('ascii'))

    if msg == 'q':
        break

print("Closing connection with server...")