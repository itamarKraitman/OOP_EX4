"""
OOP - Ex4
Very simple GUI examples for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace
from client import Client
import json




# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'



client = Client()
client.start_connection(HOST, PORT)

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


client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()



client.move()
# game over: