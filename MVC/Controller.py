from types import SimpleNamespace
from client import Client
import json
from MVC import Model
from graph import Graph

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

client = Client()
client.start_connection(HOST, PORT)

'''
pokemons = client.get_pokemons()
# Amazing Python one-liner for parsing JSON objects -
# from - https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

print(pokemons)

graph_json = client.get_graph()

# Amazing Python one-liner for parsing JSON objects -
# from - https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))
'''

client.add_agent("{\"id\":0}")


# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")


def parse_pokemon():
    pokemons_dictonary = {}
    i = 0
    pokemons_json = client.get_pokemons()
    pokemons_str = json.loads(pokemons_json)
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
        agent_dict = {"id": agent.get("id"), "value": agent.get("value"), "src": agent.get("src"), "dest": agent.get("dest"),
                      "speed": agent.get("speed"), "pos": agent.get("pos")}
        agents_dictonary[i] = agent_dict
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
    return  Model.agents

def get_graph():
    return  Model.graph_load

def update_agents():
    pass


def update_pokemons():
    pass


# Once we parse everything and all the objects are loaded, start the game
def start_game():
    client.start()
    pass


def get_game_state():
    info = client.get_info()
    print(info)


def get_time() -> str:
    return client.time_to_end()


def make_decision():

    pass


def update_view():
    pass


def return_error():
    pass
