from spreadsheet.Spreadsheet import Spreadsheet, Coordinates
from spreadsheet.Content import Formula

import re
from itertools import pairwise

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
        r"^(SUMA|MIN|MAX|PROMEDIO)",                 # 1
        r"^([A-Z]+[1-9][0-9]*)\:([A-Z]+[1-9][0-9]*)", # 2
        r"^([A-Z]+[1-9][0-9]*)",                     # 3
        r"^([0-9])+",                                # 4
        r"^\(",                                      # 5
        r"^\)",                                      # 6
        r"^;",                                       # 7
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
        # TODO: Document
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
    """TODO: Document"""
    # Normes:
    #  - 0 => 1, 3, 4, 5
    #  - 1 => 5
    #  - 2 => 6
    #  - 3 => 0
    #  - 5 => (1, 2)
    #  - 6 => ()
    #  - Per cada 5 hi ha un 6 despres
    #  - L'expressio ha de comencar amb: 1, 3, 4, 5
    #  - L'expressio ha d'acabar amb: 3, 4, 6

    # Rules that determine possible posterior tokens
    posterior_rules = {
        0: [1, 3, 4, 5],  # After 0, only 1, 3, 4 or 5
        1: [5],
        2: [6, 7],
        3: [0, 3, 6, 7],
        4: [0, 6, 7],
        5: [1, 2, 3, 4],
        6: [0, 6, 7],
        7: [1, 2, 3, 4]
    }
    
    # starting/ending rules
    start_rule = [1, 3, 4, 5]
    end_rule = [3, 4, 6]
    
    function_operator = {
        'SUMA': '+',
        'MIN': 'm',
        'MAX': 'M',
        'PROMEDIO': '+'
    }

    def parse(self, tokens: list[tuple[str, int]]) -> list[tuple[str, int]]:
        """TODO: Document"""
        # Check posterior rules
        for (token1, id1), (token2, id2) in pairwise(tokens):
            if id2 not in self.posterior_rules[id1]:
                raise ValueError(f"{token2} can not be after {token1}")
        
        # Check start/end rule
        if tokens[0][1] not in self.start_rule:
            raise ValueError(f"First token can not be: {tokens[0][1]}")
        if tokens[-1][1] not in self.end_rule:
            raise ValueError(f"Last token can not be: {tokens[-1][1]}")
        
        # Check parenthesis:
        parenthesis_counter = 0
        for _, id in tokens:
            if id == 5:
                parenthesis_counter += 1
            elif id == 6:
                parenthesis_counter -= 1
        if parenthesis_counter != 0:
            raise ValueError("Parenthesis do not match")
        
        return tokens


    def resolve_ranges(self, tokens: list[tuple[str, int]], spreadsheet: Spreadsheet) -> list[tuple[str, int]]:
        """Transform the ranges into list of cells.""" # TODO: Document properly
        print("Resolving ranges...")
        tokens = tokens.copy()
        for token, token_id in tokens:
            if token_id != 2:  # Not a range, skip
                yield (token, token_id)
            else:
                
                ul, lr = Coordinates.range_from_text(token)
                coords = spreadsheet.get_range(ul, lr)
                yield from ((str(coord), 3) for coord in coords)
                
    
    @staticmethod
    def _advance_until_closed_parenthesis(tokens: list, start_idx: int):
        """TODO: Write"""
        num_open_parenthesis = 1
        while num_open_parenthesis:
            _, token_id = tokens[start_idx]
            if token_id == 5:
                num_open_parenthesis += 1
            elif token_id == 6:
                num_open_parenthesis -= 1
            start_idx += 1
        return start_idx
    
    
    def function2operator(self, function: str, tokens: list[tuple[str, int]], idx: int) -> list[tuple[str, int]]:
        """TODO: Write
        
        Note: recursive."""
        operator = self.function_operator[function]
        num_operands = 0
        
        # Start by yielding the open parenthesis token
        yield ("(", 5)
        
        # In the case of average, we add and extra parenthesis
        if function == 'PROMEDIO':
            yield ("(", 5)
        
        # Traverse all tokens until you find a ")"
        while idx < len(tokens):
        # for idx, (token, token_id) in enumerate(tokens):
            token, token_id = tokens[idx]
            if token_id == 6:         # close parenthesis
                break
            elif token_id == 1:       # another function
                yield from self.function2operator(token, tokens, idx+2)
                idx = self._advance_until_closed_parenthesis(tokens, idx+2)
                num_operands += 1
            elif token_id in (3, 4):  # cell or value
                yield (token, token_id)
                num_operands += 1
                idx += 1
            else:
                idx += 1
                continue
            
            if tokens[idx][1] != 6:
                yield (operator, 0)
            
        # In the case of average, divide by number of operands
        if function == 'PROMEDIO':
            yield from ((")", 6), ("/", 0), (f"{num_operands}", 4))  
        
        # Close the initial parenthesis
        yield(")", 6)
            
    
    def transform_functions_to_operators(self, tokens: list[tuple[str, int]]) -> list[tuple[str, int]]:
        """ Given a list of tokens substitute functions with operators
        
        Parameters
        ----------
        tokens: list[tuple[str, int]]
            List of tokens (Assumption: no ranges)
        idx: int
            index of the first character
        """
        idx = 0
        while idx < len(tokens):
            token, token_id = tokens[idx]
        # for idx, (token, token_id) in enumerate(tokens):
            if token_id != 1: # Not a function, skip
                yield (token, token_id)
                idx += 1
                continue
            
            # Yield the transformed set of tokens
            idx += 2
            yield from self.function2operator(token, tokens, idx)
            
            # Advance until the outer function is finished
            idx = self._advance_until_closed_parenthesis(tokens, idx)
            
        
    
    # def transform_functions_to_operators(self, tokens: list[tuple[str, int]], spreadsheet: Spreadsheet) -> list[tuple[str, int]]:
    #     """ Given a list of tokens:
    #         - Substitute functions with operators
    #         - Substitute ranges with actual cell coordinates inside
    #     """
    #     i = 0
    #     while i < len(tokens):
    #         token, id = tokens[i]
    #         if id != 1:
    #             i += 1
    #             continue
    #         assert tokens[i+1][0] == '('
    #         j = i + 2
    #         operands = []
    #         # TODO: Add functions inside functions
    #         while j < len(tokens) and tokens[j][0] != ')':
    #             if tokens[j] == ';':
    #                 j += 1
    #                 continue
    #             f_token, f_id = tokens[j]
    #             if f_id == 2: # range
    #                 ul, lr = Coordinates.range_from_text(f_token)
    #                 coords = spreadsheet.get_range(ul, lr)
    #                 operands.extend([(str(coord), 3) for coord in coords])
    #             if f_id in (3, 4):
    #                 operands.append((f_token, f_id))
                
    #             j += 1
    #         j += 1
    #         new_tokens = list(self.tf_function(token, operands))
    #         tokens = tokens[:i] + new_tokens + tokens[j:]
    #         i = j
    #     return tokens
            


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

    # def __init__(self, tokenizer):
    #     self.tokenizer = tokenizer
    
    def generate_postfix_expression(self, tokens: list[tuple[str, int]], spreadsheet: Spreadsheet):
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
            '^': 3,
            'M': 3,  # Max
            'm': 3   # Min
        }

        for token, id in tokens:
            # The token is a number
            if id == 4:
                output.append(float(token))
            
            # The token is a cell reference.
            if id == 3:
                coords = Coordinates.from_text(token)
                if coords not in spreadsheet.cells:
                    spreadsheet.expand(coords.col, coords.row)
                value = spreadsheet.cells[coords].get_value()
                output.append(value)
            
            # The token is an operator.
            elif id == 0:
                # compare the precedence of the token with that of the operator on the top of the stack.
                while stack and stack[-1] in precedence.keys() and precedence[stack[-1]] >= precedence[token]:
                    operator = stack.pop()
                    output.append(operator)
                # push the operator onto the stack.
                stack.append(token)                    
            
            # The token is a function.
            # elif id == 1:
            #     # compare the precedence of the token with that of the operator on the top of the stack.
            #     while stack and stack[-1] == 0 and precedence[stack[-1]] >= precedence[token]:
            #         formula, _ = stack.pop()
            #         output.append(formula)
            #     # push the formula onto the stack.
            #     stack.append(token)   

            # The token is a left parenthesis.
            elif id == 5:
                stack.append(token)
            
            # The token is a right parenthesis.
            elif id == 6:
                while stack and stack[-1] != '(':
                    output.append(stack.pop()[0])
                if stack and stack[-1] == '(':
                    stack.pop() # Remove the left parenthesis.
                else:
                    raise ValueError("Parenthesis do not match")
            
        # Empty the stack.
        while stack:
            if stack[-1] == 5 or stack[-1] == 6:
                raise ValueError("Parenthesis do not match")
            output.append(stack.pop())
        
        return output
                    
    def evaluate_operation(self, a, b, operator):
        """TODO: Document"""
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
        elif operator == "m":  # min
            return min(a, b)
        elif operator == "M":  # max
            return max(a, b)
        else:
            raise ValueError(f"Bad operator ({operator})")
        
    def evaluate_postfix_expression(self, tokens):
        """TODO: Document"""
        stack = []
        for token in tokens:
            if isinstance(token, (float, int)):
                stack.append(token)
            else:
                if len(stack) < 2:
                    raise ValueError("Bad expression")
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(self.evaluate_operation(a, b, token))
        
        if len(stack) != 1:
            raise ValueError("Bad expression")
        return stack.pop()     
        
        
class FormulaEvaluator:
    """TODO: Document"""
    
    def __init__(self, formula: Formula, spreadhseet: Spreadsheet):
        self.formula = formula
        self.spreadsheet = spreadhseet
        self.tokens = None
        
    def get_tokens(self):
        """TODO: Document"""
        # Obtain tokens from representation
        representation = self.formula.get_representation()
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(representation)
        
        # Parse tokens
        parser = Parser()
        self.tokens = parser.parse(tokens)
        self.tokens = list(parser.resolve_ranges(self.tokens, self.spreadsheet))
        self.tokens = list(parser.transform_functions_to_operators(self.tokens))
        
        return self.tokens
        
    def evaluate(self):
        """TODO: Document"""
        # Get tokens
        tokens = self.tokens if self.tokens else self.get_tokens()
        
        # Generate Postfix Expression
        postfix = PostfixExpressionManager()
        postfix_expression = postfix.generate_postfix_expression(tokens, self.spreadsheet)
        value = postfix.evaluate_postfix_expression(postfix_expression)
        
        # Cast value to integer if possible
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        
        self.formula.set_value(value)
        
    def update_dependencies(self):
        """TODO: Document"""
        # Get tokens
        tokens = self.tokens if self.tokens else self.get_tokens()
        cell_tokens = filter(lambda token: token[1] == 3, tokens)
        self.formula.set_dependencies([Coordinates.from_text(cell) for cell, _ in cell_tokens])
