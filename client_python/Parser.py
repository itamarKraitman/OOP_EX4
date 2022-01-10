import math as m
from client_python.graph.Graph import *
from Playing_Objects import *
import json
from client import Client

EPS = 0.00000001  # Epsilon for math calculations
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
        """
        this method is responsible to parse the data which is given from the server- graph, pokemons and agents
        this method uses the parse_graph, parss_agents and parse_pokemons methods aheaad
        :param pokemons:
        :param agents:
        :param graph:
        :return:
        """
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

    def parse_pokemon(self, pokemon_str):
        self.pokemons.clear()
        for i in pokemon_str['Pokemons']:
            p = Pokemon(i['Pokemon'])
            self.pokemon_position(p)
            self.pokemons.append(p)

    def pokemon_position(self, pokemon: Pokemon):
        """
        this method target is to determine on which edge the pokemon is on
        this method used the distance, distance,_pokemon_to_node and is_edge method below
        :param pokemon:
        :return:
        """
        for source_node in self.graph.nodes:
            for dest_node in self.graph.nodes:
                distance = self.distance(self.graph.nodes[source_node], self.graph.nodes[dest_node])
                distance2 = (self.distance_pokemon_to_node(self.graph.nodes[source_node], pokemon) +
                             self.distance_pokemon_to_node(self.graph.nodes[dest_node], pokemon))
                ans = abs(distance - distance2)
                if ans <= EPS:
                    if pokemon.type == -1:
                        dest = min(source_node, dest_node)
                        src = max(source_node, dest_node)

                    else:
                        dest = max(source_node, dest_node)
                        src = min(source_node, dest_node)
                    if self.is_edge(src, dest):
                        pokemon.src = src
                        pokemon.dest = dest
                        return

    def distance(self, node1: Node, node2: Node):
        return m.sqrt(pow(node1.pos[0] - node2.pos[0], 2) + pow(node1.pos[1] - node2.pos[1], 2))

    def distance_pokemon_to_node(self, node1: Node, pok: Pokemon):
        return m.sqrt(pow(node1.pos[0] - pok.pos[0], 2) + pow(node1.pos[1] - pok.pos[1], 2))

    def is_edge(self, id1, id2):
        if id1 in self.graph.edges and id2 in self.graph.edges[id1]:
            return True
        else:
            return False
