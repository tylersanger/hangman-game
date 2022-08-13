import socket
from hangman import Hangman
from customException import ResponseLengthError, InvalidInputHangmanError
import json
import os
import threading

IP = "0.0.0.0"
port = 55987


def handle_client(conn, addr):

    gameOver = False
    strikes = 0
    data = {'STATE' : '', 'MESSAGE' : ''}
    clientMessage = ""
    print(f"Received connection from {addr[0]}.")

    clientMessage = conn.recv(1024).decode("ascii")

    if clientMessage == "READY":

        game = Hangman()
        game.play()

        while not gameOver:

            try:
                clientMessage = game.get_game_state()
                data['STATE'] = 'STATS'
                data['MESSAGE'] = clientMessage
                conn.send(json.dumps(data).encode("utf-8"))

                clientMessage = conn.recv(1024).decode("utf-8")
                print(f'{addr[0]} guessed "{clientMessage}"')
                winner = game.check_guess(clientMessage)
                strikes = game.get_strikes()

                if strikes == 6:
                    data['STATE'] = 'STRIKEOUT'
                    data['MESSAGE'] = (f'You struck out and lost the game. The word was "{game.get_word_to_guess()}"')
                    conn.send(json.dumps(data).encode("utf-8"))
                    gameOver = True

                if winner:
                    data['STATE'] = 'GAMEOVER'
                    data['MESSAGE'] = "You won the game!! The word was " + game.get_word_to_guess()
                    conn.send(json.dumps(data).encode("utf-8"))
                    gameOver = True

            except (InvalidInputHangmanError, ResponseLengthError) as e:
                data['STATE'] = 'ERROR'
                data['MESSAGE'] = str(e)
                conn.send(json.dumps(data).encode("utf-8"))
            except (ConnectionAbortedError, ConnectionResetError) as e:
                print(f"ERROR: {str(e)}: Connection to client " + addr[0] + " was lost.")
                break;


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
    except Exception as e:
        print("Lost connection to client" + addr[0])
        connections.remove(conn)

for connection in connections:
    connection.close()
s.close()
exit("Goodbye...")
