
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
