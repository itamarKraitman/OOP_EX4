import sys

from GraphAlgo import GraphAlgo
from Parser import Parser
from client import Client
import time

EPS = 0.0000001

"""
The following function receives a single agent
 and knows how to go through all the Pokemon and 
 send the agent to the appropriate Pokemon
"""


class Logic:

    def __init__(self, game: Parser()):
        self.game = game
        self.client = Client()
        self.inf = sys.maxsize

    def one_agent(self, client: Client, t):
        go_to = []

        for agent in self.game.agents:
            if agent.dest == -1:
                go_to = self.pick_pok(agent)
                for i in go_to:
                    client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(go_to[1]) + '}')

        if t == 1:
            if len(go_to) <= 2:
                if self.game.agents[0].speed >= 3:
                    time.sleep(0.02)
                else:
                    time.sleep(0.02)
            else:
                if self.game.agents[0].speed <= 3:
                    time.sleep(0.75)
                else:
                    time.sleep(0.35)

        else:
            if len(go_to) <= 2:
                if self.game.agents[0].speed >= 2:
                    time.sleep(0.035)
                else:
                    time.sleep(0.035)
            else:
                if self.game.agents[0].speed <= 2:
                    time.sleep(0.4)
                else:
                    time.sleep(0.085)

    # //////////////////////////////////////////////////////////////

    def pick_pok(self, agent):
        graph = self.game.graph
        graph_algo = GraphAlgo(graph)
        pick = []
        res = []
        min = 0
        i = 0
        max = 0
        p = None
        for pok in self.game.pokemons:
            max += 1

        for pok in self.game.pokemons:
            if pok.mode == 0:

                if pok.src is None or agent.src is None:
                    pok.src = 7
                    pok.dest = 6

                s = graph_algo.shortest_path(agent.src, pok.src)
                # t = GA.shortest_path(pok.src,pok.dest)
                pick = s[0], s[1], pok.value

                w = (pok.value / (s[0] + 1))

                if min < w:
                    min = w
                    res = pick[1]
                    p = pok
                    i += 1
                    if i < max:
                        continue
        res.append(p.dest)
        return res

    """
    The next function gets more than one 
    agent and goes through all the Pokemon
     in order to match each Pokemon with the 
     appropriate agent, as opposed to the function above
    """

    # ////////////////////////////////////////////more then one/////////////////////////////////////////////////////////

    def multiple_agents(self, client: Client, t):
        pick = []
        for pok in self.game.pokemons:
            pick = self.pick_age(pok, client, t)

        age = None
        speed = 0
        min = 0
        # min = float('inf')
        for agent in self.game.agents:
            speed = agent.speed
            if speed > min:
                min = speed
                age = agent

        if len(pick) <= 2:
            if min >= 3:
                time.sleep(0.035)
            else:
                time.sleep(0.035)
        else:
            if min <= 3:
                time.sleep(0.12)
            else:
                time.sleep(0.03)

    def pick_age(self, pokemon, client, t):
        if pokemon.mode == 0:
            pokemon.mode = 1
            G = self.game.graph
            GA = GraphAlgo(G)
            pick = []
            res = []
            min = 0
            i = 0
            max = 0
            a = None

            for AG in self.game.agents:
                max += 1

            for agent in self.game.agents:
                s = GA.shortest_path(agent.src, pokemon.src)
                pick = s[0], s[1], pokemon.value

                w = (pokemon.value / (s[0] + 1)) * agent.speed

                if min < w:
                    min = w
                    res = pick[1]
                    a = agent
                    res[0] = a.id
                    res.append(pokemon.dest)
                    i += 1
                    if i < max:
                        continue

            client.choose_next_edge(
                '{"agent_id":' + str(res[0]) + ', "next_node_id":' + str(res[1]) + '}')

            for agent in self.game.agents:
                if agent == a:
                    agent.mode = 1
            return res

    def pick_pok_for_A(self, agent, client):
        graph = self.game.graph
        graph_algo = GraphAlgo(graph)
        pick = []
        res = []
        min = 0
        i = 0
        max = 0
        p = None
        for pok in self.game.pokemons:
            if pok.mode == 0:
                max += 1

        for pok in self.game.pokemons:

            if pok.src == None or agent.src == None:
                pok.src = 7
                pok.dest = 6

            s = graph_algo.shortest_path(agent.src, pok.get_src())
            # t = GA.shortest_path(pok.src,pok.dest)
            pick = s[0], s[1], pok.value

            w = (pok.value / (s[0] + 1))

            if min < w:
                min = w
                res = pick[1]
                p = pok
                i += 1
                if i < max:
                    continue
        res.append(p.dest)
        for pok in self.game.pokemons:
            if pok == p:
                pok.mode = 1
                client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(res[1]) + '}')
