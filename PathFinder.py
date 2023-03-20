from Windows import *


class Pathfinder:
	def __init__(self, matrix):

		# setup
		self.matrix = matrix
		self.grid = Grid(matrix=a)

		# pathfinding
		self.path = []
