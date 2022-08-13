import socket
import os
import json

IP = '192.168.1.9'
port = 55987
jData = ''
last_stats = ""

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

s.send("READY".encode("utf-8"))

while True:

    try:

        jData = s.recv(1024).decode("utf-8")

        message = json.loads(jData)

        if message['STATE'] == 'STATS':
            print(f"{message['MESSAGE']}")
            last_stats = message['MESSAGE']
        if message['STATE'] == 'ERROR':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"ERROR: {message['MESSAGE']}")
            print(last_stats)
            s.send(input("Enter your guess: ").encode("utf-8"))
        if message['STATE'] == 'STRIKEOUT':
            print(message['MESSAGE'])
            break
        if message['STATE'] == 'GAMEOVER':
            print(message['MESSAGE'])
            break

        s.send(input("What is your guess: ").encode("utf-8"))
    except (KeyboardInterrupt) as e:
        print(f"\nClosing client connection due to CTRL+C command.")
        s.close()
        exit("Client connection closed...")
    except Exception as e:
        print("Lost connection to the server.")
        exit("Program exiting...")

s.close()


    




