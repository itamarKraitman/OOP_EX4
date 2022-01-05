
from data import Pokemon
from data import Agent

pokemons = {}
agents = {}

def create_pokemons(poke_dict:dict):
    pass

def create_agents(agent_dict:dict):
    pass

def create_graph(graph_dict:dict):
    pass


# choose next edge
    for agent in agents:
        if agent.dest == -1:
            next_node = (agent.src - 1) % len(graph.Nodes)
            client.choose_next_edge(
                '{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())