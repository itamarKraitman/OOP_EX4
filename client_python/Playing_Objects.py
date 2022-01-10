"""
Playing Objects module consisting of class definition for Agents and Pokemons
    :return Agent, Pokemon objects
"""


class Agent:
    def __init__(self, data: dict) -> None:
        self.id = int(data['id'])
        self.value = float(data['value'])
        self.src = int(data['src'])
        self.dest = int(data['dest'])
        self.speed = float(data['speed'])
        position = str(data['pos']).split(',')
        self.pos = []
        for coordinate in position:
            self.pos.append(float(coordinate))
        self.path = []
        self.allocated = 0

    # TODO: check if repr needed
    def __repr__(self) -> str:
        f'{self.value},'

    def get_id(self):
        return self.id

    def set_id(self, new_id: int):
        self.id = new_id

    def get_value(self):
        return self.value

    def set_value(self, new_value: float):
        self.value = new_value

    def get_src(self):
        return self.src

    def set_src(self, new_src: int):
        self.src = new_src

    def get_dest(self):
        return self.dest

    def set_dest(self, new_dest: int):
        self.dest = new_dest

    def get_speed(self) -> float:
        return self.speed

    def set_speed(self, new_speed: float):
        self.speed = new_speed

    def get_pos(self):
        return self.pos

    def set_pos(self, new_pos: tuple):
        self.pos = new_pos

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

    def get_allocated(self):
        return self.mode

    def set_allocated(self, new_mode):
        self.mode = new_mode


class Pokemon:
    def __init__(self, data: dict) -> None:
        self.value = data['value']
        self.type = int(data['type'])
        p = str(data['pos']).split(',')
        self.pos = []
        for i in p:
            self.pos.append(float(i))
        self.src = None
        self.dest = None
        self.allocated = 0

    # TODO: check if repr needed
    def __repr__(self) -> str:
        return f'{self.pos} ' f'{self.src} 'f'{self.dest} 'f'{self.type} 'f'{self.value}'

    def get_value(self):
        return self.value

    def get_type(self):
        return self.type

    def get_pos(self):
        return self.pos

    def set_value(self, value: float):
        self.value = value

    def set_type(self, new_type: int):
        self.type = new_type

    def set_pos(self, pos: tuple):
        self.pos = pos

    def set_src(self, new_src: int):
        self.src = new_src

    def set_dest(self, new_dest: int):
        self.dest = new_dest

    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest

    def get_allocated(self):
        return self.allocated

    def set_allocated(self):
        if self.allocated:
            self.allocated = False
        else:
            self.allocated = True

