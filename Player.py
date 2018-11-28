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
		self.tileNames = []

	# returns True if you can pong the tile that is thrown out
	def canPong(self, data, discTile):
		tileFreq = 0
		ind = 0
		for myTile in self.tiles:
			if discTile[2][1] == myTile[2][1]:
				tileFreq += 1
				if tileFreq == 1:
					data.firstPongTile = myTile
			if tileFreq == 2:
				data.secondPongTile = myTile
				return True
			ind += 1
		return False

	# returns True if you can chow the tile that is thrown out
	def canChow(self, data, discTile):
		discName = discTile[2][1]
		if discName[0] not in "0123456789":
			return False
		minusTwo = str(int(discName[0]) - 2) +  discName[1:]
		minusOne = str(int(discName[0]) - 1) +  discName[1:]
		plusOne = str(int(discName[0]) + 1) +  discName[1:]
		plusTwo = str(int(discName[0]) + 2) +  discName[1:]
		b1 = False
		b2 = False
		for myTile in self.tiles:
			if myTile[2][1] == minusTwo:
				b1 = True
				data.firstChowTile = myTile
			if myTile[2][1] == minusOne:
				b2 = True
				data.secondChowTile = myTile
		if b1 and b2:
			return True
		b3 = False
		b4 = False
		for myTile in self.tiles:
			if myTile[2][1] == minusOne:
				b3 = True
				data.firstChowTile = myTile
			if myTile[2][1] == plusOne:
				b4 = True
				data.secondChowTile = myTile
		if b3 and b4:
			return True
		b5 = False
		b6 = False
		for myTile in self.tiles:
			if myTile[2][1] == plusOne:
				b5 = True
				data.firstChowTile = myTile
			if myTile[2][1] == plusTwo:
				b6 = True
				data.secondChowTile = myTile
		if b5 and b6:
			return True
		return False

	# takes three tiles from hand and makes it a meld
	def makeMeld(self, tileInd0, tileInd1, tileInd2):
		# loop through the indexes in reversed order to not interfere with loop when popping
		# idea from https://stackoverflow.com/questions/11303225/how-to-remove-multiple-indexes-from-a-list-at-the-same-time/41097792
		sortedInd = sorted([tileInd0, tileInd1, tileInd2], reverse = True)
		poppedLst = []
		for ind in sortedInd:
			poppedLst.append(self.tiles.pop(ind))
		for element in poppedLst:
			self.melds.append(element)
			self.tileNames.remove(element)




	


