import sys

from GraphAlgo import GraphAlgo
from Parser import Parser
from client import Client

EPS = 0.0000001

class Logic:

    def __init__(self, game: Parser()):
        self.game = game
        self.client = Client()
        self.inf = sys.maxsize
        self.graph = self.game.graph
        self.graph_algo = GraphAlgo(self.graph)

    def send_one_agent(self, client: Client):
        i = 0
        # one agent
        for agent in self.game.agents:
            if agent.dest == -1:
                path = self.allocate_pokemon(agent)
                while i < len(path):
                    client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(path[1]) + '}')
                    i += 1

    def send_some_agents(self, client: Client):
        # multiple agents
        for pokemon in self.game.pokemons:
            self.select_agent(pokemon, client)
        #     age = None
        #     speed = 0
        #     min = 0
        # # min = float('inf')
        #     for agent in self.game.agents:
        #         speed = agent.speed
        #         if speed > min:
        #             min = speed
        #             age = agent

        # if t == 1:
        #     if len(go_to) <= 2:
        #         if self.game.agents[0].speed >= 3:
        #             time.sleep(0.02)
        #         else:
        #             time.sleep(0.02)
        #     else:
        #         if self.game.agents[0].speed <= 3:
        #             time.sleep(0.75)
        #         else:
        #             time.sleep(0.35)
        #
        # else:
        #     if len(go_to) <= 2:
        #         if self.game.agents[0].speed >= 2:
        #             time.sleep(0.035)
        #         else:
        #             time.sleep(0.035)
        #     else:
        #         if self.game.agents[0].speed <= 2:
        #             time.sleep(0.4)
        #         else:
        #             time.sleep(0.085)

    def allocate_pokemon(self, agent):
        min_weight = 0
        selected_pokemon = None
        result_path = []
        for pokemon in self.game.pokemons:
            if pokemon.allocated == 0:
                dist, path = self.graph_algo.shortest_path(agent.src, pokemon.src)
                weight = (pokemon.value / (dist + 1))
                if min_weight < weight:
                    min_weight = weight
                    result_path = path
                    selected_pokemon = pokemon
        result_path.append(selected_pokemon.dest)
        return result_path

    # ////////////////////////////////////////////more then one/////////////////////////////////////////////////////////

    # def multiple_agents(self, client: Client, t):
    #     pick = []
    #     for pok in self.game.pokemons:
    #         pick = self.pick_age(pok, client, t)
    #
    #     age = None
    #     speed = 0
    #     min = 0
    #     # min = float('inf')
    #     for agent in self.game.agents:
    #         speed = agent.speed
    #         if speed > min:
    #             min = speed
    #             age = agent

        # if len(pick) <= 2:
        #     if min >= 3:
        #         time.sleep(0.035)
        #     else:
        #         time.sleep(0.035)
        # else:
        #     if min <= 3:
        #         time.sleep(0.12)
        #     else:
        #         time.sleep(0.03)

    def select_agent(self, pokemon, client):
        if pokemon.allocated == 0:
            pokemon.allocated = 1
            path_result = None
            min_weight = 0
            agent_to_pick = None
            for agent in self.game.agents:
                dist, path = self.graph_algo.shortest_path(agent.src, pokemon.src)
                weight = (pokemon.value / (dist + 1)) * agent.speed
                if min_weight < weight:
                    min_weight = weight
                    path_result = path
                    path_result.append(pokemon.dest)
                    agent_to_pick = agent.id
                    path_result.append(pokemon.dest)
            client.choose_next_edge('{"agent_id":' + str(agent_to_pick) + ', "next_node_id":'
                                            + str(path_result[1]) + '}')
            for agent in self.game.agents:
                if agent == agent_to_pick:
                    agent.mode = 1


    def allocate_pokemon_to_agent(self, agent, client):
        result_path = []
        min_weight = 0
        selected_pokemon = None
        for pokemon in self.game.pokemons:
            dist, path = self.graph_algo.shortest_path(agent.src, pokemon.get_src())
            weight = (pokemon.value / (dist + 1))
            if min_weight < weight:
                min_weight = weight
                result_path = path
                selected_pokemon = pokemon
        result_path.append(selected_pokemon.dest)
        for pok in self.game.pokemons:
            if pok == selected_pokemon:
                pok.mode = 1
                client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(result_path[1]) + '}')
