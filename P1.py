import Player
import random

class CPU(Player):
	def __init__(self, tiles):
		super().__init__(tiles)

	# choose discard tile index based on "AI", currently is random
	def chooseDiscInd(self):
		discardInd = random.randint(0, len(tiles) - 1)
		self.discardTile(discardInd)



