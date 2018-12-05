import player
import random
import graphicsFunc
import logic
import copy
random.seed(11)
class PlayerL(player.Player):

	def __init__(self):
		super().__init__("Left")

	def initialHand(self, data):
		data.altMultL = 1 # starts adding from center and then outwards
		data.heightLeft = data.height / 2 - 15
		for i in range(1,14):
			self.addTile(data)
		self.reorganizeTiles(data)

	# returns the sequential hand order to check for melds after the current player
	def handOrder(self, data):
		return [data.B, data.R, data.T]

	# recenters tiles based on the number of tiles left in the hand
	def reorganizeTiles(self, data):
		newTiles = []
		data.heightLeft = data.height / 2 - 15
		tilesInd = 0
		for i in range(1, len(self.tiles) + 1):
			newTiles.append([ 1.3 * data.width / 10, data.heightLeft, self.tiles[tilesInd][2], False])
			data.heightLeft += 40 * data.altMultL * i # goes right then left then right...
			data.altMultL *= -1
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
		self.tiles.append([1.3 * data.width / 10, data.heightLeft, drawnTile, False])
		self.tileNames.append(drawnTile[1])
		# change position of next tile
		i = len(self.tiles)
		data.heightLeft += 40 * data.altMultL * i # goes right then left then right...
		data.altMultL *= -1


	# draws horizontal tile with hidden image
	def drawTiles(self, canvas, data):
		for piece in self.tiles:
			pX = piece[0]
			pY = piece[1]
			if data.mode == "win":
				# show the tile if it's a win
				graphicsFunc.threeDTile(canvas, pX, pY)
				img = piece[2][0]
			# show back of tile if you're a cpu or it's not your turn
			elif type(self) in data.cpus or type(data.turnOrder[data.turnInd]) != type(self):
				self.threeDTile(canvas, pX, pY)
				img = data.backHPng
			# must be your turn so show tile
			else:
				graphicsFunc.threeDTile(canvas, pX, pY)
				img = piece[2][0]
			canvas.create_image(pX, pY, image=img)

	# creates 3d appearing mahjong piece horizontally
	def threeDTile(self, canvas, pX, pY):
		canvas.create_rectangle(pX - 23, pY - 11, pX + 17, pY + 18,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 22, pY - 12, pX + 18, pY + 17,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 21, pY - 13, pX + 19, pY + 16,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 20, pY - 14, pX + 20, pY + 15,  fill ="white", width = 0)

	# draws all the melds at bottom
	def drawMelds(self, canvas, data):
		i = 0
		for piece in self.melds:
			pX = 35
			pY = 90 + 55 * i 
			graphicsFunc.threeDTile(canvas, pX, pY)
			canvas.create_image(pX, pY, image=piece[2][0])
			i += 1


