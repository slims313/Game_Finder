import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from pygame.sprite import Sprite, collide_rect


vec = pygame.math.Vector2
# FPS
FPS = 120

LIGHTGRAY = (100, 100, 100)

# WINDOW
RESOLUTION_X = 1000
RESOLUTION_Y = 1000
WINDOW_SIZE = (RESOLUTION_X, RESOLUTION_Y)

# SCREEN
SCREEN_WIDTH = RESOLUTION_X
SCREEN_HEIGHT = int(RESOLUTION_Y)
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
# print(SCREEN_SIZE)


# BLOCKS
BLOCK_SIZE = 50
# OBJECTS
# Movement
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

PLAYER_ROT_SPEED = 20
PLAYER_SPEED = 40
PLAYER_HIT_RECT = pygame.Rect(0, 0, 35, 35)

Wall_List = []


def matrix_generator():  # Преобразование .txt файла в двумерный список [[0,0,0],[1,1,1], .....]
    with open("images/MAP.txt") as MAP:
        data = MAP.readlines()
    for i in range(len(data)):
        data[i] = list(map(int, data[i].strip()))
    return data

matrix = matrix_generator()
a = matrix

