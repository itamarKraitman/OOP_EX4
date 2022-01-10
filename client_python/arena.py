import json

from pygame import gfxdraw
from pygame import *
from pygame_widgets import button
from pygame_widgets.button import Button
import graph
import pygame
from client import *
from pygame.locals import *

pygame.font.init()
pygame.mixer.init()


def scale(data, min_screen, max_screen, min_data, max_data):
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


# define some useful colors
WIDTH, HEIGHT = 1080, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (250, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
R = 15

pygame.init()
client = Client()
graph_load = graph.Graph()

# define some useful fonts
FONT = pygame.font.SysFont('Arial', 20, bold=True)
font_move = pygame.font.SysFont('comicsans', 20)
game_over_font = pygame.font.SysFont('comicsans', 40)  # to present the game is over
pygame.font.init()

# define screen attributes
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("Pokemon - catch 'em all!!")
pygame.transform.scale(pygame.image.load("../pic_for_ex5/arena.jpg"), (screen.get_width(), screen.get_height()))

# defining some pokemons and agents pictures in order to make the GUI look better
picatcu = pygame.transform.scale(pygame.image.load("../pic_for_ex5/picatcu.png"), (40, 40))
chram = pygame.transform.scale(pygame.image.load("../pic_for_ex5/chramander.jpg"), (40, 40))
balbazure = pygame.transform.scale(pygame.image.load("../pic_for_ex5/balbazor.jpg"), (40, 40))
pokemons = [picatcu, chram, balbazure]
ash = pygame.transform.scale(pygame.image.load("../pic_for_ex5/ash.png"), (40, 40))
misty = pygame.transform.scale(pygame.image.load("../pic_for_ex5/misty.jpg"), (40, 40))
brock = pygame.transform.scale(pygame.image.load("../pic_for_ex5/brock.jpg"), (40, 40))
agents_list = [ash, misty, brock]

# getting min's & max's for scaling
min_x = float('inf')
min_y = float('inf')
max_y = float('-inf')
max_x = float('-inf')
for node in graph_load.nodes:
    X = node.get_x()
    Y = node.get_y()
    min_x = min(min_x, X)
    min_y = min(min_y, Y)
    max_x = max(max_x, X)
    max_y = max(max_y, Y)

# scaling nodes
# nodes
for node in graph_load.nodes:
    x = my_scale(node.get_x(), x=True)
    y = my_scale(node.get_y(), y=True)
    node.setPosition(x, y, 0)
# edges src and dest was scaled above when scaling nodes

button_stop = Button(screen, 0, 0, 200, 40, text='Stop Game', inactiveColour=(255, 255, 255),
                         hoverColour=(255, 192, 203), font=pygame.font.SysFont('calibri', 30))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_stop.clicked(event.pos):
                pygame.quit()
                exit(0)
    info_data = json.loads(client.get_info())
    screen.blit(FONT.render('Score: ' + str(info_data["GameServer"]["grade"]), False, (0, 0, 0)), (0, 40))
    screen.blit(
        FONT.render('Time to end: ' + str(int(client.time_to_end()) // 1000) + ' sec', False, (0, 0, 0)),
        (0, 60))
    screen.blit(FONT.render('Moves: ' + str(info_data["GameServer"]["moves"]), False, (0, 0, 0)), (0, 80))
    button_stop.draw()
    # drawing nodes
    for node in graph_load.nodes:
        X = node.get_x()
        Y = node.get_y()
        gfxdraw.filled_circle(screen, int(X), int(Y), R, RED)
        gfxdraw.aacircle(screen, int(X), int(Y), R, WHITE)
        id_str = FONT.render(str(node.getKey()), True, WHITE)
        rect = id_str.get_rect(center=(X, Y))
        screen.blit(id_str, rect)

    # drawing edges
    for edge in graph_load.edges.keys():
        src = graph_load.get_node(edge.getSrc())
        dest = graph_load.get_node(edge.getDest())
        sx = my_scale(src.get_x(), x=True)
        sy = my_scale(src.get_y(), y=True)
        dx = my_scale(dest.get_x(), x=True)
        dy = my_scale(dest.get_y(), y=True)
        pygame.draw.line(screen, RED, (sx, sy), (dx, dy), width=5)

    # drawing agents
    agents = client.get_agents()
    for agent in agents:
        x, y = agent.pos[0], agent.pos[1]
        x = my_scale(float(x), x=True)
        y = my_scale(float(y), y=True)
        for i in range(agents):
            screen.blit(agents_list[i], (int(x) - 21, int(y) - 21))

    # drawing pokemons
    pokemons = client.get_pokemons()
    i = 0
    for pokemon in pokemons:
        x, y = pokemon.pos[0], pokemon.pos[1]
        x = my_scale(float(x), x=True)
        y = my_scale(float(y), y=True)
        screen.blit(pokemons[i], (int(x) - 18, int(y) - 18))

    # drawing stop button

    # drawing timer
    time_to_end = client.time_to_end()
    number_of_move = font_move.render("timer:" + str(time_to_end) + " second", True,
                                      WHITE)
    screen.blit(number_of_move, (10, screen.get_height() - 30))

    if time_to_end == 0:
        game_over = game_over_font.render("GAME OVER !", True, game_over_font)
    # button_text = game_over_font.render("Results: your grade is - " + grade,True,WHITE)
        screen.blit(game_over, (screen.get_width() / 3, 10))
    # .screen.blit(button_text,
    #              (.screen.get_width() / 6.3,.screen.get_height() / 2))
        pygame.display.update()
        # pygame.time.delay(5000)
pygame.quit()
exit(0)

