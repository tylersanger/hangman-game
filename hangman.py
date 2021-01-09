import json
import random
from customException import InvalidInputHangmanError, ResponseLengthError
import os

def get_words_and_wordCount():

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


def prepare_game(word):

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


def check_guess(letterHolder,word,userGuess,usedWords,usedLetters):
    ''' This function will check wheter the players guess is a valid guess or not. A valid guess is a character of length 1 from A-Z or a-z only or a word with no special characters
        included. A guess with a length greater than 1 is counted as a word guess. If a letter or word has already been guessed then the player will be informed.

        Input:
            letterHolder: The list that represents the randomly chosen word the player is guessing. This holds how many letters long the word is and shows the correctly guessed letters.
            word: The randomly chosen word the player is guessing.
            userGuess: The player's letter or word guess.
            usedWords: A list holding all the guessed words the player has used.
            usedLetters: A list holding all the guessed letters the player has used.
        Output:
            gameWon: Returns True if the user has won the game or False if they haven't.
            guessedcorrectly: Returns True if the user guessed a letter or the word correctly or False if they haven't.
            letterHolder: Returns the updated letter holder after the game checks to see if the player guessed a letter
                          correctly and updates the list to show it.
            word: Returns the word the user was trying to guess if they guessed the word correctly
    '''

    
    lengthOfGuess = len(userGuess)
    lengthOfWord = len(word)
    guessedCorrectly = False
    gameWon = False

    if lengthOfGuess < 1:
        raise ResponseLengthError("Guess must be at least one character in length. Please try again.")
    
    for letter in range(0,lengthOfGuess):

        if ord(userGuess[letter].upper()) < 65 or ord(userGuess[letter].upper()) > 90:
            raise InvalidInputHangmanError("Invalid input. Must be a character or word with no special characters. Please try again.")
                    
    if lengthOfGuess == 1:

        if userGuess in usedLetters:
            print(f"Guess \"{userGuess}\" has already been used.")
            return gameWon,guessedCorrectly,letterHolder

        for letter in range(0,lengthOfWord):

            if userGuess == word[letter]:
                guessedCorrectly = True
                letterHolder[letter] = userGuess

        return gameWon,guessedCorrectly,letterHolder

    elif userGuess in usedWords:
        print(f"Guess \"{userGuess}\" has already been used.")
        return gameWon,guessedCorrectly,letterHolder
    
    else:
        gameWon = check_for_winner(userGuess,word)

        if gameWon:
            guessedCorrectly = True
            return gameWon,guessedCorrectly,word

        else:
            return gameWon,guessedCorrectly,letterHolder


def print_game_state(numberOfGuesses,letterHolder):
    '''
        This function prints the current state of how many strikes the player has and the current state of the letterHolder list.

        Input:
            numberOfGuesses: How many strikes the player currently has.
            letterHolder: List containing the guessed and missing letters.
    '''

    temp = ""

    print(f"\nNumber of guesses: {numberOfGuesses}")

    for letter in range(0,len(letterHolder)):
        temp += str(letterHolder[letter] + " ")
    
    print(temp)


def check_for_winner(guess = None,word = None,letterHolder = None):
    
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


def play():

    '''
        This function is what defines a game of hangman. It will get the list of available words to guess, the number of words there are in the list and pick a random word from the list.
        The player will be ased to guess a letter or an entire word and will keep guessing until they reach six strikes or guess all the letters or the entire word.

    The game is considered over and the player loses if they reach 6 wrong letter or word guesses. The game will then tell them what the word was.

    The game is considered over and won if they guess all the letters without reaching six strikes or they guess the word correctly.

    The user will get a strike for a incorrect letter, incorrect word, already guessed letter and already guessed word.

    The total number of strikes equalling six comes from each body part that can be accumulated (head,torso,both arms,both legs).
    '''

    usedLetters = list()
    usedWords = list()
    numberOfGuesses = 0
    gameOver = False
    gameLost = False

    words,count = get_words_and_wordCount()

    random.seed()

    wordToGuess = list(words[random.randint(0,count)])

    letterHolder = prepare_game(wordToGuess)

    while not gameOver:

        correctGuess = False

        print_game_state(numberOfGuesses,letterHolder)

        try:
            userGuess = input("Enter a letter or guess the entire word: ")
            gameOver,correctGuess,letterHolder = check_guess(letterHolder,wordToGuess,userGuess,usedWords,usedLetters)

        except InvalidInputHangmanError as e:
            print(e)

        except ResponseLengthError as e:
            print(e)

        else:
            if not correctGuess:
                numberOfGuesses += 1

            if numberOfGuesses == 6:
                gameOver = True
                gameLost = True

            if check_for_winner(None,None,letterHolder):
                gameOver = True

            if len(userGuess) == 1:
                usedLetters.append(userGuess)

            else:
                usedWords.append(userGuess)

    if gameLost:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"You ran out of guesses! The word was \"{''.join(wordToGuess)}\"")
        
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"YOU WON!!! The correct word was \"{''.join(wordToGuess)}\" and you had {numberOfGuesses} strikes!")