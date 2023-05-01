import abc

class Content:
    @abc.abstractclassmethod
    def get_value():
        ...
    
    @abc.abstractclassmethod
    def set_value():
        ...


class Numerical(Content):
    def __init__(self, value: float):
        self._value = value
    
    def get_value(self):
        return self._value
    
    def set_value(self, value: float):
        self._value = value
        

class Text(Content):
    def __init__(self, value: str):
        self._value = value
    
    def get_value(self):
        return self._value
    
    def set_value(self, value: str):
        self._value = value