import abc
from spreadsheet.Coordinates import Coordinates

def is_float(txt: str):
    try:
        _ = float(txt)
        return True
    except:
        return False


class Content:
    @abc.abstractclassmethod
    def get_value():
        ...
        
    @abc.abstractclassmethod
    def get_value_to_dump():
        ...
    
    @abc.abstractclassmethod
    def set_value():
        ...


class Numerical(Content):
    """TODO: Document"""
    def __init__(self, value: float):
        self._value = value
    
    def get_value(self):
        return self._value
    
    def get_value_to_dump(self):
        return self._value    
    
    def set_value(self, value: float):
        self._value = value
        
    def __str__(self):
        return str(self._value)
        

class Text(Content):
    """TODO: Document"""
    def __init__(self, value: str):
        self._value = value
    
    def get_value(self):
        return self._value
    
    def get_value_to_dump(self):
        return self._value  
    
    def set_value(self, value: str):
        self._value = value
        
    def __str__(self):
        return str(self._value)
        

class Formula(Content):
    """TODO: Document"""
    def __init__(self, repr: str):
        if repr[0] == '=':
            repr = repr[1:]
        self._representation = repr
        self._value = None
        self._dependencies: list[Coordinates] = None
        
    def get_value(self):
        if self._value == None:
            raise Exception("Formula not yet evaluated")
        return self._value
    
    def get_value_to_dump(self):
        return "=" + self._representation  

    def set_value(self, value: int | float):
        self._value = value
    
    def get_representation(self):
        return self._representation
    
    def get_dependencies(self):
        return self._dependencies
    
    def set_dependencies(self, dep):
        self._dependencies = dep
    
    def __str__(self):
        return f"{self._representation} [{self._value}]"
    
    

class ContentFactory:
    @staticmethod
    def get(value: str | int | float):
        if isinstance(value, (int, float)):
            return Numerical(value)
        if value.isnumeric():
            return Numerical(int(value))
        if is_float(value):
            return Numerical(float(value))
        if value is None or value == "":
            return Text('')
        if value[0] == "=":
            return Formula(value)
        return Text(value)