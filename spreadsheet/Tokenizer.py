from abc import ABC, abstractmethod

'''
IS THIS REALLY AN ABSTRACT CLASS??
'''

class Tokenizer(ABC):
    '''
    Takes a string and splits it into tokens.

    Attributes:
    ------------
    tokens: list[str]
        list of tokens

    '''

    def __init__(self):
        self.tokens = []

    def get_tokens(self, list_of_strings):
        '''
        Takes a list of strings and splits them into tokens.
        '''
        for string in list_of_strings:
            self.tokens.append(string.split(' '))
        return self.tokens
    
    def tokenize (repr: str):
        ...
