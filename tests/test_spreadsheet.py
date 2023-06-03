from spreadsheet.Spreadsheet import Spreadsheet, Coordinates, Cell, Numerical, col_text2num

def test_spradsheet_init():
    spreadsheet = Spreadsheet("test", 10, 10)
    assert isinstance(spreadsheet, Spreadsheet)
    assert len(spreadsheet.cells) == 100
    print(spreadsheet.cells)
    # assert False # The prints only works when we have an error. So we force an error.


def test_spradsheet_size():
    spreadsheet = Spreadsheet("test", 10, 10)
    assert spreadsheet.size() == (10, 10)
    
    
def test_spradsheet_get_range_1():
    spreadsheet = Spreadsheet("test", 10, 10)
    c1 = Coordinates(col=1, row=3)
    c2 = Coordinates(col=1, row=5)
    cells = spreadsheet.get_range(c1, c2)
    assert len(cells) == 3


def test_spradsheet_get_range_2():
    spreadsheet = Spreadsheet("test", 10, 10)
    c1 = Coordinates(col=1, row=3)
    c2 = Coordinates(col=3, row=5)
    cells = spreadsheet.get_range(c1, c2)
    assert len(cells) == 9
    print(cells)
    # assert False
    
def test_spradsheet_get_range_3():
    spreadsheet = Spreadsheet("test", 10, 10)
    spreadsheet.cells[Coordinates(1,1)] = Cell((1, 1), Numerical(3))
    c1 = Coordinates(col=1, row=1)
    c2 = Coordinates(col=3, row=3)
    cells = spreadsheet.get_range(c1, c2)
    assert len(cells) == 9
    assert cells[0].get_value() == 3
    # print(cells)
    # assert False

def test_col_text2num():
    inputs = ["A", "B", "Z", "AA", "AB", "CD"]
    expect = [  1,   2,  26,   27,   28,  82]
    for (inp, exp) in zip(inputs, expect):
        assert col_text2num(inp) == exp