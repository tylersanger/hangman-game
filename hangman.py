import json
import random
from customException import InvalidInputHangmanError, ResponseLengthError
import os


class Hangman:

    def __init__(self):
        self.__words = []
        self.__count = 0
        self.__letterHolder = []
        self.__strikes = 0
        self.__usedLetters = []
        self.__usedWords = []
        self.__wordToGuess = []


    def __get_words_and_wordCount(self):

        ''' Returns a list of words and the number of words in the list.

        Returns:
        words: List of words to choose from
        count: Number of words in the list '''

        f = open("wordlist.json","r")

        contents = json.load(f)
        words = contents['words']
        count = len(words)

        f.close()

        return words,count


    def __prepare_game(self,word):

        '''This function will take the randomly chosen word and create a list to hold each letter of that word.
        This will automatically display any special characters in the random word such as ' or -. The rest of
        the letters are represented as a underscore (_).

        Input: 
        word: The randomly chosen word the player will be guessing as a list of characters.

        Output:
        letterHolder: The list that will be updated when the player guesses a correct letter.
        '''

        letterHolder = list()

        for letter in range(0,len(word)):

            if word[letter] == '-' or word[letter] == '\'':
                letterHolder.append(word[letter])

            else:
                letterHolder.append("_")
        
        return letterHolder


    def check_guess(self,guess):

        lengthOfGuess = len(guess)
        lengthOfWord = len(self.__wordToGuess)
        guessedCorrectly = False
        gameWon = False

        if lengthOfGuess < 1:
            raise ResponseLengthError("Guess must be at least one character in length. Please try again.")
        
        for letter in range(0,lengthOfGuess):

            if ord(guess[letter].upper()) < 65 or ord(guess[letter].upper()) > 90:
                raise InvalidInputHangmanError("Invalid input. Must be a character or word with no special characters. Please try again.")
                        
        if lengthOfGuess == 1:

            if guess in self.__usedLetters:
                print(f"Guess \"{guess}\" has already been used.")
                self.__strikes += 1
                return gameWon,self.__letterHolder

            for letter in range(0,lengthOfWord):

                if guess == self.__wordToGuess[letter]:
                    guessedCorrectly = True
                    self.__letterHolder[letter] = guess
            
            if not guessedCorrectly:
                self.__strikes += 1

            self.__add_guess_to_list(guess)

            return gameWon,self.__letterHolder

        elif guess in self.__usedWords:
            self.__strikes += 1
            print(f"Guess \"{guess}\" has already been used.")
            return gameWon,self.__letterHolder
        
        else:
            gameWon = self.check_for_winner(guess,self.__wordToGuess,None)

            if gameWon:
                guessedCorrectly = True
                return gameWon,guessedCorrectly,self.__wordToGuess

            else:
                self.__add_guess_to_list(guess)
                self.__strikes += 1
                return gameWon,guessedCorrectly,self.__letterHolder


    def get_game_state(self):
        '''
            This function prints the current state of how many strikes the player has and the current state of the letterHolder list.

            Input:
                numberOfGuesses: How many strikes the player currently has.
                letterHolder: List containing the guessed and missing letters.
        '''

        temp = ""

        print(f"\nNumber of strikes: {self.__strikes}")

        for letter in range(0,len(self.__letterHolder)):
            temp += str(self.__letterHolder[letter] + " ")
        
        return self.__strikes,temp


    def check_for_winner(self,guess = None,word = None,letterHolder = None):
        
        '''
            This function checks to see if the player has won the game. If there are no more underscores (_) left in the letterHolder list
            or the user guessed the word correctly they have won.

            Input:
                guess: The players guessed letter or word.
                word: The word the player is trying to guess.
                letterHolder: The list containing guessed letters or underscores (_) for un-guessed letters.
            Return:
                winner: Returns True if there are no underscores (_) left in letterHolder or if the word was guessed correctly.
        '''

        winner = True

        if letterHolder is not None:

            for letter in letterHolder:
                if letter == "_":
                    winner = False
                    return winner
            return winner

        elif guess == ''.join(word):
            return winner

        else:
            winner = False
            return winner


    def play(self):

        self.__words,self.__count = self.__get_words_and_wordCount()

        random.seed()

        self.__wordToGuess = list(self.__words[random.randint(0,self.__count)])

        self.__letterHolder = self.__prepare_game(self.__wordToGuess)
    
    def __add_guess_to_list(self,guess):

        if len(guess) == 1:
            self.__usedLetters.append(guess)
        else:
            self.__usedWords.append(guess)
    
    def get_word_to_guess(self):
        return self.__wordToGuess
    
    def print_game_state(self):

        temp = ''

        for letter in self.__letterHolder:
            temp += letter + " "
        
        print(f"You have {self.__strikes} strikes.")
        print(temp)
    

