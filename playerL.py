import player
import random

class PlayerL(player.Player):

	def initialHand(self, data):
		data.altMultL = 1 # starts adding from center and then outwards
		data.heightLeft = data.height / 2 - 30
		for i in range(1,14):
			randInd = random.randint(0,len(data.drawPile) - 1)
			self.tiles.append([ 1.5 * data.width / 10, data.heightLeft, data.drawPile[randInd], False])
			data.heightLeft += 40 * data.altMultL * i # goes right then left then right...
			data.altMultL *= -1
			data.drawPile.pop(randInd)

	def reorganizeTiles(self, data):
		newTiles = []
		data.heightLeft = data.height / 2 - 30
		tilesInd = 0
		for i in range(1, len(self.tiles) + 1):
			newTiles.append([ 1.5 * data.width / 10, data.heightLeft, self.tiles[tilesInd][2], False])
			data.heightLeft += 40 * data.altMultL * i # goes right then left then right...
			data.altMultL *= -1
			tilesInd += 1
		self.tiles = newTiles

	# draws a tile from the available tiles
	def addTile(self, data):
		randInd = random.randint(0, len(data.drawPile) - 1)
		drawnTile = data.drawPile.pop(randInd)
		# add new tile at corresponding position
		self.tiles.append([ 1.5 * data.width / 10, data.heightLeft, drawnTile, False])
		# change position of next tile
		i = len( self.tiles)
		data.heightLeft += 40 * data.altMultL * i # goes right then left then right...
		data.altMultL *= -1

	# draws horizontal tile with hidden image
	def drawTiles(self, canvas, data):
		for piece in self.tiles:
			pX = piece[0]
			pY = piece[1]
			self.threeDTile(canvas, pX, pY)
			canvas.create_image(pX, pY, image=data.backHPng)

	# creates 3d appearing mahjong piece horizontally
	def threeDTile(self, canvas, pX, pY):
		canvas.create_rectangle(pX - 23, pY - 11, pX + 17, pY + 18,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 22, pY - 12, pX + 18, pY + 17,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 21, pY - 13, pX + 19, pY + 16,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 20, pY - 14, pX + 20, pY + 15,  fill ="white", width = 0)



