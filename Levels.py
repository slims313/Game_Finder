from Groups import *

cell_X = 0
cell_Y = 0


for row in LEVEL_1:
    for col in row:
        if col == '0':
            Wall_List.append([cell_X, cell_Y])
        cell_X += 1
    cell_Y += 1
    cell_X = 0

np.savetxt('matrix', matrix, fmt='%d', delimiter=' ')