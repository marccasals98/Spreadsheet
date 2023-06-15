# Spreadsheet
This spreadsheet is the final project of the ARQSOFT subject in MATT (UPC)

Authors: Raul Higueras, Marc Casals

# How to run
In order to run all the scripts, do:
 1. Go to SpreadsheetMarkerForStudents/src
 2. Change the pyt
 3. Run the TestRunner class inside the `tests` folder without changing directory

> Important!
> The project needs python 3.10 or higher to work


```{bash}
cd SpreadsheetMarkerForStudents/src
export PYTHONPATH="$(pwd):$(pwd)/../test"
python3 ../test/edu/upc/ac/marker/TestsRunner.py
```

In case of running this command with a powershell, you should do the following:

```{bash}
cd SpreadsheetMarkerForStudents/src
$env:pythonpath = "$pwd;$pwd\..\test"
python3 ../test/edu/upc/ac/marker/TestsRunner.py
```

Commands:

* RF: Read a the commands from a file.

* C: Creates a new sheet.

* E: Edits a cell.

* L: Loads a sheet from a file.

* S: Saves the sheet to a file.
