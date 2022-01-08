import sys

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
        pos = str(pokemon_dict.get("pos"))
        split_pos = pos.split(',')
        x = float(split_pos[0])
        y = float(split_pos[1])
        z = float(split_pos[2])
        pokemon = Pokemon.Pokemon(pokemon_dict.get("value"), pokemon_dict.get("type"), (x, y, z))
        set_pokemon_src_dest(pokemon)
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


def quadratic_formula(a, b, c):
    x1 = ((-b) + math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    x2 = ((-b) - math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    return x1, x2


def set_pokemon_src_dest(p: Pokemon):
    for src in graph_load.edges:
        for dest in graph_load.all_out_edges_of_node(src):
            dist_poke2src = Location.distance(p.get_pos(), graph_load.nodes.get(src).getPosition())
            dist_poke2dest = Location.distance(p.get_pos(), graph_load.nodes.get(dest).getPosition())
            dist_poke2edge = Location.distance_to_edge(p.get_pos(), graph_load.nodes.get(src).getPosition(),
                                                       graph_load.nodes.get(dest).getPosition())
            if abs(dist_poke2src + dist_poke2dest - dist_poke2edge) < 0.01:
                if src > dest:
                    p.set_src(src)
                    p.set_dest(dest)
                    break
                elif src < dest:
                    p.set_src(dest)
                    p.set_dest(src)
                    break


def allocate_pokemon_to_agent(agent_list: list, poke: Pokemon):
    min_weight = sys.maxsize
    min_path = []
    min_agent_id = 0
    for i in range(len(agent_list)):
        temp_path = agent_list[i].get_path()
        temp_path.append(poke.get_src())
        temp_min_path, temp_min_weight = graph_algo.tsp(temp_path)
        if min_weight > temp_min_weight:
            min_weight = temp_min_weight
            min_agent_id = i
            min_path = temp_path
    agent_list[min_agent_id].add_path(min_path)
    agents[min_agent_id] = agent_list[min_agent_id]
    # TODO: should this return anything?
