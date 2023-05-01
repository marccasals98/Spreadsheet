# from openpyxl.utils.cell import get_column_letter
from collections import namedtuple

from spreadsheet.Content import Content, Numerical, Text


Coordinates = namedtuple("Coords", "col row")


class Cell:
    def __init__(self, coords: Coordinates, content: Content = None):
        if content is None:
            content = Numerical(0)

        self._coordinates = coords
        self._content = content
        
    def __repr__(self):
        return f"<Cell value={self.get_value()}>"
    
    def get_value(self):
        return self._content.get_value()


class Spreadsheet:
    def __init__(self, name: str, num_columns: int, num_rows: int):
        self.name = name
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.cells: dict[Coordinates, Cell] = self._initialize_cell_dict(num_columns, num_rows)
        
    @staticmethod
    def _initialize_cell_dict(num_columns: int, num_rows: int) -> dict:
        """
        Create new dictionary of cells
        
        Arguments:
        ----------
        num_columns : int
                the number of columns of the dictionary.
        num_rows : int
                the number of columns of the dictionary.

        Returns:
        --------
        d : dict
                the dictionary of cells. 
        """
        d = dict()
        for c in range(1, num_columns+1):
            for r in range(1, num_rows+1):
                coords = Coordinates(col=c,row=r)
                d[coords] = Cell(coords)
        return d

    def size(self) -> tuple[int, int]:
        return self.num_columns, self.num_rows
        
    def get_range(self, ll_coord: Coordinates, ur_coord: Coordinates):
        
        ls = []
        for c in range(ll_coord.col, ur_coord.col+1):
            for r in range(ll_coord.row, ur_coord.row+1):
                ls.append(self.cells[(c, r)])
        return ls
            