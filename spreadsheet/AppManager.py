from pathlib import Path
import os 

from spreadsheet.CLI import CLI
from spreadsheet.Spreadsheet import Spreadsheet, Coordinates
from spreadsheet.Content import ContentFactory, Formula

class SpreadsheetIO:
    """SpreadsheetIO class
    Responsible for reading/writing spreadsheets to files
    
    File formats supported:
        - sv2
    """
    @staticmethod
    def save_sheet(spreadsheet: Spreadsheet, path: str | Path):
        """Saves a spreadsheet into the desired path (sv2 format)

        Parameters
        ----------
        spreadsheet: Spreadsheet
            The spreadsheet to save
        path: str | path
            The path to save the file to
        """
        path = Path(path)
        if path.is_dir():
            path = path / 'sheet.sv2'
        values = spreadsheet.get_values()
        
        # Clean values for saving
        for i in range(len(values)):
            row = values[i]
            row = [val.replace(";", ",") if val != "0" else "" for val in row]
            while row and row[-1] == "":
                row.pop()
            values[i] = row
        
        with path.open(mode='w') as f:
            f.writelines([';'.join(row) + '\n' for row in values])
            f.write("\n")
        
    @staticmethod
    def load_sheet(path: str | Path) -> Spreadsheet:
        """Loads a spreadsheet from a file (sv2 format)

        Parameters
        ----------
        path: str | path
            The path to the file to read
            
        Returns
        -------
        Spreadsheet
            The parsed spreadsheet
        """
        path = Path(path)
        rows = []
        with path.open(mode='r') as f:
            for line in f.readlines():
                if (line := line.strip()):
                    rows.append(line.split(";"))
        rows = [[
            val.replace(",", ";")
            for val in row] for row in rows]
        return Spreadsheet.from_values(rows)
        

class AppManager:
    """AppManager class
    Responsible for controlling the main components of the app.
    """
    def __init__(self):
        self.spreadsheet = Spreadsheet("empty", 1, 1)
        self.cli = None
        self.formula_evaluator = None

    def execute_command(self, cmd: str, **argv):
        """Execute a command given its name and arguments
        
        Parameters
        ----------
        cmd: str
            Command name. Must be one in ("RF", "C", "E", "L", "S")
        """
        match cmd:
            case "RF":
                self.read_commands_from_file(argv['path'])
            case "C":
                self.create_new_sheet()                  
            case "E":
                self.edit_cell(argv['coordinates'], argv['content'])
            case "L":
                self.load_sheet_from_file(argv['path'])
            case "S":
                self.save_sheet_to_file(argv['path'])

    def read_commands_from_file(self, path: str | Path):
        """Run all the commands present in a text file
        
        Parameters
        ----------
        path: str | Path
            Path to the file to read the commands from
        """
        # TODO: test
        path = Path(path)
        if not path.exists():
            self.cli.cerror(f"The file {path} does not eist")
            return
        with path.open(mode='r') as file:
            for line_idx, line in enumerate(file.readlines()):
                if (parsed := self.cli.parse_command(line)):
                    cmd, args = parsed
                    self.execute_command(cmd, **args)
                else:
                    self.cli.cerror(f"Wrong command from file at "
                                    f"line {line_idx}")

    def create_new_sheet(self):
        """Creates a new empty spreadsheet"""
        # TODO: Check default values
        self.spreadsheet = Spreadsheet("my spreadsheet", 10, 10)
        
    def edit_cell(self, coords: str, value: str | float | int):
        """Edits the content of a cell

        Parameters
        ----------
        coords: str
            Coordinates in the text format (Ex: A4)
        value: str | float | int
            Value to assign to the cell. It will be casted to a 
            content of type (Formula, Text or Numerical)
        """
        content = ContentFactory.get(value)
        if isinstance(content, Formula):
            # TODO: Evaluate function value
            ...
        coords = Coordinates.from_text(coords)
        if coords not in self.spreadsheet.cells:
            self.spreadsheet.expand(coords.col, coords.row)
        self.spreadsheet.cells[coords].set_content(content)
        # TODO: Update all influenced cells

    def load_spreadsheet_from_file(self, path: str):
        """Loads a spreadsheet from a path (sv2 format)

        Parameters
        ----------
        path: str
            Path to the file
        """
        path = os.path.join(os.getcwd(), path)
        self.spreadsheet = SpreadsheetIO.load_sheet(path)
    
    def save_spreadsheet_to_file(self, path: str):
        """Saves a spreadsheet to a file (sv2 format)

        Parameters
        ----------
        path: str
            Path to the file
        """
        path = os.path.join(os.getcwd(), path)
        SpreadsheetIO.save_sheet(self.spreadsheet, path)
        
    def run(self):
        """Runs the program by launching a CLI.
        The program will run indefinetely until the command 
        "EXIT" is provided as input
        """
        self.cli = CLI()
        cmd, args = self.cli.read_command()
        while cmd != "EXIT":
            self.execute_command(cmd, **args)
            self.cli.print_spreadsheet(self.spreadsheet)
            cmd, args = self.cli.read_command()
        

    ### The following are classes are just for the checker:
    def set_cell_content(self, coord, str_content):
        self.edit_cell(coord, str_content)
    
    def get_cell_content_as_float(self, coord):
        return float(self.spreadsheet.cells[Coordinates.from_text(coord)].get_value())
    
    def get_cell_content_as_string(self, coord):
        return str(self.spreadsheet.cells[Coordinates.from_text(coord)].get_value())
    
    def get_cell_formula_expression(self, coord):
        # TODO: Change
        # formula: Formula = self.spreadsheet.cells[Coordinates.from_text(coord)].get_content()
        # return formula.get_representation()
        return self.get_cell_content_as_string(coord)
        