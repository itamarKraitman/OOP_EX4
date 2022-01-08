from client import Client
import json
from MVC import Model
import time

"""
===============================================================================
START of code block consisting of function which will be used by the controller
===============================================================================
"""

pokemon_prev_JSON = ""


def parse_pokemon():
    global pokemon_prev_JSON
    pokemons_dictonary = {}
    k = 0
    pokemons_json = client.get_pokemons()
    pokemons_str = json.loads(pokemons_json)
    globals()[pokemon_prev_JSON] = json.loads(pokemons_json)
    pokemons = pokemons_str.get("Pokemons")
    for pokemon in pokemons:
        pokemon_dict = {"value": pokemon.get('Pokemon').get("value"), "type": pokemon.get('Pokemon').get("type"),
                        "pos": pokemon.get('Pokemon').get("pos")}
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
        agent_dict = {"id": new_agent.get('Agent').get("id"), "value": new_agent.get('Agent').get("value"),
                      "src": new_agent.get('Agent').get("src"),
                      "dest": new_agent.get('Agent').get("dest"),
                      "speed": new_agent.get('Agent').get("speed"), "pos": new_agent.get('Agent').get("pos")}
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
    global pokemon_prev_JSON
    if globals()[pokemon_prev_JSON] != json.loads(client.get_pokemons()):
        parse_pokemon()


# TODO: is this needed?
def update_agent_pos():
    pos_list = json.loads(client.get_agents())
    for i in agent_list:
        agent_list[i].set_pos(pos_list['Agents']['agent'])


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
    graph = get_graph()

    parse_pokemon()
    # pokemons = get_pokemons()
    # Get how many agents are in the game
    no_of_agents = get_number_of_agents()

    # Initial phase - insert all agents in the center of the graph
    for i in range(no_of_agents):
        client.add_agent("{\"id\":" + str(graph.centerPoint()) + "}")
    parse_agents()
    print(json.loads(client.get_info()))

    poke_list = get_pokemons()
    agent_list = get_agents()

    # We are ready to start the game & timer
    client.start()
    start_time = time.time()


    # TODO: initial edge choice logic will go here
    # allocate initial state pokemons to agents
    for poke in poke_list:
        Model.allocate_pokemon_to_agent(agent_list, poke)
    for a in range(len(agent_list)):
        client.choose_next_edge('{"agent_id":' + str(agent_list[a].get_id()) + ', "next_node_id":'
                                + str(poke_list[a].get_src())+'}')
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
        for agent in range(len(agent_list)):
            if agent_list[agent].get_dest() == -1:  # TODO: how to update agent position?
                client.choose_next_edge('{"agent_id":' + str(agent_list[agent].get_id()) + ', "next_node_id":'
                                        + str(agent_list[agent].path_pop())+'}')

        # TODO: limit to 10 calls per second- pygame clock.tick()
        client.move()

    client.stop_connection()