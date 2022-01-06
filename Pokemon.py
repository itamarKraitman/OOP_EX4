class Pokemon:

    def __init__(self, _value: float, _type: int, _pos: tuple):
        self._value = _value
        self._type = _type
        self._pos = _pos

    def get_value(self):
        return self._value

    def get_type(self):
        return self._type

    def get_pos(self):
        return self._pos

    def set_value(self, value: float):
        self._value = value

    def set_type(self, type: int):
        self._type = type

    def set_pos(self, pos: tuple):
        self._pos = pos
