# Player.py contains the object Player, with all the actions a player can do and their tiles

import random
import logic
import assist

class Player(object):

	discPile = []

	def __init__(self, name):
		self.name = name
		self.tiles = []
		self.melds = []
		self.discarded = []
		self.highlighted = None
		self.tileNames = []
		self.winningTiles = []
		self.lastDrawnTileName = None
		self.recTiles = []

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

	# returns True if you can chow the tile that is thrown out, sets the chow tiles that you can chow
	def canChow(self, data, discTile):
		discName = discTile[2][1]
		if discName[0] not in "123456789":
			return False
		minusTwo = str(int(discName[0]) - 2) +  discName[1:]
		minusOne = str(int(discName[0]) - 1) +  discName[1:]
		plusOne = str(int(discName[0]) + 1) +  discName[1:]
		plusTwo = str(int(discName[0]) + 2) +  discName[1:]
		m2 = None
		m1 = None
		p1 = None
		p2 = None
		for tile in self.tiles:
			if tile[2][1] == minusTwo:
				m2 = tile
			elif tile[2][1] == minusOne:
				m1 = tile
			elif tile[2][1] == plusOne:
				p1 = tile
			elif tile[2][1] == plusTwo:
				p2 = tile
		if m2 != None and m1 != None:
			data.firstChowTile = m2
			data.secondChowTile = m1
			return True
		elif m1 != None and p1 != None:
			data.firstChowTile = m1
			data.secondChowTile = p1
			return True
		elif p1 != None and p2 != None:
			data.firstChowTile = p1
			data.secondChowTile = p2
			return True
		return False

	# discards the chosen tile, checking for other hands' potentially using it for melds in order
	def discardTile(self, data, handOrder):
		if data.mode != "moving":
			if self.highlighted == None:
				print("You can't discard if you didn't choose a tile!")
				return
			removed = self.tiles.pop(self.highlighted)
			self.highlighted = None
			data.curRemoved = removed
			data.widthIncr = (data.width / 2 - data.curRemoved[0]) / 4
			data.heightIncr = (data.height / 2 - data.curRemoved[1]) / 4
			data.mode = "moving"

	# continue after discarding tile and after the subsequent moving animation
	def discardTileAfterAni(self, data, handOrder, removed):
		self.discarded.append(removed)
		data.discPile.append(removed)
		self.tileNames.remove(removed[2][1])
		# update winning tiles everytime a tile is discarded
		self.winningTiles = logic.winningTiles(data.imageNames, self)
		meldsAndTiles = self.melds + self.tiles
		meldsAndTilesNames = []
		for tile in meldsAndTiles:
			meldsAndTilesNames.append(tile[2][1])
		# check if anyone can win with the tile
		for hand in handOrder:
			if removed[2][1] in hand.winningTiles:
				hand.tiles.append(removed)
				hand.tileNames.append(removed[2][1])
				print("Won from someone else's tile!")
				print("Loser: " + self.name)
				data.loser = " " + self.name + " lost."
				assist.sortTiles(data, self)
				data.winner = hand.name
				data.winningHand = hand.melds + hand.tiles
				winningHandNames = []
				for tile in data.winningHand:
					winningHandNames.append(tile[2][1])
				data.handSco = logic.handScore(data, winningHandNames)
				print("Hand Score: " + str(data.handSco[0]))
				print(winningHandNames)
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
