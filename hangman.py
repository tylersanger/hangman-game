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
    
    def __str__(self):

        temp = ""

        for letter in self.__letterHolder:
            temp += letter + " "
        
        return temp


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

            if ord(guess[letter].upper()) < ord('A') or ord(guess[letter].upper()) > ord('Z'):
                raise InvalidInputHangmanError("Invalid input. Must be a character or word with no special characters. Please try again.")
                        
        if lengthOfGuess == 1:

            if guess in self.__usedLetters:
                print(f"Guess \"{guess}\" has already been used.")
                self.__strikes += 1
                return gameWon

            for letter in range(0,lengthOfWord):

                if guess == self.__wordToGuess[letter]:
                    guessedCorrectly = True
                    self.__letterHolder[letter] = guess
            
            if not guessedCorrectly:
                self.__strikes += 1
                self.__add_guess_to_list(guess)
                return gameWon

            self.__add_guess_to_list(guess)

            return self.check_for_winner(guess,self.__wordToGuess,self.__letterHolder)

        elif guess in self.__usedWords:
            self.__strikes += 1
            print(f"Guess \"{guess}\" has already been used.")
            return gameWon
        
        else:
            gameWon = self.check_for_winner(guess,self.__wordToGuess,None)

            if gameWon:
                return gameWon

            else:
                self.__add_guess_to_list(guess)
                self.__strikes += 1
                return gameWon


    def get_game_state(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        state = (f"You have {self.__strikes} strikes.\nWord To Guess: {self.__str__()}\n"
                    + f"Used Letters: {self.__usedLetters}\nUsed Words: {self.__usedWords}")
        return state


    def check_for_winner(self,guess = None,word = None,letterHolder = None):

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
        
        text = ""
        for letter in self.__wordToGuess:
            text += letter

        return text
    
    def get_strikes(self):
        return self.__strikes
    
    if __name__ == "__main__":
        os.system("python main.py")