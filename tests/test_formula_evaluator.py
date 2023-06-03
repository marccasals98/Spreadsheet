from spreadsheet.FormulaEvaluator import Tokenizer

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
    
