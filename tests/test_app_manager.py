from spreadsheet.Spreadsheet import Spreadsheet, Coordinates, Cell, Numerical
from spreadsheet.CLI import CLI
from spreadsheet.AppManager import AppManager

def test_app_manager_init():
    app = AppManager()
    assert isinstance(app, AppManager)
    
def test_app_manager_run():
    app = AppManager()
    app.run()