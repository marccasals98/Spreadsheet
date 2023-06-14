from spreadsheet.FormulaEvaluator import Tokenizer, PostfixExpressionManager
from spreadsheet.Spreadsheet import Spreadsheet, Coordinates
from spreadsheet.Content import Numerical

def test_tokenizer():
    expr = "MAX(A3:B3)+4*C5"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    expected = ['MAX', '(', 'A3:B3', ')', '+', '4', '*', 'C5']
    assert expected == [token for token, _ in tokens]
    
    
def test_parser_1():
    expr = "MAX(A3:B3)+4*C5"
    # Correcte!
    
def test_parser_1():
    expr = "MAX)A3:B3)+4*C5"
    # Incorrecte!


def test_postfix_creation_1():
    spreadsheet = Spreadsheet('test', 10, 10)
    tokens = (('1', 4), ('+', 0), ('2', 4))
    mngr = PostfixExpressionManager()
    expression = mngr.generate_postfix_expression(tokens, spreadsheet)
    assert expression == [1, 2, '+']
    

def test_postfix_creation_2():
    spreadsheet = Spreadsheet('test', 10, 10)
    tokens = (('1', 4), ('+', 0), ('2', 4), ('*', 0), ('3', 4))
    mngr = PostfixExpressionManager()
    expression = mngr.generate_postfix_expression(tokens, spreadsheet)
    assert expression == [1, 2, 3, '*', '+']
    

def test_postfix_creation_3():
    spreadsheet = Spreadsheet('test', 10, 10)
    tokens = (('(', 5), ('1', 4), ('+', 0), ('2', 4), (')', 6), ('*', 0), ('3', 4))
    mngr = PostfixExpressionManager()
    expression = mngr.generate_postfix_expression(tokens, spreadsheet)
    assert expression == [1, 2, '+', 3, '*']
    
    
def test_postfix_creation_4():
    spreadsheet = Spreadsheet('test', 10, 10)
    spreadsheet.cells[Coordinates.from_text('A1')].set_content(Numerical(1))
    # (A1 + 2) * 3
    tokens = (('(', 5), ('A1', 3), ('+', 0), ('2', 4), (')', 6), ('*', 0), ('3', 4))
    mngr = PostfixExpressionManager()
    expression = mngr.generate_postfix_expression(tokens, spreadsheet)
    assert expression == [1, 2, '+', 3, '*']
    

# def test_postfix_creation_5():
#     spreadsheet = Spreadsheet('test', 10, 10)
#     spreadsheet.cells[Coordinates.from_text('A1')].set_content(Numerical(1))
#     # SUMA(A1:A3) + 3
#     tokens = (('(', 5), ('A1', 3), ('+', 0), ('2', 4), (')', 6), ('*', 0), ('3', 4))
#     mngr = PostfixExpressionManager()
#     expression = mngr.generate_postfix_expression(tokens, spreadsheet)
#     assert expression == [1, 2, '+', 3, '*']


def test_postfix_evaluation_1():
    expression = [1, 2, 3, '*', '+']
    mngr = PostfixExpressionManager()
    value = mngr.evaluate_postfix_expression(expression)
    assert value == 7
    
def test_postfix_evaluation_2():
    expression = [1, 2, '+', 3, '*']
    mngr = PostfixExpressionManager()
    value = mngr.evaluate_postfix_expression(expression)
    assert value == 9