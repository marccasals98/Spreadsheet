from spreadsheet.Spreadsheet import Spreadsheet
from spreadsheet.Content import Formula

import re
from itertools import chain

class Tokenizer:
    '''
    Takes a string and splits it into tokens.

    Attributes:
    ------------
    tokens: list[tuple[str, int]]
        List of tuples with the token and its id.
        The id is the index of the token in the token_patterns list.
    
    Methods:
    --------
    get_tokens: list[str] -> list[tuple[str, int]]
        Takes a list of strings and splits them into tokens.
    tokenize: str -> list[tuple[str, int]]
        Takes a string and splits it into tokens. Returns the tokens.

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
        # TODO: Check parenthesis
        parenthesis_counter = 0
        for (token, id) in tokens:
            if id == 5:
                parenthesis_counter += 1
            elif id == 6:
                parenthesis_counter -= 1
        if parenthesis_counter != 0:
            raise ValueError("Parenthesis do not match")
        
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
    
    def generate_postfix_expression(self, tokens: list[tuple[str, int]]):
        '''
        Generates the postfix expression corresponding to formula as a sequence of formula components.
        Uses the Shunting-yard algorithm.

        Parameters:
        -----------
        tokens: list[tuple[str, int]]
            List of tuples with the token and its id.
            The id is the index of the token in the token_patterns list.
        '''
        # https://www.youtube.com/watch?v=HJOnJU77EUs

        stack = []
        output = []
        
        # Precedence of operators: determines the order of operations.
        precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '^': 3
        }

        for token, id in tokens:

            # The token is a number or a cell reference.
            if id in [3, 4]:
                output.append((token, id))
            
            # The token is an operator.
            elif id == 0:
                # compare the precedence of the token with that of the operator on the top of the stack.
                while stack and stack[-1][1] == 0 and precedence[stack[-1][0]] >= precedence[token]:
                    output.append(stack.pop())
                # push the operator onto the stack.
                stack.append((token, id))                    
            
            # The token is a function.
            elif id == 1:
                stack.append((token, id))

            # The token is a left parenthesis.
            elif id == 5:
                stack.append((token, id))
            
            # The token is a right parenthesis.
            elif id == 6:
                while stack and stack[-1][1] != 5:
                    output.append(stack.pop())
                if stack and stack[-1][1] == 5:
                    stack.pop() # Remove the left parenthesis.
                else:
                    raise ValueError("Parenthesis do not match")
            
        # Empty the stack.
        while stack:
            if stack[-1][1] == 5 or stack[-1][1] == 6:
                raise ValueError("Parenthesis do not match")
            output.append(stack.pop())
        
        return output
                    
    def evaluate_operation(self, a, b, operator):
        if operator == "+":
            return a + b
        elif operator == "-":
            return a - b
        elif operator == "*":
            return a * b
        elif operator == "/":
            return a / b
        elif operator == "^":
            return a ** b
        else:
            raise ValueError("Bad operator")
        
    def evaluate_postfix_expression(self, tokens):
        stack = []
        for token, id in tokens:
            if id == 3:
                stack.append((token, id))
            if id == 0:
                if len(stack) < 2:
                    raise ValueError("Bad expression")
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append((self.evaluate_operation(a, b, token), 3))
            return stack[0][0]     
        
        
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
