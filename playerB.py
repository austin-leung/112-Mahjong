import player
import random

class PlayerB(player.Player):

	def initialHand(self, data):
		data.widthBot = data.width / 2
		data.altMultB = 1
		for i in range(1,15):
			# bottom player (you)
			randInd = random.randint(0,len(data.drawPile) - 1)
			self.tiles.append([data.widthBot, 10 * data.height / 12, data.drawPile[randInd], False])
			data.widthBot += 40 * data.altMultB * i
			data.altMultB *= -1
			data.drawPile.pop(randInd)

	def reorganizeTiles(self, data):
		newTiles = []
		data.widthBot = data.width / 2
		tilesInd = 0
		for i in range(1, len(self.tiles) + 1):
			newTiles.append([data.widthBot, 10 * data.height / 12, self.tiles[tilesInd][2], False])
			data.widthBot += 40 * data.altMultB * i
			data.altMultB *= -1
			tilesInd += 1
		self.tiles = newTiles

	# draws a tile from the available tiles
	def addTile(self, data):
		randInd = random.randint(0, len(data.drawPile) - 1)
		drawnTile = data.drawPile.pop(randInd)
		# add new tile at corresponding position
		self.tiles.append([data.widthBot, 10 * data.height / 12, drawnTile, False])
		# change position of next tile
		i = len( self.tiles)
		data.widthBot += 40 * data.altMultB * i
		data.altMultB *= -1

	# draws tiles showing the images
	def drawTiles(self, canvas,data):
		for piece in self.tiles:
			pX = piece[0]
			pY = piece[1]
			self.threeDTile(canvas, pX, pY)
			canvas.create_image(pX, pY, image=piece[2][0])

	# creates 3d appearing mahjong piece with red at back
	def threeDTile(self, canvas, pX, pY):
		canvas.create_rectangle(pX - 12, pY - 28, pX + 22, pY + 18,  fill ="red", width = 0)
		canvas.create_rectangle(pX - 14, pY - 25, pX + 20, pY + 19,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 15, pY - 24, pX + 19, pY + 20,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 16, pY - 23, pX + 18, pY + 21,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 17, pY - 22, pX + 17, pY + 22,  fill ="white", width = 0)
