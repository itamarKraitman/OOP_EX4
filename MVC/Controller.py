from types import SimpleNamespace
from client import Client
import json
from MVC import Model

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
    pokemons = client.get_pokemons()
    Model.create_pokemons(pokemons)


def parse_agents():
    agents = client.get_agents()
    Model.create_agents(agents)


def parse_graph():
    graph = client.get_graph()
    Model.create_graph(graph)


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
