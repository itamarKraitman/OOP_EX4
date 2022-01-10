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
for i in range(no_of_agents):
    if no_of_agents == 1:
        client.add_agent("{\"id\":" + str(9) + "}")  # 9 is an arbitrary choice
    else:
        client.add_agent("{\"id\":" + str(i) + "}")

parse.parse_server_info(client.get_pokemons(), client.get_agents(), client.get_graph())
drawer = GUI(parse)
Brain = Logic(parse)
client.start()

while client.is_running():
    parse.parse_server_info(client.get_pokemons(), client.get_agents(), client.get_graph())
    time_to_end = int(client.time_to_end())
    client_info = client.get_info().split(",")
    no_of_moves = client_info[2].split(":")[1]
    grade = client.get_info().split(",")
    grade = grade[3].split(":")[1]
    drawer.run_all_GUI(no_of_moves, int(time_to_end / 1000), grade, no_of_agents)
    print(time_to_end, client.get_info(), parse.agents[0].speed)
    if no_of_agents == 1:
        Brain.send_one_agent(client)
        client.move()
    else:
        for agent in parse.agents:
            Brain.send_some_agents(client)
            client.move()
            Brain.allocate_pokemon_to_agent(agent, client)
    time.sleep(0.008)
