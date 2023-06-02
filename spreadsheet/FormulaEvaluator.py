from spreadsheet.Spreadsheet import Spreadsheet
from spreadsheet.Content import Formula

import re
from itertools import chain

class Tokenizer:
    '''
    Takes a string and splits it into tokens.

    Attributes:
    ------------
    tokens: list[str]
        list of tokens

    ''' 
        
    token_patterns = [
        r"^(\+|-|\*|\/|\^)",                         # 0
        r"^(SUM|MIN|MAX|AVG)",                       # 1
        r"^([A-Z]+[1-9][0-9]*):([A-Z]+[1-9][0-9]*)", # 2
        r"^([A-Z]+[1-9][0-9]*)",                     # 3
        r"^([0-9])+",                                # 4
        r"^\(",                                      # 5
        r"^\)",                                      # 6
    ]

    def __init__(self):
        self.tokens = []

    def get_tokens(self, list_of_strings):
        '''
        Takes a list of strings and splits them into tokens.
        '''
        for string in list_of_strings:
            self.tokens.append(string.split(' '))
        return self.tokens
    
    def tokenize(self, repr: str):
        repr = repr.replace(" ", "")
        while repr != "":
            matched = False
            for token_id, pattern in enumerate(self.token_patterns):
                regex_match = re.match(pattern, repr)
                if regex_match:
                    matched = True
                    tok = regex_match.group()
                    self.tokens.append((tok, token_id))
                    repr = repr.replace(tok, "", 1)
                    break
            if not matched:
                raise Exception("Bad expression")
        return self.tokens
                    
                    
                    
                    
                    
                
        

class Parser:
    # Normes:
    #  - 0 => 1, 3, 4, 5
    #  - 1 => 5
    #  - 2 => 6
    #  - 3 => 0
    #  - 5 => (1, 2)
    #  - ...
    #  - Per cada 5 hi ha un 6 despres
    #  - L'expressio ha de comencar amb: 1, 3, 4, 5
    #  - L'expressio ha d'acabar amb: 3, 4, 6

    # Rules that determine possible posterior tokens
    posterior_rules = {
        0: [1, 3, 4, 5],  # After 0, only 1, 3, 4 or 5
        1: [5],
        2: [6],
        # ...
    }
    
    # starting/ending rules
    start_rule = [1, 3, 4, 5]
    end_rule = [3, 4, 6]
    
    def __init__(self):
        ...
    
    def parse(self, tokens: list[tuple[str, int]]) -> list[tuple[str, int]]:
        # Check posterior rules
        for (token1, id1), (token2, id2) in chain(tokens):
            if id2 not in self.posterior_rules[id1]:
                raise ValueError(f"{token2} can not be after {token1}")
        
        # Check start/end rule
        if tokens[0][1] not in self.start_rule:
            raise ValueError(f"First token can not be: {tokens[0][1]}")
        if tokens[-1][1] not in self.end_rule:
            raise ValueError(f"Last token can not be: {tokens[-1][1]}")
        
        # Check parenthesis:
        # TODO
        
        return tokens
            


class PostfixExpressionManager():
    '''
    Evaluate the formula introduced by the user.

    Methods:
    ------------
    generate_postfix_expression: list[str]
        Returns the postfix expression.
    evaluate_postfix_expression: list[str] -> NumericalValue
        Returns the result of the postfix expression.
    '''

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    
    def generate_postfix_expression(self, list_of_strings):
        ...
    
    def evaluate_postfix_expression(self, list_of_strings):
        ...
        
        
class FormulaEvaluator:
    ...
    def __init__(self, formula: Formula, spreadhseet: Spreadsheet):
        self.formula = formula
        self.spreadsheet = spreadhseet
        
    def evaluate(self):
        representation = self.formula.get_representation()
        
        # Get tokens
        tokenizer = Tokenizer()
        tokens = tokenizer.get_tokens(representation)
        
        # Parse tokens
        parser = Parser()
        tokens = parser.parse_tokens(tokens)
        
        # Generate Postfix Expression
        postfix = PostfixExpressionManager()
        postfix_expression = postfix.generate_postfix_expression(tokens)
        value = self.evaluate_postfix_expression(postfix_expression)
        
        self.formula.set_value(value)
        
    def evaluate_postfix_expression(self):
        ...
