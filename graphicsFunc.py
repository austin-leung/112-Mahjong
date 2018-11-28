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
import copy

# loads the seasons and flowers
def loadSeaFlow(data):
    for i in range(1,5):
        actualFileS = "s" + str(i) + ".png"
        seaFile = os.getcwd() + "/miscImages/" + actualFileS
        #data.images.append((PhotoImage(file=seaFile), actualFileS))
        data.drawPile.append((PhotoImage(file=seaFile), actualFileS))

        actualFileF = "f" + str(i) + ".png"
        flowFile = os.getcwd() + "/miscImages/" + actualFileF
        #data.images.append((PhotoImage(file=flowFile), actualFileF))
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
    for tile in data.turnOrder[data.turnInd].tiles:
        x1 = tile[0] - 15
        y1 = tile[1] - 20
        x2 = tile[0] + 15
        y2 = tile[1] + 20
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            curPlayer = data.turnOrder[data.turnInd]
            # unhighlight the previous highlighted tile
            if curPlayer.highlighted != None:
                curPlayer.tiles[curPlayer.highlighted][1] += 20
            # highlight currently clicked tile
            curPlayer.tiles[i][1] -= 20
            curPlayer.highlighted = i
        i += 1

# discards highlighted tile if you click on the discard button, changes turn, next draws
def discardPressed(event, data):
    if data.width / 2 - 120 <= event.x < data.width / 2 + 120  and \
    2 * data.height / 3 + 80 <= event.y <=  2 * data.height / 3 + 130:
        data.turnOrder[data.turnInd].discardTile(data, data.turnOrder[data.turnInd].handOrder(data))
        data.turnOrder[data.turnInd].reorganizeTiles(data)
        data.turnInd += 1
        if data.turnInd >= 4:
            data.turnInd = 0
        data.turnOrder[data.turnInd].addTile(data)
        # don't be destructive
        tileNames = copy.copy(data.turnOrder[data.turnInd].tileNames)
        # check if you won after adding a tile
        checkWin = logic.winningCombo(tileNames)
        if checkWin != None:
            print(checkWin, "Won from draw!")
            data.mode = "win"
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
    canvas.create_rectangle(data.width / 2 - 120, 2 * data.height / 3 + 80, \
        data.width / 2 + 120, 2 * data.height / 3 + 130, fill = "pink")
    canvas.create_text(data.width / 2, 2 * data.height / 3 + 105, text="Discard chosen tile", font = "Arial 25", \
        fill = "Gray")

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
    cpuTurn = type(data.pongOptHand) in data.cpus # if it's a cpu's turn
    if cpuTurn:
        # cpu should press Pong! 
        print("pong cpu option")
        event.x = data.width / 3 + 50
        event.y = 7 * data.height / 10
    if data.width / 3 + 40 <= event.x <= data.width / 3 + 90 \
    and 6.8 * data.height / 10 <= event.y <= 7.1 * data.height / 10:
        # add discarded tile to meld
        data.pongOptHand.melds.append([None, None, data.pongOptTile[2], False])
        # add first pong tile in hand to meld and remove from hand
        for tile in  data.pongOptHand.tiles:
            if tile[2][1] == data.firstPongTile[2][1]: # only compare by tile name
                data.pongOptHand.tiles.remove(tile)
                data.pongOptHand.tileNames.remove(tile[2][1])
                break
        data.pongOptHand.melds.append([None, None, data.firstPongTile[2], False])
        # add second pong tile in hand to meld and remove from hand
        for tile in  data.pongOptHand.tiles:
            if tile[2][1] == data.secondPongTile[2][1]: # only compare by tile name
                data.pongOptHand.tiles.remove(tile)
                data.pongOptHand.tileNames.remove(tile[2][1])
                break
        data.pongOptHand.melds.append([None, None, data.secondPongTile[2], False])
        data.mode = "play"
        data.pongOptHand.reorganizeTiles(data)
        player.Player.discPile.pop()
        # send the added tile for the following player back to the draw pile
        lastDrawnTile = data.turnOrder[data.turnInd].tiles.pop()
        data.turnOrder[data.turnInd].tileNames.remove(lastDrawnTile[2][1])
        data.drawPile.append(lastDrawnTile[2])
        data.turnInd = data.turnOrder.index(data.pongOptHand)
        data.mode = "play"
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
    cpuTurn = type(data.chowOptHand) in data.cpus # if it's a cpu's turn
    if cpuTurn:
        print("chow cpu option")
        # cpu should press Chow! 
        event.x = data.width / 3 + 50
        event.y = 7 * data.height / 10
    # press Chow!
    if data.width / 3 + 40 <= event.x <= data.width / 3 + 90 \
    and 6.8 * data.height / 10 <= event.y <= 7.1 * data.height / 10:
        # add discarded tile to meld
        data.chowOptHand.melds.append([None, None, data.chowOptTile[2], False])
        # add first chow tile in hand to meld and remove from hand
        for tile in data.chowOptHand.tiles:
            if tile[2][1] == data.firstChowTile[2][1]: # only compare by tile name
                data.chowOptHand.tiles.remove(tile)
                data.chowOptHand.tileNames.remove(tile[2][1])
                break
        data.chowOptHand.melds.append([None, None, data.firstChowTile[2], False])
        # add second chow tile in hand to meld and remove from hand
        for tile in data.chowOptHand.tiles:
            if tile[2][1] == data.secondChowTile[2][1]: # only compare by tile name
                data.chowOptHand.tiles.remove(tile)
                data.chowOptHand.tileNames.remove(tile[2][1])
                break
        data.chowOptHand.melds.append([None, None, data.secondChowTile[2], False]) 
        data.mode = "play"
        data.chowOptHand.reorganizeTiles(data)
        player.Player.discPile.pop()
        # send the added tile for the following player back to the draw pile
        lastDrawnTile = data.turnOrder[data.turnInd].tiles.pop()
        data.turnOrder[data.turnInd].tileNames.remove(lastDrawnTile[2][1])
        data.drawPile.append(lastDrawnTile[2])
        data.turnInd = data.turnOrder.index(data.chowOptHand)
    # press Skip
    elif 2 * data.width / 3 - 90 <= event.x <= 2 * data.width / 3 - 40 \
    and 6.8 * data.height / 10 <= event.y <= 7.1 * data.height / 10:
        data.mode = "play"

# victory message
def winRedrawAll(canvas, data):
    canvas.create_rectangle(data.width / 2 - 200, data.height / 2 - 200, \
        data.width / 2 + 200, data.height / 2 + 200, fill = "pink")
    canvas.create_text(data.width / 2, data.height / 2 - 100, text= data.winner + " WON!!!", font = "Arial 30")
    canvas.create_text(data.width / 2, data.height / 2 - 50, text= "The winning hand:", font = "Arial 30")
    # display the winning hand
    i = 0
    j = 0
    for piece in data.winningHand:
        pX = data.width / 2 - 125 + 45 * i
        pY = data.height / 2 + 50 + 55 * j
        threeDTile(canvas, pX, pY)
        canvas.create_image(pX, pY , image=piece[2][0])
        i += 1
        if i == 7:
            j += 1
            i = 0
