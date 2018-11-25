# Player.py contains the object Player, with all the actions a player can do and their tiles

import random
class Player(object):

	discPile = []

	def __init__(self, tiles, name):
		self.name = name
		self.tiles = []
		self.melds = []
		self.discarded = []
		self.highlightedPieces = []


	# draws a tile from the available tiles
	"""
	def drawTile(self, availableTiles):
		tileIndex = random.randint(0, len(availableTiles) - 1)
		drawnTile = availableTiles.pop(tileIndex)
		self.tiles.append(drawnTile)"""

	# def setTiles(self):
	# 	altMult = 1
	# 	for i in range(1,len(self.tiles) + 1):
	# 		# right player
	# 		self.tiles.append([8.5 * data.width / 10, heightRight, data.drawPile[randInd], False])
	# 		heightRight += 40 * altMult * i
	# 		altMult *= -1
	# 		data.drawPile.pop(randInd)

	# discards the chosen tile
	def discardTile(self):
		self.tiles.remove(self.highlightedPieces[0])
		self.discarded.append(self.highlightedPieces[0])
		Player.discPile.append(self.highlightedPieces[0])
		self.highlightedPieces = []



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


	


