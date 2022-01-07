from client import Client
import json
from MVC import Model
import time

"""

===============================================================================
START of code block consisting of function which will be used by the controller
===============================================================================

"""

global pokemon_JSON


def parse_pokemon():
    pokemons_dictonary = {}
    k = 0
    pokemons_json = client.get_pokemons()
    pokemons_str = json.loads(pokemons_json)
    globals()[pokemon_JSON] = json.loads(pokemons_json)
    pokemons = pokemons_str.get("Pokemons")
    for pokemon in pokemons:
        pokemon_dict = {"value": pokemon.get("value"), "type": pokemon.get("type"), "pos": pokemon.get("pos")}
        pokemons_dictonary[k] = pokemon_dict
        k += 1
    Model.create_pokemons(pokemons_dictonary)


def parse_agents():
    agents_dictionary = {}
    j = 0
    agents_json = client.get_agents()
    agents_str = json.loads(agents_json)
    agents = agents_str.get("Agents")
    for new_agent in agents:
        agent_dict = {"id": new_agent.get("id"), "value": new_agent.get("value"), "src": new_agent.get("src"),
                      "dest": new_agent.get("dest"),
                      "speed": new_agent.get("speed"), "pos": new_agent.get("pos")}
        agents_dictionary[j] = agent_dict
        j += 1
    Model.create_agents(agents_dictionary)


def parse_graph():
    g = client.get_graph()
    data = json.loads(g)
    node_data = data.get("Nodes")
    edge_data = data.get("Edges")
    Model.create_graph({"nodes": node_data, "edges": edge_data})


def get_pokemons():
    return Model.pokemons


def get_agents():
    return Model.agents


def get_graph():
    return Model.graph_algo


def update_pokemons():
    if globals()[pokemon_JSON] != json.loads(client.get_pokemons()):
        parse_pokemon()


def get_number_of_agents():
    game_info = json.loads(client.get_info())
    number_of_agents = game_info['GameServer']['agents']
    return number_of_agents


def get_time() -> str:
    return client.time_to_end()


def make_decision():
    pokemons = get_pokemons()
    for pokemon in pokemons:
        Model.allocate_pokemon_to_agent(get_agents(), pokemon)


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
        client.add_agent("{\"id\":" + str(graph.centerPoint()) + "}")

    # We are ready to start the game & timer
    client.start()
    start_time = time.time()

    # TODO: initial edge choice logic will go here
    # allocate initial state pokemons to agents
    for poke in poke_list:
        Model.allocate_pokemon_to_agent(agent_list, poke)
    for agent in agent_list:
        client.choose_next_edge('{"agent_id":' + str(agent_list[agent].get_id()) + ', "next_node_id":'
                                + str(agent_list[agent].path_pop()))
    client.move()

    while client.is_running() == 'true':
        # if there is less than 500ms left, stop
        if int(client.time_to_end()) <= 500:
            info = json.loads(client.get_info())
            print(info)
            client.stop()
            break

        update_pokemons()
        make_decision()
        client.move()

    client.stop_connection()
