# graphicsFunc.py contains helper functions for graphics
from tkinter import *
import os
import random
import copy
import logic
import player
import playerL
import playerT
import playerB
import playerR

# loads the seasons and flowers
def loadSeaFlow(data):
    for i in range(1,5):
        actualFileS = "s" + str(i) + ".png"
        seaFile = os.getcwd() + "/miscImages/" + actualFileS
        data.images.append((PhotoImage(file=seaFile), actualFileS))
        data.drawPile.append((PhotoImage(file=seaFile), actualFileS))

        actualFileF = "f" + str(i) + ".png"
        flowFile = os.getcwd() + "/miscImages/" + actualFileF
        data.images.append((PhotoImage(file=seaFile), actualFileF))
        data.drawPile.append((PhotoImage(file=flowFile), actualFileF))

# loads the main tiles other than seasons and flowers, making 4 of each
def loadImages(data):
    path = os.getcwd() + "/tileImages/"
    for filename in os.listdir(path):
        if filename == ".DS_Store": # ignore this
            continue
        filepathName = path + filename
        # store in tuple, image, filename. filename is for ex. "2bamboo.png"
        data.images.append((PhotoImage(file=filepathName), filename)) 
    data.drawPile = copy.copy(data.images * 4) # 4 of each tile

# loads the red back.png and backH.png
def loadBack(data):
    backFile = os.getcwd() + "/miscImages/back.png"
    data.backPng = PhotoImage(file=backFile)
    backHFile = os.getcwd() + "/miscImages/backH.png"
    data.backHPng = PhotoImage(file=backHFile)


# sets up the hands of each  player, randomly, drawing from the drawpile
def initialHands(data):
    # 13 per hand initially, 14 for the first player
    for hand in data.turnOrder:
        hand.initialHand(data)

def tilePressed(event, data):
    i = 0
    for piece in data.turnOrder[data.turnInd].tiles:
        x1 = piece[0] - 15
        y1 = piece[1] - 20
        x2 = piece[0] + 15
        y2 = piece[1] + 20
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            piece[3] = not piece[3]
            if piece[3] == True:
                data.turnOrder[data.turnInd].highlightedPieces.append(i)
                """
                # add e.g. "1bamboo.png"
                data.highlighted.append(piece[2][1])
                data.highlightedPieces.append(piece)
                """
                piece[1] -= 20 # highlighted pieces are shifted up
            elif piece[3] == False:
                data.turnOrder[data.turnInd].highlightedPieces.remove(i)
                """
                data.highlighted.remove(piece[2][1])
                """
                piece[1] += 20 # shift down when unhighlighted
        i += 1
    """
    meld = False
    if logic.isPong(data.highlighted) or logic.isChow(data.highlighted):
        meld = True
        for i in range(3):
            piecesToRemove.append(data.highlightedPieces[i])
            namesToRemove.append(data.highlighted[i])
    if logic.isKong(data.highlighted):
        meld = True
        for i in range(4):
            piecesToRemove.append(data.highlightedPieces[i])
            namesToRemove.append(data.highlighted[i])
    if meld:
        print(namesToRemove)
        for i in range(len(namesToRemove)):
            data.highlighted.remove(namesToRemove[i])
        for i in range(len(piecesToRemove)):
            removeInd = hand.index(piecesToRemove[i])
            hand.pop(removeInd)
    piecesToRemove = []
    namesToRemove = []
    """
# discards highlighted tile if you click on the discard button, changes turn, next draws
def discardPressed(event, data):
    # can only discard one piece
    if len(data.turnOrder[data.turnInd].highlightedPieces) != 1:
        return
    elif event.x > data.width - 140 and event.y > data.height - 30:
        data.turnOrder[data.turnInd].discardTile(data)
        data.turnOrder[data.turnInd].reorganizeTiles(data)
        data.turnInd += 1
        if data.turnInd >= 4:
            data.turnInd = 0
        data.turnOrder[data.turnInd].addTile(data)
        data.turnOrder[data.turnInd].reorganizeTiles(data)

# draws the discard pile in the center of the table
def drawDiscard(canvas, data):
    # discard pile
    i = 0 # tracks pX up to 11 tiles in row
    j = 0 # tracks pY, increments only when row is completed
    for piece in player.Player.discPile:
        pX = 175 + 45 * i
        pY = 175 + 55 * j
        threeDTile(canvas, pX, pY)
        canvas.create_image(pX, pY , image=piece[2][0])
        i += 1
        if i == 11:
             i = 0
             j += 1

# creates 3d appearing mahjong piece with red at back
def threeDTile(canvas, pX, pY):
    canvas.create_rectangle(pX - 12, pY - 28, pX + 22, pY + 18,  fill ="red", width = 0)
    canvas.create_rectangle(pX - 14, pY - 25, pX + 20, pY + 19,  fill ="white", width = 0)
    canvas.create_rectangle(pX - 15, pY - 24, pX + 19, pY + 20,  fill ="white", width = 0)
    canvas.create_rectangle(pX - 16, pY - 23, pX + 18, pY + 21,  fill ="white", width = 0)
    canvas.create_rectangle(pX - 17, pY - 22, pX + 17, pY + 22,  fill ="white", width = 0)

# makes a discard button
def discardButton(canvas, data):
    canvas.create_rectangle(data.width - 140, data.height - 30, data.width, data.height, fill = "pink")
    canvas.create_text(data.width - 5, data.height - 5, text="Discard chosen tile", font = "Arial 15", \
        fill = "Gray", anchor = "se")

# draw pong
def pongRedrawAll(canvas, data):
    # background box
    canvas.create_rectangle(data.width / 3, 7.2 * data.height / 10, \
        2 * data.width / 3, 5.7 * data.height / 10, fill = "pink")
    # pong option text
    texty = data.pongOptHand.name + " can pong "
    canvas.create_text(data.width / 2, 6.3 * data.height / 10, text=texty, font = "Arial 15", \
        fill = "Gray")
    threeDTile(canvas, data.width / 2 + 80, 6.3 * data.height / 10)
    canvas.create_image(data.width / 2 + 80, 6.3 * data.height / 10, image = data.pongOptTile[2][0])
    # pong button
    canvas.create_rectangle(data.width / 3 + 40, 6.8 * data.height / 10, \
        data.width / 3 + 90, 7.1 * data.height / 10, fill = "cyan")
    canvas.create_text(data.width / 3 + 65, 6.95 * data.height / 10, text="Pong!", font = "Arial 15", \
        fill = "Gray")
    # skip button
    canvas.create_rectangle(2 * data.width / 3 - 90, 6.8 * data.height / 10, \
        2 * data.width / 3 - 40, 7.1 * data.height / 10, fill = "cyan")
    canvas.create_text(2 * data.width / 3 - 65, 6.95 * data.height / 10, text="Skip", font = "Arial 15", \
        fill = "Gray")

# key pressed pong
def pongMousePressed(event, data):
    # press Pong!
    if data.width / 3 + 40 <= event.x <= data.width / 3 + 90 \
    and 6.8 * data.height / 10 <= event.y <= 7.1 * data.height / 10:
        # add discarded tile to meld
        data.pongOptHand.melds.append([None, None, data.pongOptTile[2], False])
        # add first pong tile in hand to meld and remove from hand
        for tile in  data.pongOptHand.tiles:
            if tile[2][1] == data.firstPongTile[2][1]: # only compare by tile name
                data.pongOptHand.tiles.remove(tile)
                break
        data.pongOptHand.melds.append([None, None, data.firstPongTile[2], False])
        # add second pong tile in hand to meld and remove from hand
        for tile in  data.pongOptHand.tiles:
            if tile[2][1] == data.secondPongTile[2][1]: # only compare by tile name
                data.pongOptHand.tiles.remove(tile)
                break
        data.pongOptHand.melds.append([None, None, data.secondPongTile[2], False])
        data.mode = "play"
        data.pongOptHand.reorganizeTiles(data)
        player.Player.discPile.pop()
        data.turnInd = data.turnOrder.index(data.pongOptHand)
    # press Skip
    elif 2 * data.width / 3 - 90 <= event.x <= 2 * data.width / 3 - 40 \
    and 6.8 * data.height / 10 <= event.y <= 7.1 * data.height / 10:
        data.mode = "play"

# draw chow
def chowRedrawAll(canvas, data):
    # background box
    canvas.create_rectangle(data.width / 3, 7.2 * data.height / 10, \
        2 * data.width / 3, 5.7 * data.height / 10, fill = "pink")
    # pong option text
    texty = data.chowOptHand.name + " can chow "
    canvas.create_text(data.width / 2, 6.3 * data.height / 10, text=texty, font = "Arial 15", \
        fill = "Gray")
    threeDTile(canvas, data.width / 2 + 80, 6.3 * data.height / 10)
    canvas.create_image(data.width / 2 + 80, 6.3 * data.height / 10, image = data.chowOptTile[2][0])
    # chow button
    canvas.create_rectangle(data.width / 3 + 40, 6.8 * data.height / 10, \
        data.width / 3 + 90, 7.1 * data.height / 10, fill = "cyan")
    canvas.create_text(data.width / 3 + 65, 6.95 * data.height / 10, text="Chow!", font = "Arial 15", \
        fill = "Gray")
    # skip button
    canvas.create_rectangle(2 * data.width / 3 - 90, 6.8 * data.height / 10, \
        2 * data.width / 3 - 40, 7.1 * data.height / 10, fill = "cyan")
    canvas.create_text(2 * data.width / 3 - 65, 6.95 * data.height / 10, text="Skip", font = "Arial 15", \
        fill = "Gray")

# key pressed chow
def chowMousePressed(event, data):
    # press Chow!
    if data.width / 3 + 40 <= event.x <= data.width / 3 + 90 \
    and 6.8 * data.height / 10 <= event.y <= 7.1 * data.height / 10:
        print(data.firstChowTile, "first")
        print(data.secondChowTile, "second")
        print(data.chowOptHand.tiles, "the hand tiles")
        # add discarded tile to meld
        data.chowOptHand.melds.append([None, None, data.chowOptTile[2], False])
        # add first chow tile in hand to meld and remove from hand
        for tile in data.chowOptHand.tiles:
            if tile[2][1] == data.firstChowTile[2][1]: # only compare by tile name
                data.chowOptHand.tiles.remove(tile)
                break
        data.chowOptHand.melds.append([None, None, data.firstChowTile[2], False])
        # add second chow tile in hand to meld and remove from hand
        for tile in data.chowOptHand.tiles:
            if tile[2][1] == data.secondChowTile[2][1]: # only compare by tile name
                data.chowOptHand.tiles.remove(tile)
                break
        data.chowOptHand.melds.append([None, None, data.secondChowTile[2], False]) 
        data.mode = "play"
        data.chowOptHand.reorganizeTiles(data)
        player.Player.discPile.pop()
        data.turnInd = data.turnOrder.index(data.chowOptHand)
    # press Skip
    elif 2 * data.width / 3 - 90 <= event.x <= 2 * data.width / 3 - 40 \
    and 6.8 * data.height / 10 <= event.y <= 7.1 * data.height / 10:
        data.mode = "play"

