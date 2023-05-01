class AppManager:
    def __init__(spreadsheet: "Spreadsheet"):
        self.spreadsheet = spreadsheet
        self.cli = CLI()
        self.formula_evaluator = FormulaEvaluator()

    def execute_command(cmd: str):
        ...

    def set_spreadsheet(spreadsheet: Spreadsheet):
        ...

    def open_spreadhseet(url: str):
        ...
