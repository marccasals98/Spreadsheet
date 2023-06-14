import re

def col_num2text(col_num: int):
    letter = ''
    while col_num > 25 + 1:   
        letter += chr(65 + int((col_num-1)/26) - 1)
        col_num = col_num - (int((col_num-1)/26))*26
    letter += chr(65 - 1 + (int(col_num)))
    return letter


def col_text2num(col_text: str):
    letters = "~ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    col_num = 0
    for idx, char in enumerate(col_text[::-1]):
        col_num += (letters.index(char)) * (26**idx)
    return col_num
    

class Coordinates:
    """Coordinates class.
    
    Attributes
    ----------
    col: int
        Number indicating the column. First column is 1
    
    row: int
        Number indicating the row. First row is 1
    """
    def __init__(self, col: int, row: int):
        self.col, self.row = col, row
        
    @classmethod
    def from_text(cls, text:str) -> "Coordinates":
        """Creates the coordinates given the textual representation
        Example: A1 -> (1,1)
        
        Parameters
        ----------
        text: str
            Textual representation of the coordinates. Ex: A1
            
        Returns
        -------
        Coordinates
            The corresponding coordinates
        """
        col_text, row_num, _ = re.split(r'(\d+)', text)
        col_num = col_text2num(col_text)
        return cls(col_num, int(row_num))
    
    @classmethod
    def range_from_text(cls, text:str) -> tuple["Coordinates", "Coordinates"]:
        """...
        """
        first, last = text.split(":") 
        return cls.from_text(first), cls.from_text(last)
        
    def __repr__(self):
        """Representation dunder method. Just for debugging"""
        return f"{col_num2text(self.col)}{self.row}"
    
    # The following functions are needed for Coordinates to 
    # be a valid dict key    
    def __hash__(self):
        """Hash dunder method"""
        return hash((self.col, self.row))

    def __eq__(self, other):
        """Equal dunder method"""
        return (self.col, self.row) == (other.col, other.row)
