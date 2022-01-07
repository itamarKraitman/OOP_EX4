from types import SimpleNamespace
from client import Client
import json
from MVC import Model
import time
from graph import Graph

"""

===============================================================================
START of code block consisting of function which will be used by the controller
===============================================================================

"""

global pokemon_JSON


def parse_pokemon():
    pokemons_dictonary = {}
    i = 0
    pokemons_json = client.get_pokemons()
    pokemons_str = json.loads(pokemons_json)
    globals()[pokemon_JSON] = json.loads(pokemons_json)
    pokemons = pokemons_str.get("Pokemons")
    for pokemon in pokemons:
        pokemon_dict = {"value": pokemon.get("value"), "type": pokemon.get("type"), "pos": pokemon.get("pos")}
        pokemons_dictonary[i] = pokemon_dict
        i += 1
    Model.create_pokemons(pokemons_dictonary)


def parse_agents():
    agents_dictonary = {}
    i = 0
    agents_json = client.get_agents()
    agents_str = json.loads(agents_json)
    agents = agents_str.get("Agents")
    for agent in agents:
        agent_dict = {"id": agent.get("id"), "value": agent.get("value"), "src": agent.get("src"),
                      "dest": agent.get("dest"),
                      "speed": agent.get("speed"), "pos": agent.get("pos")}
        agents_dictonary[i] = agent_dict
        i += 1
    Model.create_agents(agents_dictonary)


def parse_graph():
    graph = client.get_graph()
    data = json.loads(graph)
    node_data = data.get("Nodes")
    edge_data = data.get("Edges")
    Model.create_graph({"nodes": node_data, "edges": edge_data})


def get_pokemons():
    return Model.pokemons


def get_agents():
    return Model.agents


def get_graph():
    return Model.graph_load


def update_pokemons():
    if globals()[pokemon_JSON] != json.loads(client.get_pokemons()):
        parse_pokemon()


def get_number_of_agents():
    info = json.loads(client.get_info())
    no_a = info.get("GameServer")
    number_of_agents = no_a.get("agents")
    return number_of_agents


def get_time() -> str:
    return client.time_to_end()


def make_decision():
    pass


def update_view():
    pass


def return_error():
    pass


"""

===============================================================================
END of functions code block, main code below
===============================================================================

"""

if __name__ == '__main__':
    # default port
    PORT = 6666
    # server host (default localhost 127.0.0.1)
    HOST = '127.0.0.1'

    client = Client()
    client.start_connection(HOST, PORT)

    parse_graph()
    parse_pokemon()
    parse_agents()
    print(json.loads(client.get_info()))

    graph = get_graph()
    poke_list = get_pokemons()
    agent_list = get_agents()

    # Get how many agents are in the game
    no_of_agents = get_number_of_agents()

    # Initial phase - insert all agents in the center of the graph
    for i in no_of_agents:
        client.add_agent("{\"id\":" + str(Model.graph_algo.centerPoint()) + "}")

    # We are ready to start the game & timer
    client.start()
    start_time = time.time()

    # TODO: initial edge choice logic will go here
    client.move()

    while client.is_running() == 'true':
        # if there is less than 500ms left, stop
        if int(client.time_to_end()) <= 500:
            info = json.loads(client.get_info())
            print(info)
            client.stop()
            break

        # TODO: main edge coice logic will go here
        client.move()

    client.stop_connection()
