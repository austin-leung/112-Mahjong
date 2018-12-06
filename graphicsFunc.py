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

#---------------------- Init Functions -------------------------- #

# images photoshopped by me of actual tile pictures
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

# Most of the images from https://github.com/FluffyStuff/riichi-mahjong-tiles
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

# Most of the images from https://github.com/FluffyStuff/riichi-mahjong-tiles
def loadImagesL(data):
    path = os.getcwd() + "/tileLImages/"
    for filename in os.listdir(path):
        if filename == ".DS_Store": # ignore this
            continue
        filepathName = path + filename
        # store in tuple, image, filename. filename is for ex. "2bamboo.png"
        data.imagesL.append((PhotoImage(file=filepathName), filename))
    for image in data.imagesL:
        data.imageDictL[image[1]] = image[0]

# Most of the images from https://github.com/FluffyStuff/riichi-mahjong-tiles
def loadImagesR(data):
    path = os.getcwd() + "/tileRImages/"
    for filename in os.listdir(path):
        if filename == ".DS_Store": # ignore this
            continue
        filepathName = path + filename
        # store in tuple, image, filename. filename is for ex. "2bamboo.png"
        data.imagesR.append((PhotoImage(file=filepathName), filename))
    for image in data.imagesR:
        data.imageDictR[image[1]] = image[0]

# loads the miscelanneous images such as red back.png and backH.png, altered from https://github.com/FluffyStuff/riichi-mahjong-tiles
# start bg from https://www.fotolia.com/tag/mah-jongg
# start mahjong from https://www.randomsaladgames.com/
# start start from https://es.kisspng.com/kisspng-907zr1/preview.html
# start players from https://zh-cn.flamingtext.com/Word-Logos/players/
# start arrows from https://www.flaticon.com/free-icon/left-and-right-small-triangular-arrows-couple_37456
# start numbers from https://cliparts.zone/cute-number-4-cliparts
# assist checks from https://www.nuget.org/packages/awesome-bootstrap-checkbox-aspnet-mvc/
# green bg from http://xpgameplus.com/games/mahjongunlimited/index.html
# square from https://shoplook.io/product-preview/138758
# sunlight from https://pngtree.com/freepng/yellow-sunlight-beam-effect-light-png-photoshop_3563771.html
# go from http://www.cndajin.com/group/go/
# discard from http://iconsetc.com/icon/broccolidry_trash-bin/?style=simple-blue-gray
# edited for size and transparent background
def loadMisc(data):
    backFile = os.getcwd() + "/miscImages/back.png"
    data.backPng = PhotoImage(file=backFile)
    backHFile = os.getcwd() + "/miscImages/backH.png"
    data.backHPng = PhotoImage(file=backHFile)
    startBGFile = os.getcwd() + "/miscImages/startBG.png"
    data.startBGPng = PhotoImage(file=startBGFile)
    startMJFile = os.getcwd() + "/miscImages/startMahjong.png"
    data.startMJPng = PhotoImage(file=startMJFile)
    startStartFile = os.getcwd() + "/miscImages/startStart.png"
    data.startStartPng = PhotoImage(file=startStartFile)
    startPlayersFile = os.getcwd() + "/miscImages/startPlayers.png"
    data.startPlayersPng = PhotoImage(file=startPlayersFile)
    startArrowsFile = os.getcwd() + "/miscImages/startArrows.png"
    data.startArrowsPng = PhotoImage(file=startArrowsFile)
    start1File = os.getcwd() + "/miscImages/start1.png"
    data.start1Png = PhotoImage(file=start1File)
    start2File = os.getcwd() + "/miscImages/start2.png"
    data.start2Png = PhotoImage(file=start2File)
    start3File = os.getcwd() + "/miscImages/start3.png"
    data.start3Png = PhotoImage(file=start3File)
    start4File = os.getcwd() + "/miscImages/start4.png"
    data.start4Png = PhotoImage(file=start4File)
    assistCheckFile = os.getcwd() + "/miscImages/assistCheck.png"
    data.assistCheckPng = PhotoImage(file=assistCheckFile)
    assistCheckedFile = os.getcwd() + "/miscImages/assistChecked.png"
    data.assistCheckedPng = PhotoImage(file=assistCheckedFile)
    greenBGFile = os.getcwd() + "/miscImages/greenBG.png"
    data.greenBGPng = PhotoImage(file=greenBGFile)
    squareFile = os.getcwd() + "/miscImages/square.png"
    data.squarePng = PhotoImage(file=squareFile)
    sunlightFile = os.getcwd() + "/miscImages/sunlight.png"
    data.sunlightPng = PhotoImage(file=sunlightFile)
    goFile = os.getcwd() + "/miscImages/go.png"
    data.goPng = PhotoImage(file=goFile)
    discardFile = os.getcwd() + "/miscImages/discard.png"
    data.discardPng = PhotoImage(file=discardFile)
    assistCheckBigFile = os.getcwd() + "/miscImages/assistCheckBig.png"
    data.assistCheckBigPng = PhotoImage(file=assistCheckBigFile)
    assistCheckedBigFile = os.getcwd() + "/miscImages/assistCheckedBig.png"
    data.assistCheckedBigPng = PhotoImage(file=assistCheckedBigFile)

# sets up the hands of each  player, randomly, drawing from the drawpile
def initialHands(data):
    # 13 per hand initially, 14 for the first player
    for hand in data.turnOrder:
        hand.initialHand(data)

def setPlayersCpu(data):
    if data.numPlayers == 4:
        return
    data.cpu = True
    if data.numPlayers == 3:
        cpu = random.choice([data.R, data.T, data.L])
        data.cpus.append(type(cpu))
    elif data.numPlayers == 2:
        possCpu = [data.R, data.T, data.L]
        cpu1 = random.choice(possCpu)
        possCpu.remove(cpu1)
        cpu2 = random.choice(possCpu)
        data.cpus.append(type(cpu1))
        data.cpus.append(type(cpu2))
    elif data.numPlayers == 1:
        data.cpus.append(type(data.R))
        data.cpus.append(type(data.L))
        data.cpus.append(type(data.T))

#---------------------- Mouse Pressed Functions -------------------------- #

def tilePressed(event, data):
    curPlayer = data.turnOrder[data.turnInd]
    i = 0
    for tile in data.turnOrder[data.turnInd].tiles:
        if data.turnInd == 0 or data.turnInd == 2: # vertical tile ranges
            x1 = tile[0] - 15
            y1 = tile[1] - 20
            x2 = tile[0] + 15
            y2 = tile[1] + 20
        elif data.turnInd == 1 or data.turnInd == 3: # horizontal tile ranges
            x1 = tile[0] - 20
            y1 = tile[1] - 15
            x2 = tile[0] + 20
            y2 = tile[1] + 15
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            # highlight clicked tile
            # bottom or top
            if data.turnInd == 0 or data.turnInd == 2:
                curPlayer.tiles[i][1] -= 20
            # right
            elif data.turnInd == 1:
                curPlayer.tiles[i][0] -= 20
            # left
            elif data.turnInd == 3:
                curPlayer.tiles[i][0] += 20
            # unhighlight currently clicked tile
            if curPlayer.highlighted !=  None:
                # bottom or top
                if data.turnInd == 0 or data.turnInd == 2:
                    curPlayer.tiles[curPlayer.highlighted][1] += 20
                # right
                if data.turnInd == 1:
                    curPlayer.tiles[curPlayer.highlighted][0] += 20
                # left
                if data.turnInd == 3:
                    curPlayer.tiles[curPlayer.highlighted][0] -= 20
            if data.showHeuristics == True:
                curL = copy.copy(curPlayer.tileNames)
                removedTile = curPlayer.tiles[i][2][1]
                curL.remove(removedTile)
                print(logic.handHeuristic(data, curL, removedTile), "heuristic value of tile")
            curPlayer.highlighted = i
        i += 1 # try if another tile was clicked

# discards highlighted tile if you click on the discard button, changes turn, next draws
def discardPressed(event, data):
    if data.width / 2 - 255 <= event.x < data.width / 2 - 185  and \
    data.height / 2 + 195 <= event.y <= data.height / 2 + 265:
        data.turnOrder[data.turnInd].discardTile(data, data.turnOrder[data.turnInd].handOrder(data))
        data.turnOrder[data.turnInd].reorganizeTiles(data)
        # pause if you're not a cpu (and you're not the only player in the game)
        if type(data.turnOrder[data.turnInd]) not in data.cpus and data.numPlayers != 1:
                data.mode = "pause"
                data.paused = True
                return "discarded and paused"
        return "just discarded"

# changes turn checks for a win, adds tile
def nextTurn(data):
    data.turnInd += 1
    if data.turnInd >= 4:
        data.turnInd = 0
    hand = data.turnOrder[data.turnInd]
    hand.addTile(data)
    #print(lastDrawnTile[2][0], lastDrawnTile[2][1], hand.winningTiles, hand.name)
    if hand.lastDrawnTileName in hand.winningTiles:
        print("Won from draw!")
        data.winner = hand.name
        data.winningHand = hand.melds + hand.tiles
        winningHandNames = []
        for tile in data.winningHand:
            winningHandNames.append(tile[2][1])
        data.handSco = logic.handScore(data, winningHandNames)
        data.handSco[0] += 1
        data.handSco[1] += "Self-picked last tile +1\n"
        data.loser = "Self-pick!"
        print("Hand Score: " + str(data.handSco[0]))
        print(winningHandNames)
        data.mode = "win"
    hand.reorganizeTiles(data)

# draws the discard pile in the center of the table
def drawDiscard(canvas, data):
    # discard pile
    i = 0 # tracks pX up to 11 tiles in row
    j = 0 # tracks pY, increments only when row is completed
    for piece in data.discPile:
        pX = 170 + 45 * i
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
    #canvas.create_rectangle(data.width / 2 - 255, data.height / 2 + 195, \
    #data.width / 2 - 185, data.height / 2 + 265, fill = "pink")
    canvas.create_image(data.width / 2 - 220, data.height / 2 + 230, image = data.discardPng)

#---------------------- Pong Mode -------------------------- #

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
        data.discPile.pop()
        # send the added tile for the following player back to the draw pile
        lastDrawnTile = data.turnOrder[data.turnInd].tiles.pop()
        data.turnOrder[data.turnInd].tileNames.remove(lastDrawnTile[2][1])
        data.drawPile.append(lastDrawnTile[2])
        data.turnInd = data.turnOrder.index(data.pongOptHand)
        if data.assistMode == True:
            data.turnOrder[data.turnInd].recTiles = logic.discAI(data)
        data.mode = "play"
    # press Skip
    elif 2 * data.width / 3 - 90 <= event.x <= 2 * data.width / 3 - 40 \
    and 6.8 * data.height / 10 <= event.y <= 7.1 * data.height / 10:
        data.mode = "play"

#---------------------- Chow Mode -------------------------- #

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
        data.discPile.pop()
        # send the added tile for the following player back to the draw pile
        lastDrawnTile = data.turnOrder[data.turnInd].tiles.pop()
        data.turnOrder[data.turnInd].tileNames.remove(lastDrawnTile[2][1])
        data.drawPile.append(lastDrawnTile[2])
        data.turnInd = data.turnOrder.index(data.chowOptHand)
        if data.assistMode == True:
            data.turnOrder[data.turnInd].recTiles = logic.discAI(data)
    # press Skip
    elif 2 * data.width / 3 - 90 <= event.x <= 2 * data.width / 3 - 40 \
    and 6.8 * data.height / 10 <= event.y <= 7.1 * data.height / 10:
        data.mode = "play"

#---------------------- Win Mode -------------------------- #

# returns to start if you click in box
def winMousePressed(event, data):
    if data.width / 2 - 200 <= event.x <= data.width / 2 + 200 and\
    data.height / 2 - 200 <= event.y <= data.height / 2 + 200:
        data.mode = "toStart"

# victory message
def winRedrawAll(canvas, data):
    canvas.create_rectangle(data.width / 2 - 200, data.height / 2 - 200, \
        data.width / 2 + 200, data.height / 2 + 200, fill = "pink")
    canvas.create_text(data.width / 2, data.height / 2 - 180, \
        text= "The " + data.winner + " player won!" + data.loser, font = "Arial 25")
    canvas.create_text(data.width / 2, data.height / 2 - 150, \
        text= "Hand score: " + str(data.handSco[0]), font = "Arial 25", fill = "violet red")
    canvas.create_text(data.width / 2, data.height / 2 - 105, \
        text= data.handSco[1], font = "Arial 20", fill = "coral")
    canvas.create_text(data.width / 2, data.height / 2, text= "The winning hand:", font = "Arial 25")
    canvas.create_text(data.width / 2, data.height / 2 + 192, \
        text= "Click in the box to return to the start screen.", font = "Arial 12")
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

#---------------------- Pause Mode -------------------------- #

# draw pause screen
def pauseRedrawAll(canvas, data):
    # background box
    canvas.create_rectangle(data.width / 3 - 70, 6.6 * data.height / 10, \
        2 * data.width / 3 + 70, 6 * data.height / 10, fill = "pink")
    # pong option text
    texty = "Click this box and once more to continue"
    canvas.create_text(data.width / 2, 6.3 * data.height / 10, text=texty, font = "Arial 22", \
        fill = "Gray")

#---------------------- Drawn Mode -------------------------- #

def drawnMousePressed(event, data):
    if data.width / 3 - 100 <= event.x <= 2 * data.width / 3  + 90 and \
    6 * data.height / 10 <= event.y <= 7 * data.height / 10:
        data.mode = "toStart"

# draw drawn screen
def drawnRedrawAll(canvas, data):
    # background box
    canvas.create_rectangle(data.width / 3 - 100, 7 * data.height / 10, \
        2 * data.width / 3 + 90, 6 * data.height / 10, fill = "pink")
    # pong option text
    texty = "Game drawn. There are no tiles left.\nClick in the box to return to the start screen."
    canvas.create_text(data.width / 2, 6.4 * data.height / 10, text=texty, font = "Arial 22", \
        fill = "Gray")

#---------------------- Moving Mode -------------------------- #

# draws the tile moving
def movingTile(canvas, data):
    threeDTile(canvas, data.curRemoved[0], data.curRemoved[1])
    canvas.create_image(data.curRemoved[0], data.curRemoved[1], image = data.curRemoved[2][0])

def movingTimerFired(data):
    data.curRemoved[0] += data.widthIncr
    data.curRemoved[1] += data.heightIncr
    # if the tile is close enough to the center, stop moving
    if abs(data.curRemoved[0] - data.width / 2)  <= 1 \
    or abs(data.curRemoved[1] - data.height / 2) <= 1:
        data.mode = "play"
        hand = data.turnOrder[(data.turnInd-1) % 4] # subtract as pressing discarded incremented turn
        hand.discardTileAfterAni(data, hand.handOrder(data), data.curRemoved)

# draws go
def drawGo(canvas, data):
    if data.turnInd == 0: # bottom
        canvas.create_image(data.width / 2, 11 * data.height / 12, image = data.goPng)
    elif data.turnInd == 1: # right
        canvas.create_image(9.3 * data.width / 10, data.height / 2, image = data.goPng)
    elif data.turnInd == 2: # top
        canvas.create_image(data.width / 2, 1 * data.height / 12, image = data.goPng)
    elif data.turnInd == 3: # left
        canvas.create_image(0.8 * data.width / 10, data.height / 2, image = data.goPng)
