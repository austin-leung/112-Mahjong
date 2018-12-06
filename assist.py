# assist.py contains functions for assist mode

import copy
import logic

# toggles assist mode when the button is pressed
def assistModePressed(event, data):
	if data.width / 2 - 185 <= event.x  <= data.width / 2 - 125 \
	and data.height / 2 + 200 <= event.y <= data.height / 2 + 260:
		data.assistMode = not data.assistMode
		return "toggled"

def drawCheck(canvas, data):
	if data.assistMode == False:
		canvas.create_image(data.width / 2 - 155, data.height / 2 + 230, image = data.assistCheckPng)
	elif data.assistMode == True:
		canvas.create_image(data.width / 2 - 155, data.height / 2 + 230, image = data.assistCheckedPng)
	canvas.create_text(data.width / 2 - 155, data.height / 2 + 250, text = "Assist", font="Sans 12", \
		fill = "white")

# sorts tiles
def sortTiles(data, hand):
	tileNamesCopy = copy.copy(hand.tileNames)
	# bamboo first
	bamboos = []
	for name in hand.tileNames:
		if name[1:] == "bamboo.png":
			bamboos.append(name)
			tileNamesCopy.remove(name)
	# dots second
	dots = []
	for name in hand.tileNames:
		if name[1:] == "dot.png":
			dots.append(name)
			tileNamesCopy.remove(name)
	# characters second
	characters = []
	for name in hand.tileNames:
		if name[1:] == "character.png":
			characters.append(name)
			tileNamesCopy.remove(name)
	bamboos.sort()
	dots.sort()
	characters.sort()
	# directions, winds, dragons last
	tileNamesCopy.sort()
	hand.tileNames = bamboos + dots + characters + tileNamesCopy
	sortedTileNames = copy.copy(hand.tileNames)
	newHand = [0] * len(hand.tileNames)
	for tile in hand.tiles:
		# add the tiles in order corresponding to the tileNames order
		sortedInd = sortedTileNames.index(tile[2][1])
		newImgTile = (data.imageDict[sortedTileNames[sortedInd]], sortedTileNames[sortedInd])
		newHand[sortedInd] = [tile[0], tile[1], newImgTile, False]
		sortedTileNames[sortedInd] = -1 # don't index to that tileName again
	hand.tiles = newHand

def sortTilesMeld(data, hand):
	tileNamesCopy = copy.copy(hand.tileNames)
	meldHand = logic.longestCombo(tileNamesCopy)
	tileNamesCopy2 = copy.copy(hand.tileNames)
	for name in meldHand:
		tileNamesCopy2.remove(name)
	copyRest = copy.copy(tileNamesCopy2)
	# bamboo first
	bamboos = []
	for name in tileNamesCopy2:
		if name[1:] == "bamboo.png":
			bamboos.append(name)
			copyRest.remove(name)
	# dots second
	dots = []
	for name in tileNamesCopy2:
		if name[1:] == "dot.png":
			dots.append(name)
			copyRest.remove(name)
	# characters second
	characters = []
	for name in tileNamesCopy2:
		if name[1:] == "character.png":
			characters.append(name)
			copyRest.remove(name)
	bamboos.sort()
	dots.sort()
	characters.sort()
	# directions, winds, dragons last
	tileNamesCopy.sort()
	sortedRest = bamboos + dots + characters + copyRest
	hand.tileNames = meldHand + sortedRest
	sortedTileNames = copy.copy(hand.tileNames)
	newHand = [0] * len(hand.tileNames)
	for tile in hand.tiles:
		# add the tiles in order corresponding to the tileNames order
		sortedInd = sortedTileNames.index(tile[2][1])
		newImgTile = (data.imageDict[sortedTileNames[sortedInd]], sortedTileNames[sortedInd])
		newHand[sortedInd] = [tile[0], tile[1], newImgTile, False]
		sortedTileNames[sortedInd] = -1 # don't index to that tileName again
	hand.tiles = newHand

# draws background box and winning tiles
def drawWinningTiles(data, canvas):
	winningTiles = data.turnOrder[data.turnInd].winningTiles
	canvas.create_rectangle(data.width / 2 + 105, 2 * data.height / 3 + 65, \
    data.width / 2 + 260, 2 * data.height / 3 + 135, fill = "pink")
	canvas.create_text(data.width / 2 + 185, 2 * data.height / 3 + 75, text = "Winning Tiles:", \
		font = "Arial 12", fill = "gray35")
	i = 0
	for tile in winningTiles:
		winTileImg = data.imageDict[tile]
		pX = data.width / 2 + 130 + 45 * i
		pY = 2 * data.height / 3 + 110
		threeDTile(canvas, pX, pY)
		canvas.create_image(pX, pY , image=winTileImg )
		i += 1

# creates 3d appearing mahjong piece with red at back
def threeDTile(canvas, pX, pY):
    canvas.create_rectangle(pX - 12, pY - 28, pX + 22, pY + 18,  fill ="red", width = 0)
    canvas.create_rectangle(pX - 14, pY - 25, pX + 20, pY + 19,  fill ="white", width = 0)
    canvas.create_rectangle(pX - 15, pY - 24, pX + 19, pY + 20,  fill ="white", width = 0)
    canvas.create_rectangle(pX - 16, pY - 23, pX + 18, pY + 21,  fill ="white", width = 0)
    canvas.create_rectangle(pX - 17, pY - 22, pX + 17, pY + 22,  fill ="white", width = 0)

def drawRecommendedTiles(data, canvas):
	recTiles = data.turnOrder[data.turnInd].recTiles
	canvas.create_rectangle(data.width / 2 - 25, 2 * data.height / 3 + 65, \
    data.width / 2 + 100, 2 * data.height / 3 + 135, fill = "pink")
	canvas.create_text(data.width / 2 + 40, 2 * data.height / 3 + 75, text = "Suggested Discards:", \
		font = "Arial 12", fill = "gray35")
	i = 0
	for tile in recTiles:
		recTileImg = data.imageDict[tile]
		pX = data.width / 2 + 10 + 45 * i
		pY = 2 * data.height / 3 + 110
		threeDTile(canvas, pX, pY)
		canvas.create_image(pX, pY , image=recTileImg )
		i += 1
