# playerB.py contains methods for the bottom player specifically

import player
import random
import graphicsFunc
import logic
import copy
import assist

class PlayerB(player.Player):

	def __init__(self):
		super().__init__("Bottom")

	def initialHand(self, data):
		data.widthBot = data.width / 2
		data.altMultB = 1
		for i in range(1,14):
			self.addTile(data)
		self.reorganizeTiles(data)

	# returns the sequential hand order to check for melds after the current player
	def handOrder(self, data):
		return [data.R, data.T, data.L]

	# recenters tiles based on the number of tiles left in the hand
	def reorganizeTiles(self, data):
		newTiles = []
		data.widthBot = data.width / 2 - 40 * (len(self.tiles) // 2)
		tilesInd = 0
		for i in range(1, len(self.tiles) + 1):
			newTiles.append([data.widthBot, 10.5 * data.height / 12, self.tiles[tilesInd][2], False])
			data.widthBot += 40
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
		self.tiles.append([data.widthBot, 10 * data.height / 12, drawnTile, False])
		self.tileNames.append(drawnTile[1])
		self.lastDrawnTileName = drawnTile[1]
		if data.assistMode == True:
			if data.meldsFirst == True:
				assist.sortTilesMeld(data, self)
			else:
				# sort normally
				assist.sortTiles(data, self)


	# draws tiles showing the images
	def drawTiles(self, canvas,data):
		for piece in self.tiles:
			pX = piece[0]
			pY = piece[1]
			if data.mode == "win" or data.showTiles:
				# show the tile if it's a win
				graphicsFunc.threeDTile(canvas, pX, pY)
				img = piece[2][0]
			# always show if you're the only player
			elif data.numPlayers == 1:
				graphicsFunc.threeDTile(canvas, pX, pY)
				img = piece[2][0]
			# show back of tile if you're a cpu or it's not your turn
			elif type(self) in data.cpus \
			or type(data.turnOrder[data.turnInd]) != type(self) or data.mode == "pause":
				self.threeDTile(canvas, pX, pY)
				img = data.backPng
			else:
				graphicsFunc.threeDTile(canvas, pX, pY)
				img = piece[2][0]
			canvas.create_image(pX, pY, image=img)

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
			pX = 80 + 45 * i
			pY = data.height - 35
			graphicsFunc.threeDTile(canvas, pX, pY)
			canvas.create_image(pX, pY, image=piece[2][0])
			i += 1
