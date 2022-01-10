"""
Class Node
In this class we receive Node's value and create it.
Values: key - the id number of the node.
        pos - the geographical position values of where the node is located.
        out - the edges that goes out of the node.
        in - the edges that goes into the node.
"""


# TODO : change comment at the top

class Node:
    # constructor
    def __init__(self, key, position: tuple):
        self.key = key
        # self.position = position.copyLoc(position)
        self.pos = position
        self.weight = None

    def getKey(self):
        return self.key

    def getPosition(self):
        return self.pos

    def setPosition(self, coordinates: tuple):
        self.pos = coordinates

    def __str__(self):
        return f'key = {self.key}, ' f'pos = {self.pos}'

    # TODO: do we need this?
    # String with node's values
    def __repr__(self) -> str:
        return f'key = {self.key}, ' f'pos = {self.pos}'
