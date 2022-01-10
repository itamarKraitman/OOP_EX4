import math as m
from Graph import *
from Playing_Objects import *
import json
from client import Client

EPS = 0.00000000001  # Epsilon for math calculations
client = Client()

"""
Main Parser class for all the JSON encoded info coming in from the server
first, parses the graph, than agents & pokemon afterwards
"""


class Parser:
    def __init__(self) -> None:
        self.graph = Graph()
        self.pokemons = []
        self.agents = []

    def parse_server_info(self, pokemons=None, agents=None, graph=None):

        if graph is not None:
            graph_json = json.loads(graph)
            self.parse_graph(graph_json)

        if agents is not None:
            agents_json = json.loads(agents)
            self.parse_agents(agents_json)

        if pokemons is not None:
            poke_json = json.loads(pokemons)
            self.parse_pokemon(poke_json)

    def parse_graph(self, graph):
        for n in graph["Nodes"]:
            if "pos" in n:
                data = n["pos"].split(',')
                self.graph.add_node(n["id"], (float(data[0]), float(data[1]), float(data[2])))

        for e in graph["Edges"]:
            self.graph.add_edge(int(e["src"]), int(e["dest"]), float(e["w"]))

    def parse_agents(self, agents):
        self.agents = []
        for i in agents['Agents']:
            self.agents.append(Agent(i['Agent']))

    def parse_pokemon(self, pokemon):
        self.pokemons.clear()
        for i in pokemon['Pokemons']:
            p = Pokemon(i['Pokemon'])
            self.pok_pos(p)
            self.pokemons.append(p)

    """
    Function to determine which edge a Pokemon is on
    :param Pokemon
    :returns source, destination for Pokemon
    """

    def pok_pos(self, pok: Pokemon):
        for source_node in self.graph.nodes:
            for dest_node in self.graph.nodes:
                d1 = self.distance(self.graph.nodes[source_node], self.graph.nodes[dest_node])
                d2 = (self.distance_poke2node(self.graph.nodes[source_node], pok) + self.distance_poke2node(
                    self.graph.nodes[dest_node], pok))
                if abs(d1 - d2) <= EPS:
                    src = None
                    dest = None
                    if pok.type == -1:
                        dest = min(source_node, dest_node)
                        src = max(source_node, dest_node)
                    else:
                        dest = max(source_node, dest_node)
                        src = min(source_node, dest_node)

                    if self.is_edge(src, dest):
                        pok.src = src
                        pok.dest = dest
                        return
                    return

    def distance(self, node1: Node, node2: Node):
        dis = m.sqrt(pow(node1.pos[0] - node2.pos[0], 2) + pow(node1.pos[1] - node2.pos[1], 2))
        return dis

    def distance_poke2node(self, node1: Node, pok: Pokemon):
        dis = m.sqrt(pow(node1.pos[0] - pok.pos[0], 2) + pow(node1.pos[1] - pok.pos[1], 2))
        return dis

    def is_edge(self, src, dest) -> bool:
        return (src, dest) in self.graph.edges
