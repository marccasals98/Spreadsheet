from pathlib import Path
import os 

from copy import deepcopy

from spreadsheet.CLI import CLI
from spreadsheet.Spreadsheet import Spreadsheet, Coordinates
from spreadsheet.Content import ContentFactory, Formula, Content
from spreadsheet.FormulaEvaluator import FormulaEvaluator

from edu.upc.etsetb.arqsoft.spreadsheet.entities.circular_dependency_exception import CircularDependencyException

class SpreadsheetIO:
    """SpreadsheetIO class
    Responsible for reading.writing spreadsheets to files
    
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
        self.spreadsheet: Spreadsheet = Spreadsheet("empty", 1, 1)
        self.cli: CLI = None
        # Mapping cell => list of cells
        self.cell_dependencies: dict[Coordinates, list[Coordinates]] = {}

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
        self.spreadsheet = Spreadsheet("my spreadsheet", 10, 10)
        
    
    def _update_dependencies(self, coords: Coordinates, new_content: Content):
        """Update the dependencies between cells."""
        # Save copy of dependencies for rollback
        old_dependencies = deepcopy(self.cell_dependencies)
        
        # If cell had a formula before, remove dependencies
        content = self.spreadsheet.cells[coords].get_content()
        if isinstance(content, Formula):
            for cell in content.get_dependencies():
                self.cell_dependencies[cell].remove(coords)
                
        # If new content is not formula, no need to add dependencies
        if not isinstance(new_content, Formula):
            return
        
        # Add new dependencies
        for cell in new_content.get_dependencies():
            if cell not in self.cell_dependencies:
                self.cell_dependencies[cell] = []
            self.cell_dependencies[cell].append(coords)
        
        # Check for circular dependencies
        if self.check_circular_dependencies([coords]):
            self.cell_dependencies = old_dependencies
            raise CircularDependencyException("Formula introduced circular dependencies!")
    
        
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
        coords = Coordinates.from_text(coords)
        content = ContentFactory.get(value)
        if coords not in self.spreadsheet.cells:
            self.spreadsheet.expand(coords.col, coords.row)
        if isinstance(content, Formula):
            evaluator = FormulaEvaluator(content, self.spreadsheet)
            evaluator.evaluate()
            evaluator.update_dependencies()
        self._update_dependencies(coords, content)
        
        self.spreadsheet.cells[coords].set_content(content)
        
        # Recompute cells that depend on new cell
        dependencies = self.cell_dependencies.get(coords, []).copy()
        recomputed_cells = set()
        while dependencies:
            cell = dependencies.pop()
            # if cell in recomputed_cells:
            #     raise ValueError("Circular Dependency")
            recomputed_cells.add(cell)
            evaluator = FormulaEvaluator(self.spreadsheet.cells[cell].get_content(), 
                                         self.spreadsheet)
            evaluator.evaluate()
            dependencies.extend(self.cell_dependencies.get(cell, []).copy())

            
        
    def check_circular_dependencies(self, coords: list[Coordinates]):
        """Check if there is a circular dependency involving `coords`"""
        # BFS
        cells_to_check = coords.copy()
        checked_cells = set(coords)
        while cells_to_check:
            cells_to_check_future = []
            for cell in cells_to_check:
                for dep_cell in self.cell_dependencies.get(cell, []):
                    if dep_cell in checked_cells:
                        return True
                    cells_to_check_future.append(dep_cell)
                    checked_cells.add(dep_cell)
            cells_to_check = cells_to_check_future
        
        return False

    def load_spreadsheet_from_file(self, path: str):
        """Load a spreadsheet from a path (sv2 format)

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
        

    ### The following methods are just for the checker:
    def set_cell_content(self, coord, str_content):
        self.edit_cell(coord, str_content)
    
    def get_cell_content_as_float(self, coord):
        if (coords := Coordinates.from_text(coord)) not in self.spreadsheet.cells:
            self.spreadsheet.expand(coords.col, coords.row)
        return float(self.spreadsheet.cells[Coordinates.from_text(coord)].get_value())
    
    def get_cell_content_as_string(self, coord):
        if (coords := Coordinates.from_text(coord)) not in self.spreadsheet.cells:
            self.spreadsheet.expand(coords.col, coords.row)
        value = self.spreadsheet.cells[Coordinates.from_text(coord)].get_value()
        return value if value else ""
    
    def get_cell_formula_expression(self, coord):
        if (coords := Coordinates.from_text(coord)) not in self.spreadsheet.cells:
            self.spreadsheet.expand(coords.col, coords.row)
        formula: Formula = self.spreadsheet.cells[Coordinates.from_text(coord)].get_content()
        return "=" + formula.get_representation().replace(";", ",")
        # return self.get_cell_content_as_string(coord)
        