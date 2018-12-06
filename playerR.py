# playerR.py contains methods for the right player specifically

import player
import random
import graphicsFunc
import logic
import copy
import assist
random.seed(11)
class PlayerR(player.Player):

	def __init__(self):
		super().__init__("Right")

	def initialHand(self, data):
		data.heightRight = data.height / 2 - 15
		data.altMultR = 1
		for i in range(1,14):
			self.addTile(data)
		self.reorganizeTiles(data)

	# returns the sequential hand order to check for melds after the current player
	def handOrder(self, data):
		return [data.T, data.L, data.B]

	# recenters tiles based on the number of tiles left in the hand
	def reorganizeTiles(self, data):
		newTiles = []
		data.heightRight = data.height / 2 - 15 - 40 * (len(self.tiles) // 2)
		tilesInd = 0
		for i in range(1, len(self.tiles) + 1):
			newTiles.append([8.7 * data.width / 10, data.heightRight, self.tiles[tilesInd][2], False])
			data.heightRight += 40
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
		self.tiles.append([8.7 * data.width / 10, data.heightRight, drawnTile, False])
		self.tileNames.append(drawnTile[1])
		self.lastDrawnTileName = drawnTile[1]
		if data.assistMode == True:
			if data.meldsFirst == True:
				assist.sortTilesMeld(data, self)
			else:
				# sort normally
				assist.sortTiles(data, self)

	# draws horizontal tile with hidden image
	def drawTiles(self, canvas, data):
		for piece in self.tiles:
			pX = piece[0]
			pY = piece[1]
			if data.mode == "win" or data.showTiles:
				# show the tile if it's a win
				canvas.create_image(pX + 3, pY - 4, image=data.backHPng)
				self.threeDTile(canvas, pX + 1, pY - 2)
				tileName = piece[2][1]
				img = data.imageDictR[tileName]
			# show back of tile if you're a cpu or it's not your turn
			elif type(self) in data.cpus or type(data.turnOrder[data.turnInd]) != type(self):
				self.threeDTile(canvas, pX, pY)
				img = data.backHPng
			else:
				canvas.create_image(pX + 3, pY - 4, image=data.backHPng)
				self.threeDTile(canvas, pX + 1, pY - 2)
				tileName = piece[2][1]
				img = data.imageDictR[tileName]
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
			pX = data.width - 35
			pY = 720 - 40 * i
			canvas.create_image(pX + 3, pY - 4, image=data.backHPng)
			self.threeDTile(canvas, pX + 1, pY - 2)
			tileName = piece[2][1]
			img = data.imageDictR[tileName]
			canvas.create_image(pX, pY, image=img)
			i += 1
