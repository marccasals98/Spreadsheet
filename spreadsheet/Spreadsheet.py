from __future__ import annotations
import re

from spreadsheet.Content import Content, Numerical, Text, ContentFactory
from spreadsheet.Coordinates import Coordinates

class Cell:
    """Cell class
    Represents a cell in the spreadshet
    
    Attributes
    ----------
    coordinates: Coordinates
        The coordinates of the cell in the table
    content: Content
        The content of the cell
    """
    def __init__(self, coords: Coordinates, content: Content = None):
        if content is None:
            content = Numerical(0)

        self._coordinates = coords
        self._content = content
        
    def __repr__(self):
        """Representation dunder method. Just for debugging"""
        return str(self.get_content())
    
    def get_value(self) -> int | float | str:
        """Get the value of the cell"""
        return self._content.get_value()
    
    def get_content(self) -> int | float | str:
        """Get the value of the cell"""
        return self._content
    
    def set_content(self, content: Content):
        """Sets the content of the cell"""
        self._content = content


class Spreadsheet:
    """Spreadsheet class
    Represents the spreadsheet data.
    
    Attributes
    ----------
    name: str
        Name of the spreadsheet
    num_columns: int
        Number of columns of the spreadsheet
    num_rows: int
        Number of rows of the spreadsheet
    cells: dict[Coordinate, Cell]
        Dictionary with a mapping between each coordinate and the
        cell object in that coordinate
    """
    def __init__(self, name: str, num_columns: int, num_rows: int):
        self.name = name
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.cells: dict[Coordinates, Cell] = {}
        self._initialize_cell_dict(num_columns, num_rows)
        
    @classmethod
    def from_values(cls, values: list[list[int|float|str]]) -> Spreadsheet:
        """Creates a Spreadsheet from a matrix of values.
        
        Parameters
        ----------
        values: list[list[int|float|str]]
            Matrix of values to fill the spreadsheet to create
        
        Returns
        -------
        Spreadsheet 
            New spreadsheet 
        """
        num_rows = len(values)
        num_cols = max([len(row) for row in values])
        print(f"!!! {num_cols} {num_rows}")
        sheet: Spreadsheet = cls("sheet", num_cols, num_rows)
        for row_idx, row in enumerate(values):
            for col_idx, value in enumerate(row):
                content = ContentFactory.get(value)
                coords = Coordinates(col_idx+1, row_idx+1)
                sheet.cells[coords].set_content(content)
        return sheet
    
    def _initialize_cell_dict(self, num_columns: int, num_rows: int) -> dict:
        """
        Create new dictionary of cells
        
        Arguments:
        ----------
        num_columns : int
                the number of columns of the dictionary.
        num_rows : int
                the number of columns of the dictionary.
        """
        for c in range(1, num_columns+1):
            for r in range(1, num_rows+1):
                coords = Coordinates(col=c,row=r)
                if coords not in self.cells:
                    self.cells[coords] = Cell(coords)

    def size(self) -> tuple[int, int]:
        """Retruns the number of columns and rows of the spreadsheet"""
        return self.num_columns, self.num_rows
        
    def get_range(self, 
                  ul_coord: Coordinates, 
                  lr_coord: Coordinates) -> list[Cell]:
        """Returns a list of cells contained on a range defined by
        the corner coordinates of the range.

        Parameters
        ----------
        ul_coord: Coordinates
            Upper-left coordinates
        lr_coord: Coordinates
            Lower-right coordinates
            
        Returns
        -------
        list[Coords]
            List of cells inside the range
        """
        ls = []
        for c in range(ul_coord.col, lr_coord.col+1):
            for r in range(ul_coord.row, lr_coord.row+1):
                coords = Coordinates(c, r)
                ls.append(coords)
        return ls
    
    def get_values(self):
        """Return all the values (casted to string) of the 
        spreadsheet in matrix form.
        
        Note: This is mainly used for IO proposes.
        
        Returns
        -------
        list[list[str]]
            Matrix of values
        """
        values = []
        for row in range(1, self.num_rows+1):
            row_values = []
            for col in range(1, self.num_columns+1):
                coord = Coordinates(col, row)
                row_values.append(str(self.cells[coord].get_value()))
            values.append(row_values)
        return values
            
            
    def expand(self, num_cols: int, num_rows: int):
        """_summary_
        """
        self.num_columns = max(self.num_columns, num_cols)
        self.num_rows = max(self.num_rows, num_rows)
        self._initialize_cell_dict(self.num_columns, self.num_rows)
        
