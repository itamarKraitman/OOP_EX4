class Agent:

    def __init__(self, _id: int, _value: float, _src: int, _dest: int, _speed: float, _pos: int):
        self._id = _id
        self._value = _value
        self._src = _src
        self._dest = _dest
        self._speed = _speed
        self._pos = _pos
        self.path = []

    def get_id(self):
        return self._id

    def set_id(self, new_id: int):
        self._id = new_id

    def get_value(self):
        return self._value

    def set_value(self, new_value: float):
        self._value = new_value

    def get_src(self):
        return self._src

    def set_src(self, new_src: int):
        self._src = new_src

    def get_dest(self):
        return self._dest

    def set_dest(self, new_dest: int):
        self._dest = new_dest

    def get_speed(self):
        return self._speed

    def set_speed(self, new_speed: float):
        self._speed = new_speed

    def get_pos(self):
        return self._pos

    def set_pos(self, new_pos: tuple):
        self._pos = new_pos

    def add_path(self, lst: list):
        for i in lst:
            self.path.append(i)

    def get_path(self):
        return self.path

    def get_path_head(self):
        return self.path[0]

    def path_pop(self):
        head = self.path[0]
        self.path.pop(0)
        return head

    def set_path(self, path: list):
        self.path = path
