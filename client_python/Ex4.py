from GUI import *
from Logic import *
import time

# default port
PORT = 6666
# server host
HOST = '127.0.0.1'

client = Client()
client.start_connection(HOST, PORT)
parse = Parser()

# First, get how many agents and place them on the playing field
no_of_agents = int(json.loads(client.get_info())["GameServer"]["agents"])


def add_agent():
    size = int(json.loads(client.get_info())["GameServer"]["agents"])
    for i in range(size):
        if size == 1:
            client.add_agent("{\"id\":" + str(9) + "}")  # 9 is an arbitrary choice
        else:
            client.add_agent("{\"id\":" + str(i) + "}")


add_agent()

parse.parse_server_info(client.get_pokemons(), client.get_agents(), client.get_graph())
drawer = GUI(parse)
Brain = Logic(parse)
client.start()

t = 0
if (int(client.time_to_end()) / 1000) > 30:
    t = 1

"""
In this loop the game actually runs when we know how long the 
game will be played and with how many agents we will play
"""

while client.is_running():
    parse.parse_server_info(client.get_pokemons(), client.get_agents(), client.get_graph())
    ttl = int(client.time_to_end())
    client_info = client.get_info().split(",")
    no_of_moves = client_info[2].split(":")[1]
    grade = client.get_info().split(",")
    grade = grade[3].split(":")[1]
    drawer.main(no_of_moves, int(ttl / 1000), grade, no_of_agents)
    print(ttl, client.get_info(), parse.agents[0].speed)
    if no_of_agents == 1:
        Brain.one_agent(client, t)
        client.move()
    else:
        Brain.multiple_agents(client, t)
        client.move()
        for a in parse.agents:
            if a.mode == 0:
                Brain.pick_pok_for_A(a, client)

    time.sleep(0.008)
