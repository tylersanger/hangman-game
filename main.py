'''
Created by Tyler Sanger
Copyright: 01/04/2021
This software is licensed under the MIT license.

This program plays a game of Hangman. It will choose a randomly chosen word from 3000 words and have the player guess until they have either
guessed the entire word or reached the six strike
'''

from hangman import Hangman
from customException import InvalidInputHangmanError,ResponseLengthError
from hangman import Hangman
import os
import time

os.system('cls' if os.name == 'nt' else 'clear')
response = list("YyNn")
letterHolder = []
strikes = 0
validRes = False
gameOver = False
gameLost = False
correctGuess = False
h1 = Hangman()

print("----------------------------HANGMAN INTRODUCTION-------------------------------")
print("- 1. This game will choose a random word out of 3000 for you to guess from.   -")
print("- 2. You have 6 wrong guesses available. One for each body part you can       -")
print("-    accumilate (head, torso, 2 arms, 2 legs) in the actual game.             -")
print("- 3. The name of the game is simple, guess the word and dont strike out!      -")
print("- 4. Guesses must be at least 1 character. You can try to guess the entire    -")
print("- 5. Guesses of length > 1 are counted as a word guess.                       -")
print("-    word if you would like. Only a-z or A-Z is accepted. No special chars.   -")
print("- 6. Both incorrect characters and word guesses are counted as 1 strike.      -")
print("- 7. Already guessed letters or words are also counted as a strike.           -")
print("-                                                                             -")
print("-                              GOOD LUCK!                                     -")
print("-------------------------------------------------------------------------------")

while not validRes:
    
    try:
        res = input("Are you ready to play? (y/n): ")

        if len(res) > 1:
            raise ResponseLengthError(f"Expected response length of 1. Received response \"{res}\" of length {len(res)}")

        if res not in response:
            raise InvalidInputHangmanError(f"Expected input of y/n or Y/N. Received \"{res}\"")

    except ResponseLengthError as e:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(e)

    except InvalidInputHangmanError as e:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(e)

    else:
        validRes = True

os.system('cls' if os.name == 'nt' else 'clear')

if res.upper() == 'Y':
    game = Hangman()
    game.play()
    winner = False
    strikes = 0

    while not winner:

        try:
            print(game.get_game_state())
            winner = game.check_guess(input("Guess a letter or an entire word: "))
            strikes = game.get_strikes()

        except Exception as e:
            print(e)
            time.sleep(3)

        if strikes == 6:
            print(game.get_game_state())
            print(f"You struck out. The word to guess was \"{game.get_word_to_guess()}\".")
            break;

    if winner:
        print("YOU WON!!")
    
else:
    print("You chose to not play. See you next time!")
    exit(0)