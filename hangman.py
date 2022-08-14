"""System Modules"""
import json
import random
from customException import InvalidInputHangmanError, ResponseLengthError


class Hangman:
    """Class to handle the Hangman game functionality.

    Public Methods:
        __init__: Initializes the game.
        __str__: Overloads the __str__ method to print the current state of the Hangman game.
        check_guess: Checks whether the user guess was correct.
        get_game_state: Gets the current state of letter holder.
        __check_for_winner: Checks whether the user has won the game.
        play: Sets up the game and begins the game loop.
        get_word_to_guess: Returns the word to be guessed.

    Private Methods:
        __get_words_and_word_count: gets a list of words and the number of
                                    words in the pool to guess from.
        __prepare_game: Sets up the letter_holder variable.
        __add_guess_to_list: Adds a guessed letter or word to the used letter or word list.
    """

    def __init__(self):
        self.__words = []
        self.__count = 0
        self.__letter_holder = []
        self.__strikes = 0
        self.__used_letters = []
        self.__used_words = []
        self.__word_to_guess = []

    def __str__(self):

        temp = ""

        for letter in self.__letter_holder:
            temp += letter + " "

        temp += "\n"

        return str("You have " + str(self.__strikes) + " strikes.\n" + str(temp))

    def __get_words_and_word_count(self) -> tuple[str,int]:
        """
        Gets the list of words and the number of words in the pool to guess from.
        """

        file = open("wordlist.json", "r", encoding="ascii")

        contents = json.load(file)
        words = contents["words"]
        count = len(words)

        file.close()

        return words, count

    def __prepare_game(self, word) -> str:
        """
        Takes in the word to guess and sets up the letter_holder variable based off it.

        Args:
            word (str): The word to guess.

        Returns:
            letter_holder (str): Variable with as many underscore's as there
                                 are letters in the word to guess.
        """

        letter_holder = list()

        for index,_ in enumerate(word):

            if word[index] == "-" or word[index] == "'":
                letter_holder.append(word[index])

            else:
                letter_holder.append("_")

        return letter_holder

    def check_guess(self, guess) -> bool:
        """
        Checks to see if the guess was first valid and then sees if the guess is correct.

        Args:
            guess (str): The guess to check.
        Returns:
            bool: True if the guess is correct, False otherwise.
        """

        length_of_guess = len(guess)
        length_of_word = len(self.__word_to_guess)
        guessed_correctly = False
        game_won = False

        if length_of_guess < 1:
            raise ResponseLengthError(
                "Guess must be at least one character in length." \
                   " Please try again."
            )

        for letter in range(length_of_guess):

            if ord(guess[letter].upper()) < 65 or ord(guess[letter].upper()) > 90:
                raise InvalidInputHangmanError(
                    "Invalid input. Must be a alphabetical character or word with no special" \
                        " characters. Please try again."
                )

        if length_of_guess == 1:
            if guess in self.__used_letters:
                print(f'Guess "{guess}" has already been used.')
                self.__strikes += 1
                return game_won

            for letter in range(length_of_word):
                if guess == self.__word_to_guess[letter]:
                    guessed_correctly = True
                    self.__letter_holder[letter] = guess

            if guessed_correctly:
                game_won = self.__check_for_winner(None,None,self.__letter_holder)
            else:
                self.__strikes += 1
            self.__add_guess_to_list(guess)

            return game_won

        if guess in self.__used_words:
            self.__strikes += 1
            print(f'Guess "{guess}" has already been used.')
            return game_won

        game_won = self.__check_for_winner(guess, self.__word_to_guess, None)

        if not game_won:
            self.__add_guess_to_list(guess)
            self.__strikes += 1
            return game_won

        return game_won

    def get_game_state(self) -> str:
        """
        Get the state of the game.

        Returns:
            str: The state of the game.
        """

        temp = ""

        for _ , letter in enumerate(self.__letter_holder):
            temp += letter + " "

        return self.__strikes, temp

    def __check_for_winner(self, guess=None, word=None, letter_holder=None) -> bool:
        """
        Checks if a given word matches the word to guess or if the letter_holder
        variable has no more under scores left.

        Args:
            guess (str): The guess to check.
            word (str): The word to check.
            letter_holder (str): If passed in, checks if there are any underscores left.
        Returns:
            bool: True if the word matches or if no underscores are left, False otherwise.
        """

        if not word:
            return False

        if not letter_holder:
            return False

        if not guess:

            winner = True

            if letter_holder is not None:

                for letter in letter_holder:
                    if letter == "_":
                        winner = False
                        return winner
                return winner

        elif guess == "".join(word):
            return winner

        else:
            winner = False
            return winner

    def play(self) -> None:
        """
        Sets up the game and begins playing.
        """

        self.__words, self.__count = self.__get_words_and_word_count()

        random.seed()

        self.__word_to_guess = list(self.__words[random.randint(0, self.__count)])

        self.__letter_holder = self.__prepare_game(self.__word_to_guess)

    def __add_guess_to_list(self, guess) -> None:
        """
        Adds a guessed word or letter to the list of used guesses.

        Args:
            guess (str): The guessed word or letter.
        """

        if len(guess) == 1:
            self.__used_letters.append(guess)
        else:
            self.__used_words.append(guess)

    def get_word_to_guess(self):
        """
        Returns the word that will be guessed.

        Returns:
            str: The word that will be guessed.
        """
        return self.__word_to_guess
