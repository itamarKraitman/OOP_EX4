from MVC import Agent, Pokemon
from graph import Graph, GraphAlgo, Location
import math

pokemons = []
agents = []
graph_load = Graph.Graph()
graph_algo = GraphAlgo.GraphAlgo(graph_load)


def create_pokemons(poke_dict: dict):
    """
    creating pokemons from dict and stores them in list of pokemons in order to use them in view easily
    :param poke_dict:
    :return:
    """
    # i = 0
    for key in poke_dict:
        pokemon_dict = poke_dict.get(key)
        pokemon = Pokemon.Pokemon(pokemon_dict.get("value"), pokemon_dict.get("type"), pokemon_dict.get("pos"))
        _set_pokemon_src_dest(pokemon)
        pokemons.append(pokemon)
        # i += 1


def create_agents(agent_dict: dict):
    for key in agent_dict:
        all_agents = agent_dict.get(key)
        agent = Agent.Agent(_id=all_agents.get("id"), _value=all_agents.get("value"), _src=all_agents.get("src"),
                            _dest=agent_dict.get("dest"),
                            _speed=agent_dict.get("speed"), _pos=GraphAlgo.GraphAlgo.centerPoint(graph_algo))
        agents.append(agent)


def create_graph(graph_info: dict):
    nodes = graph_info.get("nodes")
    edges = graph_info.get("edges")
    # graph_load = Graph.Graph()
    for node in nodes:
        # If no position is given, set it to None
        if len(node) == 1:
            graph_load.add_node(node.get("id"), (None, None, None))

        elif len(node) == 2:
            key = node.get("id")
            pos = str(node.get("pos"))
            split_pos = pos.split(',')
            x = float(split_pos[0])
            y = float(split_pos[1])
            z = float(split_pos[2])
            graph_load.add_node(key, (x, y, z))
        for edge in edges:
            src = edge.get("src")
            weight = edge.get("w")
            dest = edge.get("dest")
            graph_load.add_edge(src, dest, weight)
            graph_load.add_rev_edge(dest, src, weight)


def distance_from_pokemon():
    """
    returns the distance between agent to all pokemons in order to decide to which pokemon go
    using TSP/SP
    :return:
    """
    pass


def get_pokemons_values():
    """
    returns all pokemons values
    :return:
    """
    pass


def quadratic_formula(self, a, b, c):
    x1 = ((-b) + math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    x2 = ((-b) - math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    return x1, x2


def _set_pokemon_src_dest(p: Pokemon):
    for edge in graph_load.edges:
        dist_poke2src = Location.distance(p.get_pos(), edge.getSrc())
        dist_poke2dest = Location.distance(p.get_pos(), edge.getDest())
        dist_poke2edge = Location.distance_to_edge(p.get_pos, edge.getSrc(), edge.getDest())
        if abs(dist_poke2src + dist_poke2dest - dist_poke2edge) < 0.00000001:
            if edge.getSrc() < edge.getDest() and p.get_type() > 0:
                p.set_src(edge.getSrc())
                p.set_dest(edge.getDest())
                break
            elif edge.getSrc() > edge.getDest() and p.get_type() < 0:
                p.set_src(edge.getSrc())
                p.set_dest(edge.getDest())
                break
