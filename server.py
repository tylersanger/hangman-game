import socket
from hangman import Hangman
from customException import InvalidInputHangmanError, ResponseLengthError
import json
import os
import threading

IP = "0.0.0.0"
port = 55987


def handle_client(conn, addr):

    gameOver = False
    strikes = 0
    clientMessage = ""
    print(f"Received connection from {addr[0]}.")

    clientMessage = conn.recv(1024).decode("ascii")

    if clientMessage == "READY":

        game = Hangman()
        game.play()

        while not gameOver:

            try:
                clientMessage = game.get_game_state().encode("ascii")
                conn.send(clientMessage)
                clientMessage = conn.recv(1024).decode("ascii")
                print(f'{addr[0]} guessed "{clientMessage}"')
                winner = game.check_guess(clientMessage)
                strikes = game.get_strikes()

                if strikes == 6:
                    conn.send("GAMEOVER".encode("ascii"))
                    clientMessage = f'You struck out and lost the game. The word was "{game.get_word_to_guess()}"'.encode(
                        "ascii"
                    )
                    conn.send(clientMessage)
                    conn.close()
                    gameOver = True

                if winner:
                    conn.send("GAMEOVER".encode("ascii"))
                    clientMessage = "You won the game!!".encode("ascii")
                    conn.send(clientMessage)
                    conn.close()
                    gameOver = True

            except Exception as e:
                error = str(e).encode("ascii")
                conn.send(error)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, port))
s.listen()
threads = []
connections = []

while True:

    try:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        connections.append(conn)
        threads.append(t)
        t.start()
    except KeyboardInterrupt:
        print("Server is shutting down...")
        break

for thread in threads:
    thread.join()

for connection in connections:
    connection.close()
s.close()
print("Goodbye...")
