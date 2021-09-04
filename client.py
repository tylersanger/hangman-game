import socket
import os

IP = "192.168.1.7"
port = 55987

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, port))


def game_menu():

    print(
        "----------------------------HANGMAN INTRODUCTION-------------------------------"
    )
    print(
        "- 1. This game will choose a random word out of 3000 for you to guess from.   -"
    )
    print(
        "- 2. You have 6 wrong guesses available. One for each body part you can       -"
    )
    print(
        "-    accumilate (head, torso, 2 arms, 2 legs) in the actual game.             -"
    )
    print(
        "- 3. The name of the game is simple, guess the word and dont strike out!      -"
    )
    print(
        "- 4. Guesses must be at least 1 character. You can try to guess the entire    -"
    )
    print(
        "- 5. Guesses of length > 1 are counted as a word guess.                       -"
    )
    print(
        "-    word if you would like. Only a-z or A-Z is accepted. No special chars.   -"
    )
    print(
        "- 6. Both incorrect characters and word guesses are counted as 1 strike.      -"
    )
    print(
        "- 7. Already guessed letters or words are also counted as a strike.           -"
    )
    print(
        "-                                                                             -"
    )
    print(
        "-                              GOOD LUCK!                                     -"
    )
    print(
        "-------------------------------------------------------------------------------"
    )


game_menu()

s.send("READY".encode("ascii"))

while True:
    msg = s.recv(1024).decode("ascii")

    if msg[0:8] != "GAMEOVER":
        print(msg)
        msg = input("What is your guess: ")
        s.send(msg.encode("ascii"))
        os.system("cls" if os.name == "nt" else "clear")
    else:
        print(msg[8:])
        break
