import pygame, random
import numpy as np
from pygame.locals import *

WHITE = (255, 255, 255)
COLOR = (200, 200, 200)

pygame.init()

TEXT_SIZE = 20
font = pygame.font.SysFont("arial", TEXT_SIZE)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("neverending")

pos = [SCREEN_HEIGHT // TEXT_SIZE // 2, SCREEN_WIDTH // TEXT_SIZE // 2]
cursor = "#"

def rnd_step(pos):
    next_pos = [pos[0], pos[1]]
    axis = random.randint(0,1)
    next_pos[axis] += (-1,1)[random.randint(0,1)]
    return tuple(next_pos)

def generate_map(pos):
    map = np.zeros((SCREEN_HEIGHT // TEXT_SIZE, SCREEN_WIDTH // TEXT_SIZE), dtype=str)
    map.fill("X")
    map[pos[0]][pos[1]] = cursor
    
    route = []
    route.append(pos)
    for i in range(500):
        route.append(rnd_step(route[-1]))

    for i in range(len(route)):
        try:
            map[route[i][0]][route[i][1]] = " "
        except:
            continue
    
    return map

map = generate_map(pos)

def make_step(next_pos, pos):
    traversal = False
    if next_pos[0] == -1 or next_pos[0] == 20 or next_pos[1] == -1 or next_pos[1] == 30: # defines border traversal
        traversal = True
        if next_pos[0] == -1: # to the top
            next_pos = (19, next_pos[1])
        elif next_pos[0] == 20: # to the bottom
            next_pos = (0, next_pos[1])
        elif next_pos[1] == -1: # to the left
            next_pos = (next_pos[0], 29)
        elif next_pos[1] == 30: # to the right
            next_pos = (next_pos[0], 0)
        if map[next_pos[0]][next_pos[1]] != " ": map[next_pos[0]][next_pos[1]] = " "
    if map[next_pos[0]][next_pos[1]] != " ": next_pos = pos
    return next_pos, traversal

while True:

    if map[pos[0]][pos[1]] != " ": map[pos[0]][pos[1]] = " "
    playground = map.copy()
    playground[pos[0]][pos[1]] = cursor
    screen.fill(COLOR)

    for y in range(map.shape[0]):
        for x in range(map.shape[1]):
            char = font.render(playground[y][x], True, (0,0,0))
            screen.blit(char, (x * TEXT_SIZE, y * TEXT_SIZE))

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                playground[pos[0]][pos[1]] = map[pos[0]][pos[1]]
                next_pos = (pos[0], pos[1]-1)
            elif event.key == K_RIGHT:
                playground[pos[0]][pos[1]] = map[pos[0]][pos[1]]
                next_pos = (pos[0], pos[1]+1)
            elif event.key == K_UP:
                playground[pos[0]][pos[1]] = map[pos[0]][pos[1]]
                next_pos = (pos[0]-1, pos[1])
            elif event.key == K_DOWN:
                playground[pos[0]][pos[1]] = map[pos[0]][pos[1]]
                next_pos = (pos[0]+1, pos[1])
            pos, traversal = make_step(next_pos, pos)
            try:
                if traversal: map = generate_map(rnd_step(pos))
            except:
                continue
                        
        pygame.display.update()