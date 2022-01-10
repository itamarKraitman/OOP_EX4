import time
from asyncio import events
from pygame import gfxdraw
from pygame import *
from Parser import *
import pygame
from client import *
from pygame.locals import *
from pygame_widgets.button import Button

pygame.init()
pygame.font.init()
pygame.mixer.init()
client = Client()

# defining some useful attributes
WIDTH, HEIGHT = 1080, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (250, 0, 0)
BLUE = (0, 0, 255)
R = 15

# init the screen and the fonts
clock = pygame.time.Clock()
FONT = pygame.font.SysFont('Arial', 20, bold=True)
pygame.font.init()
pygame.display.set_caption("Pokemon Game")
fmove = pygame.font.SysFont('comicsans', 20)
end_game_font = pygame.font.SysFont('comicsans', 55, bold=True)


def scale(data, min_screen, max_screen, min_data, max_data):
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


def my_scale(screen, min_x, max_x, min_y, max_y, data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


balbazor = pygame.transform.scale(pygame.image.load("pic_for_ex5/balbazor.jpg"), (50, 50))
picatcu = pygame.transform.scale(pygame.image.load("pic_for_ex5/picatcu.png"), (50, 50))
unknown_pokemon = pygame.transform.scale(pygame.image.load("pic_for_ex5/pokemon.jpg"), (50, 50))
pokemons_list = (balbazor, picatcu, unknown_pokemon)

brock = pygame.transform.scale(pygame.image.load("pic_for_ex5/brock.jpg"), (60, 60))
ash = pygame.transform.scale(pygame.image.load("pic_for_ex5/ash.png"), (60, 60))
misty = pygame.transform.scale(pygame.image.load("pic_for_ex5/misty.jpg"), (60, 60))
agents_list = (brock, ash, misty)

background = pygame.transform.scale(pygame.image.load("pic_for_ex5/arena.jpg"), (WIDTH, HEIGHT))


class GUI:

    def __init__(self, game: Parser()):
        self.pokemon_game = game
        self.graph = self.pokemon_game.graph
        self.screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        self.button_stop = Button(self.screen, 0, 0, 200, 40, text='Stop Game', inactiveColour=RED,
                                  hoverColour=BLACK, font=pygame.font.SysFont('calibri', 30))
        self.min_x = float('inf')
        self.max_x = float('-inf')
        self.min_y = float('inf')
        self.max_y = float('-inf')
        self.define_min_max()

    def define_min_max(self):
        for n in self.graph.nodes.values():
            x = n.pos[0]
            y = n.pos[1]
            self.min_x = min(self.min_x, x)
            self.min_y = min(self.min_y, y)
            self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)

    def drawing_graph(self):
        for n in self.graph.nodes.values():
            x = my_scale(self.screen, self.min_x, self.max_x, self.min_y, self.max_y, n.pos[0], x=True)
            y = my_scale(self.screen, self.min_x, self.max_x, self.min_y, self.max_y, n.pos[1], y=True)
            gfxdraw.filled_circle(self.screen, int(x), int(y), R, Color(64, 80, 174))
            gfxdraw.aacircle(self.screen, int(x), int(y), R, Color(255, 255, 255))
            id_srf = FONT.render(str(n.key), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            self.screen.blit(id_srf, rect)
        for src in self.graph.edges:
            for dest in self.graph.edges.get(src):
                sx = my_scale(self.screen, self.min_x, self.max_x, self.min_y, self.max_y,
                              self.graph.get_node(src).pos[0], x=True)
                sy = my_scale(self.screen, self.min_x, self.max_x, self.min_y, self.max_y,
                              self.graph.get_node(src).pos[1], y=True)
                dx = my_scale(self.screen, self.min_x, self.max_x, self.min_y, self.max_y,
                              self.graph.get_node(dest).pos[0], x=True)
                dy = my_scale(self.screen, self.min_x, self.max_x, self.min_y, self.max_y,
                              self.graph.get_node(dest).pos[1], y=True)
                pygame.draw.line(self.screen, Color(WHITE), (sx, sy), (dx, dy), width=5)

    def draw_agents_pokemons(self, number_of_agents: int):
        agents = self.pokemon_game.agents
        pokemons = self.pokemon_game.pokemons
        i = 0
        for agent in agents:
            x, y = agent.pos[0], agent.pos[1]
            x = my_scale(self.screen, self.min_x, self.max_x, self.min_y, self.max_y, float(x), x=True)
            y = my_scale(self.screen, self.min_x, self.max_x, self.min_y, self.max_y, float(y), y=True)
            self.screen.blit(pygame.transform.scale(agents_list[i], (50, 50)), (int(x), int(y)))
            i += 1
        i = 0
        for pokemon in pokemons:
            x, y = pokemon.pos[0], pokemon.pos[1]
            x = my_scale(self.screen, self.min_x, self.max_x, self.min_y, self.max_y, float(x), x=True)
            y = my_scale(self.screen, self.min_x, self.max_x, self.min_y, self.max_y, float(y), y=True)
            self.screen.blit(pokemons_list[i], (int(x) - 25, int(y) - 25))
            i += 1
            if i == len(pokemons_list):
                i = 0


    # def draw_ttl(self, ttl: int):
    #     number_of_move = fmove.render("Time to live: " + str(ttl) + " second", True, WHITE)
    #     self.screen.blit(number_of_move, (10, self.screen.get_height() - 30))

    def draw_grade(self, grade: int):
        number_of_move = fmove.render("Grade: " + str(grade), True, YELLOW)
        self.screen.blit(number_of_move, (self.screen.get_width() - 110, 10))

    def main(self, move, time_out, grade, number_of_agents):
        self.screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_stop.clicked(event):
                    pygame.quit()
                    exit(0)
        if time_out == 0:
            self.screen.fill(BLACK)
            game_end = end_game_font.render("GAME OVER !", True, RED)
            button_text = end_game_font.render("Results: your grade is - " + grade, True, WHITE)
            self.screen.blit(game_end, (self.screen.get_width() / 3, 10))
            self.screen.blit(button_text, (self.screen.get_width() / 6.3, self.screen.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(5000)
            pygame.quit()
            exit(0)

        self.screen.fill(BLACK)
        back = pygame.transform.scale(pygame.image.load("pic_for_ex5/arena.jpg"),
                                      (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(back, [0, 0])
        number_of_move = fmove.render("Moves so far: " + str(move), True, BLACK)
        self.screen.blit(number_of_move, (10, self.screen.get_height() - 30))
        number_of_move = fmove.render("Time to live: " + str(time_out) + " second", True, BLUE)
        self.screen.blit(number_of_move, (self.screen.get_width() - 222, self.screen.get_height() - 30))
        self.drawing_graph()
        self.draw_agents_pokemons(number_of_agents=number_of_agents)
        number_of_move = fmove.render("Grade: " + str(grade), True, YELLOW)
        self.screen.blit(number_of_move, (self.screen.get_width() - 110, 10))
        self.button_stop.draw()
        display.update()
        clock.tick(10)
