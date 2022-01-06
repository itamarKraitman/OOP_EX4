from data import Pokemon
from data import Agent
from graph import Graph, GraphAlgo

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
        pokemon = Pokemon.Pokemon(pokemon_dict.get("value"), poke_dict.get("type"), poke_dict.get("pos"))
        pokemons.append(pokemon)
        # i += 1


def create_agents(agent_dict: dict):
    for key in agent_dict:
        agent_dict = agent_dict.get(key)
        agent = Agent.Agent(_id=agent_dict.get("id"), _value=agent_dict.get("value"), _src=agent_dict.get("src"), _dest=agent_dict.get("dest"),
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

    # choose next edge
    for agent in agents:
        if agent.dest == -1:
            next_node = (agent.src - 1) % len(graph.Nodes)
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())
