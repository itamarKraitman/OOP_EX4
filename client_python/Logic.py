import sys

from client_python.graph.GraphAlgo import GraphAlgo
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
        """
        this method allocate the agent to all pokemons, this method is called only when there only one agent is given from server
        this method uses allocate_pokemon method
        :param client:
        :return:
        """
        i = 0
        for agent in self.game.agents:
            if agent.dest == -1:
                path = self.allocate_pokemon(agent)
                while i < len(path):
                    client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(path[1]) + '}')
                    i += 1

    def send_some_agents(self, client: Client):
        """
        this method send each agent to correct pokemon in case more than one agent was given from server
        :param client:
        :return:
        """
        for pokemon in self.game.pokemons:
            self.select_agent(pokemon, client)


    def allocate_pokemon(self, agent):
        """
        this method organizes the path that the agent should pass in order to pick as much pokemons as possible,
        along side as mush score as possible
        :param agent:
        :return: rsult path: path of nodes
        """
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


    def select_agent(self, pokemon, client):
        """
        this method selects the right agent to allocate to the pokemon considering distance
        :param pokemon:
        :param client:
        :return:
        """
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
        """
        this method allocats to each pokemon the right agent
        :param agent:
        :param client:
        :return:
        """
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
