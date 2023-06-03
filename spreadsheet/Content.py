import abc

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
        

class Formula(Content):
    def __init__(self, repr: str):
        self._representation = repr
        
    def get_value(self):
        ...
    
    def get_representation(self):
        return self._value
    

class ContentFactory:
    @staticmethod
    def get(value: str | int | float):
        if isinstance(value, (int, float)):
            return Numerical(value)
        if value.isnumeric():
            return Numerical(int(value))
        if is_float(value):
            return Numerical(float(value))
        # if value[0] == "=":
        #     return Formula(value)
        return Text(value)