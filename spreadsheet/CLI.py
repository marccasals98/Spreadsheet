from re import match
from rich import box
from rich.console import Console
from rich.table import Table

from spreadsheet.Spreadsheet import Spreadsheet, Coordinates, col_num2text

# Command list and the regex expression to match
COMMANDS = {
    'RF': r'RF',
    'C': r'C',
    'E': r'E (?P<coordinates>.*) (?P<content>.*)',
    'L': r'L (?P<path>.*)',
    'S': r'S (?P<path>.*)',
    'EXIT': r'EXIT'
}


class CLI:
    """Command-Line Interface Class"""
    def __init__(self):
        self._spreadsheet_loaded = False
        self.console = Console()


    def cprint(self, msg: str | Table):
        """Print a message on the console using the rich system
        
        Parameters
        ----------
        msg: str | Table
            Message to print on the console
        """
        self.console.print(msg)
        
        
    def cerror(self, msg: str):
        """Print an error message on the console
        
        Parameters
        ----------
        msg: str
            Message to print as an error on the console
        """
        self.console.print(f"[bold red]Error: {msg}")
        
        
    def parse_command(self, line: str) -> tuple[str, dict] | None:
        """Parse a command entered in a line into two components:
            - the command name
            - the command arguments
        
        Parameters
        ----------
        line: str
            String containing the command and arguments in a line
            
        Returns
        -------
        tuple[str, dict] | None
            If the command is valid, returns a tuple with the name
            of the command and a dictionary with the parsed arguments.
            If the command is invalid, returns None
        """
        for cmd_name, cmd_pattern in COMMANDS.items():
            if (m := match(cmd_pattern, line)):
                self.cprint(f"[green]Command found! {m.groupdict()}")
                return cmd_name, m.groupdict()
        return None

    def read_command(self) -> tuple[str, dict]:
        """Block the execution and asks for a command as user's input. 
        Once a correct command is provided as input, it returns the 
        command name and the arguments provided 

        Returns
        -------
        tuple[str, dict]
            A tuple with the name of the command and a dictionary 
            with the parsed arguments.
        """
        line = input()
        if line.strip() == "":
            return self.read_command()
        
        if (parsed := self.parse_command(line)) is not None:
            return parsed
        
        self.cprint(f"[bold red]Command {line} not found")
        self.read_command()

            
    def print_spreadsheet(self, sheet: Spreadsheet):
        """Prints on console a rich table with the contents of a
        spreadsheet.
        
        Parameters
        ----------
        sheet: Spreadsheet
            The spreadsheet to print on the console
        """
        ncol, nrow = sheet.size()
        tab = Table(title=sheet.name)
        tab.add_column("", justify="right", )
        for c in range(1, ncol+1):
            tab.add_column(col_num2text(c))
        for r in range(1, nrow+1):
            row_vals = [sheet.cells[Coordinates(c,r)].get_value() 
                        for c in range(1, ncol+1)]
            tab.add_row(str(r), *[str(val) for val in row_vals])
        self.cprint(tab)