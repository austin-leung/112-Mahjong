# Player.py contains the object Player, with all the actions a player can do and their tiles

import random
import logic
class Player(object):

	discPile = []

	def __init__(self, name):
		self.name = name
		self.tiles = []
		self.melds = []
		self.discarded = []
		self.highlighted = None
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
		if discName[0] not in "123456789":
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



	# discards the chosen tile, checking for other hands' potentially using it for melds in order
	def discardTile(self, data, handOrder):
		if self.highlighted == None:
			print("You can't discard if you didn't choose a tile!")
			return
		removed = self.tiles.pop(self.highlighted)
		self.discarded.append(removed)
		data.discPile.append(removed)
		self.tileNames.remove(removed[2][1])
		self.highlighted = None
		# check if anyone can win with the tile
		for hand in handOrder:
			if removed[2][1] in logic.winningTiles(data.imageNames, hand.tileNames):
				hand.tiles.append(removed)
				hand.tileNames.append(removed[2][1])
				print("should win")
				data.winner = hand.name
				data.winningHand = hand.melds + hand.tiles
				data.mode = "win"
				return
		# check if anyone can pong or chow the tile
		for hand in handOrder:
			if hand.canPong(data, removed):
				data.pongOptHand = hand
				data.pongOptTile = removed
				data.mode = "pong"
			if hand.canChow(data, removed):
				data.chowOptHand = hand
				data.chowOptTile = removed
				data.mode = "chow"


	


