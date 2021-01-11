class InvalidInputHangmanError(Exception):

    '''
        This class creates a custom exception InvalidInputHangmanError which is thrown when the player doesn't supply a valid
        letter or word to guess
    '''

    def __init__(self,message):

        self.__message = message
    
    def __str__(self):
        return self.__message


class ResponseLengthError(Exception):

    '''
        This class creates a custom exception ResponseLengthError which is thrown when the player doesn't supply a valid
        guess length
    '''

    def __init__(self,message):

        self.__message = message

    def __str__(self):
        return self.__message