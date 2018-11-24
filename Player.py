# Player.py contains the object Player, with all the actions a player can do and their tiles

import random
class Player(object):
	def __init__(self, tiles):
		self.tiles = tiles
		self.melds = []
		self.discarded = []

	# draws a tile from the available tiles
	def drawTile(self, availableTiles):
		tileIndex = random.randint(0, len(availableTiles) - 1)
		drawnTile = availableTiles.pop(tileIndex)
		self.tiles.append(drawnTile)

	# discards the chosen tile
	def discardTile(self, chosenTileIndex):
		discTile = self.tiles.pop(chosenTileIndex)
		self.discarded.append(discTile)

	# takes three tiles from hand and makes it a meld
	def makeMeld(self, tileInd0, tileInd1, tileInd2):
		# loop through the indexes in reversed order to not interfere with loopwhen popping
		# idea from https://stackoverflow.com/questions/11303225/how-to-remove-multiple-indexes-from-a-list-at-the-same-time/41097792
		sortedInd = sorted([tileInd0, tileInd1, tileInd2], reverse = True)
		poppedLst = []
		for ind in sortedInd:
			poppedLst.append(self.tiles.pop(ind))
		for element in poppedLst:
			self.melds.append(element)

	


