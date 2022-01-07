
class Pokemon:

    def __init__(self, _value: float, _type: int, _pos: tuple):
        self._value = _value
        self._type = _type
        self._pos = _pos
        self.src = None
        self.dest = None

    def get_value(self):
        return self._value

    def get_type(self):
        return self._type

    def get_pos(self):
        return self._pos

    def set_value(self, value: float):
        self._value = value

    def set_type(self, new_type: int):
        self._type = new_type

    def set_pos(self, pos: tuple):
        self._pos = pos

    def set_src(self, new_src: int):
        self.src = new_src

    def set_dest(self, new_dest: int):
        self.dest = new_dest

    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest
