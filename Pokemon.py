import json
import math

from graph.Location import Location


class Pokemon:

    def __init__(self, *args):
        if len(args) == 3:
            self.value = args[0]
            self.type = args[1]
            self.pos = args[2]
        else:
            self.value = math.inf
            self.type = 0  # by default
            self.pos = Location(0, 0, 0)

    def load_pokemons(self, file_name):
        """
        loading pokemon from JSON string
        :param file_name: file that contains JSON string
        :return: True if pokemon was loaded successfully, False otherwise
        """
        try:
            with open(file_name, "r") as incoming:
                data = json.loads(incoming.read())
                value = 




