import pygame
import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from pygame.sprite import Sprite, collide_rect


vec = pygame.math.Vector2
FPS = 120

LIGHTGRAY = (100, 100, 100)

# 1. BLOCKS
BLOCK_SIZE = 50
Wall_List = []

# 2. MATRIX
matrix = np.loadtxt('matrix', dtype=int)
np.savetxt('matrix', matrix, fmt='%d', delimiter='')

# 4. LEVEL
with open("matrix") as MAP:
    LEVEL_1 = [line.strip() for line in MAP]

total_level_width = len(LEVEL_1[1]) * BLOCK_SIZE
total_level_height = len(LEVEL_1) * BLOCK_SIZE

# 2. WINDOW
RESOLUTION_X = total_level_width
RESOLUTION_Y = total_level_height
WINDOW_SIZE = (RESOLUTION_X, RESOLUTION_Y)

# 3. SCREEN
SCREEN_WIDTH = RESOLUTION_X
SCREEN_HEIGHT = int(RESOLUTION_Y)
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)






# with open("images/MAP.txt") as MAP:
#     data = MAP.readlines()
# def matrix_generator():  # Преобразование .txt файла в двумерный список [[0,0,0],[1,1,1], .....]
#     for i in range(len(data)):
#         data[i] = list(map(int, data[i].strip()))
#     return data
# matrix = np.loadtxt('matrix', dtype=int)
# np.savetxt('matrix', matrix, fmt='%d', delimiter='')
# matrix = np.loadtxt('matrix', dtype=int)


# NEXT
# np.savetxt('matrix', matrix, fmt='%d', delimiter='')
# c = np.loadtxt('matrix', dtype=int)
# print(c)