import random
class Player(object):
	def __init__(self):
		self.tiles = []
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
		meldTile0 = self.tiles.pop(tileInd0)
		meldTile1 = self.tiles.pop(tileInd1)
		meldTile2 = self.tiles.pop(tileInd2)
		self.melds.append()

