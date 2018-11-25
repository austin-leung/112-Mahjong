import player
import random

class PlayerT(player.Player):

	def initialHand(self, data):
		data.widthTop = data.width / 2
		data.altMultT = 1
		for i in range(1,14):
			randInd = random.randint(0,len(data.drawPile) - 1)
			self.tiles.append([data.widthTop, 1.2 * data.height / 12, data.drawPile[randInd], False])
			data.widthTop += 40 * data.altMultT * i
			data.altMultT *= -1
			data.drawPile.pop(randInd)

	def reorganizeTiles(self, data):
		newTiles = []
		data.widthTop = data.width / 2
		tilesInd = 0
		for i in range(1, len(self.tiles) + 1):
			newTiles.append([data.widthTop, 1.2 * data.height / 12, self.tiles[tilesInd][2], False])
			data.widthTop += 40 * data.altMultT * i
			data.altMultT *= -1
			tilesInd += 1
		self.tiles = newTiles

	# draws a tile from the available tiles
	def addTile(self, data):
		randInd = random.randint(0, len(data.drawPile) - 1)
		drawnTile = data.drawPile.pop(randInd)
		# add new tile at corresponding position
		self.tiles.append([data.widthTop, 1.2 * data.height / 12, drawnTile, False])
		# change position of next tile
		i = len( self.tiles)
		data.widthTop += 40 * data.altMultT * i
		data.altMultT *= -1

	# creates 3d appearing mahjong piece with red background in front
	def drawTiles(self, canvas, data):
		for piece in self.tiles:
			pX = piece[0]
			pY = piece[1]
			self.threeDTile(canvas, pX, pY)
			canvas.create_image(pX, pY, image=data.backPng)

	# creates 3d appearing mahjong piece without red 
	def threeDTile(self, canvas, pX, pY):
		canvas.create_rectangle(pX - 11, pY - 23, pX + 18, pY + 17,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 12, pY - 22, pX + 17, pY + 18,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 13, pY - 21, pX + 16, pY + 19,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 14, pY - 20, pX + 15, pY + 20,  fill ="white", width =0)

