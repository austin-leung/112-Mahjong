import player
import random
import graphicsFunc

class PlayerT(player.Player):

	def initialHand(self, data):
		data.widthTop = data.width / 2
		data.altMultT = 1
		for i in range(1,14):
			self.addTile(data)
		self.reorganizeTiles(data)


	def reorganizeTiles(self, data):
		newTiles = []
		data.widthTop = data.width / 2
		tilesInd = 0
		for i in range(1, len(self.tiles) + 1):
			newTiles.append([data.widthTop, 1.5 * data.height / 12, self.tiles[tilesInd][2], False])
			data.widthTop += 40 * data.altMultT * i
			data.altMultT *= -1
			tilesInd += 1
		self.tiles = newTiles

	# draws a tile from the available tiles
	def addTile(self, data):
		randInd = random.randint(0, len(data.drawPile) - 1)
		drawnTile = data.drawPile.pop(randInd)
		# draw another tile for flowers and seasons
		if drawnTile[1][0] == "s" or drawnTile[1][0] == "f":
			self.melds.append([None, None, drawnTile, False])
			self.addTile(data)
			return
		# add new tile at corresponding position
		self.tiles.append([data.widthTop, 1.2 * data.height / 12, drawnTile, False])
		# change position of next tile
		i = len( self.tiles)
		data.widthTop += 40 * data.altMultT * i
		data.altMultT *= -1

	# discards the chosen tile
	def discardTile(self, data):
		removed = self.tiles.pop(self.highlightedPieces[0])
		self.discarded.append(removed)
		PlayerT.discPile.append(removed)
		self.highlightedPieces = []
		for hand in [data.L, data.B, data.R]:
			if hand.canPong(data, removed):
				data.pongOptHand = hand
				data.pongOptTile = removed
				data.mode = "pong"
				return
			if hand.canChow(data, removed):
				data.chowOptHand = hand
				data.chowOptTile = removed
				data.mode = "chow"
				return

	# creates 3d appearing mahjong piece with red background in front
	def drawTiles(self, canvas, data):
		for piece in self.tiles:
			pX = piece[0]
			pY = piece[1]
			self.threeDTile(canvas, pX, pY)
			canvas.create_image(pX, pY, image=piece[2][0])

	# creates 3d appearing mahjong piece without red 
	def threeDTile(self, canvas, pX, pY):
		canvas.create_rectangle(pX - 11, pY - 23, pX + 18, pY + 17,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 12, pY - 22, pX + 17, pY + 18,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 13, pY - 21, pX + 16, pY + 19,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 14, pY - 20, pX + 15, pY + 20,  fill ="white", width = 0)

	# draws all the melds at bottom
	def drawMelds(self, canvas, data):
		i = 0
		for piece in self.melds:
			pX = 75 + 45 * i
			pY = 35
			graphicsFunc.threeDTile(canvas, pX, pY)
			canvas.create_image(pX, pY, image=piece[2][0])
			i += 1

