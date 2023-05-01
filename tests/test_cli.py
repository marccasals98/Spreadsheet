from spreadsheet.Spreadsheet import Spreadsheet, Coordinates, Cell, Numerical
from spreadsheet.CLI import CLI

def test_cli_init():
    cli = CLI()
    assert isinstance(cli, CLI)
    
def test_cli_print_table():
    cli = CLI()
    spreadsheet = Spreadsheet("test", 10, 10)
    cli.print_spreadsheet(spreadsheet)
    assert False