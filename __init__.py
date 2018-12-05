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
import graphicsFunc
import cpu
random.seed(11)
# ---------------------- Control Center ------------------------- #
# Mode structure from course notes

def init(data):
    data.mode = "start"
    data.images = []
    data.imageNames = []
    data.drawPile = [] 
    data.discPile = []
    data.B = playerB.PlayerB()
    data.R = playerR.PlayerR()
    data.T = playerT.PlayerT()
    data.L = playerL.PlayerL()
    data.turnOrder = [data.B, data.R, data.T, data.L]
    data.turnInd = random.randint(0, 3)
    graphicsFunc.loadImages(data)
    graphicsFunc.loadSeaFlow(data)
    graphicsFunc.initialHands(data)
    graphicsFunc.loadMisc(data)
    for image in data.images:
        data.imageNames.append(image[1])
    data.turnOrder[data.turnInd].addTile(data) # first player draws
    data.winningHand = data.turnOrder[data.turnInd].tiles + data.turnOrder[data.turnInd].melds
    data.winner = data.turnOrder[data.turnInd].name
    data.cpu = False
    data.cpus = []
    data.numPlayers = 1
    data.paused = False
    # L = ['6bamboo.png', '7bamboo.png', '9dot.png', '6bamboo.png', '8character.png','7character.png', \
    # '9dot.png', '6character.png','6bamboo.png', '8bamboo.png']
    # print(logic.winningTiles(data.imageNames, L))


def mousePressed(event, data):
    if data.mode == "start":
        # you clicked on the start
        if data.width / 2 - 50 <= event.x <= data.width / 2 + 250 and\
        290 <= event.y <= 410:
            graphicsFunc.setPlayersCpu(data)
            data.mode = "play" 
        elif data.width / 2 + 0 <= event.x <= data.width / 2 + 70 and\
        480 <= event.y <= 560:
            data.numPlayers -= 1
            if data.numPlayers < 1: data.numPlayers = 1
        elif data.width / 2 + 130 <= event.x <= data.width / 2 + 200 and\
        480 <= event.y <= 560:
            data.numPlayers += 1
            if data.numPlayers > 4: data.numPlayers = 4
    elif data.mode == "play": playMousePressed(event, data)
    elif data.mode == "pong": graphicsFunc.pongMousePressed(event, data)
    elif data.mode == "chow": graphicsFunc.chowMousePressed(event, data)
    elif data.mode == "pause": pauseMousePressed(event, data)

def keyPressed(event, data):
    if event.keysym == "p": # play with full control, all tiles revealed 
        data.mode = "play"
    if event.keysym == "q": # for testing
        data.mode = "win"
    if event.keysym == "r": # for resetting
        init(data)
    if event.keysym == "1": # for testing
        for hand in data.turnOrder:
            print(hand.name)
            print(hand.tiles, "tiles")
            print(hand.melds, "melds")
    if data.mode == "start":
        if event.keysym == "c":
            data.cpu = True
            print("Currently in Cpu mode")
            data.cpus.append(type(data.R))
            data.cpus.append(type(data.L))
            data.cpus.append(type(data.T))
            data.mode = "play"
    if data.mode == "play": 
        playKeyPressed(event, data)


def timerFired(data):
    if data.mode == "play": playTimerFired(data)

def redrawAll(canvas, data):
    if data.mode == "start":
        canvas.create_image(data.width / 2, data.height / 2, image = data.startBGPng)
        canvas.create_image(data.width / 2 + 100, 150, image = data.startMJPng)
        canvas.create_image(data.width / 2 + 100, 350, image = data.startStartPng)
        canvas.create_image(data.width / 2 + 100, 450, image = data.startPlayersPng)
        canvas.create_image(data.width / 2 + 100, 520, image = data.startArrowsPng)
        if data.numPlayers == 1:
            canvas.create_image(data.width / 2 + 100, 520, image = data.start1Png)
        elif data.numPlayers == 2:
            canvas.create_image(data.width / 2 + 100, 520, image = data.start2Png)
        elif data.numPlayers == 3:
            canvas.create_image(data.width / 2 + 100, 520, image = data.start3Png)
        elif data.numPlayers == 4:
            canvas.create_image(data.width / 2 + 100, 520, image = data.start4Png)
        """
        canvas.create_text(data.width / 2, data.height / 2 + 20, \
            text="Press 'c' to play against three cpu", font = "Arial 25")
        canvas.create_text(data.width / 2, data.height / 2 + 100, font = "Arial 25",\
            text= "Press 'p' to play with revealed hands +")
        canvas.create_text(data.width / 2, data.height / 2 + 130, font = "Arial 25", \
            text= "full control over all players (testing/debugging)")
        canvas.create_text(data.width / 2, data.height / 2 + 180, font = "Arial 25", \
            text= "Press 'r' at any point to return to the start screen")
        canvas.create_text(data.width / 2, data.height / 2 + 230, font = "Arial 25", \
            text= "Press 'q' to go to the winning hand screen (testing)")
        """
    elif data.mode == "play": 
        playRedrawAll(canvas, data)
    elif data.mode == "pong": 
        playRedrawAll(canvas, data)
        graphicsFunc.pongRedrawAll(canvas, data)
    elif data.mode == "chow":
        playRedrawAll(canvas, data)
        graphicsFunc.chowRedrawAll(canvas, data)
    elif data.mode == "pause":
        playRedrawAll(canvas, data)
        graphicsFunc.pauseRedrawAll(canvas, data)
    elif data.mode == "win":
        playRedrawAll(canvas, data)
        graphicsFunc.winRedrawAll(canvas, data)


#---------------------- Play Mode -------------------------- #


def playMousePressed(event, data):
    # skip right to nextTurn(data) if you were waiting to continue turn
    if data.paused == False:
        cpuTurn = type(data.turnOrder[data.turnInd]) in data.cpus # if it's a cpu's turn
        if cpuTurn:
            # have cpu choose a tile among non-melded tiles
            cpuTiles = copy.copy(data.turnOrder[data.turnInd].tileNames)
            meldTiles = logic.longestCombo(cpuTiles)
            for tile in meldTiles:
                cpuTiles.remove(tile)
            # cpuTiles should only have tiles not already in a meld left
            chosenTileName = random.choice(cpuTiles)
            chosenTile = random.choice(data.turnOrder[data.turnInd].tiles) # just in case
            for tile in data.turnOrder[data.turnInd].tiles:
                if chosenTileName == tile[2][1]:
                    chosenTile = tile
            event.x = chosenTile[0]
            event.y = chosenTile[1]
        # highlights tile if pressed
        graphicsFunc.tilePressed(event, data)
        if cpuTurn:
            # make event.x and event.y "press" the discard button
            event.x = data.width / 2
            event.y = 2 * data.height / 3 + 100
        # discards highlighted tile, returns None unless a human player discards
        if graphicsFunc.discardPressed(event, data) != None:
            if data.mode == "pause": # don't change turn and add the tile yet if paused
                return
            graphicsFunc.nextTurn(data) # change turn and add tile
            data.paused = False
            if len(data.drawPile) == 0:
                print("game over no one wins") # temp
    else: # after you've come back from pausing
        graphicsFunc.nextTurn(data) # change turn and add tile
        data.paused = False
        if len(data.drawPile) == 0:
            print("game over no one wins") # temp

def playKeyPressed(event,data):
    pass

def playTimerFired(data):
    pass

def playRedrawAll(canvas, data):
    # draw background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="green") 
    canvas.create_rectangle(160, 140, data.width - 165, data.height - 155, fill="green", width = 2) 
    # discard button
    graphicsFunc.discardButton(canvas, data)
    # draw tiles
    for hand in data.turnOrder:
        hand.drawTiles(canvas, data)
        hand.drawMelds(canvas, data)
    # draw discard pile
    graphicsFunc.drawDiscard(canvas, data)
    # draw remaining draw tile count
    canvas.create_text(data.width / 2, 2 * data.height / 3, text= "Tiles Left: " + \
        str(len(data.drawPile)), font = "Arial 20")
    # draw text indicating whose turn it is
    canvas.create_text(data.width / 2, 2 * data.height / 3 + 40, \
        text="Current Turn: " + data.turnOrder[data.turnInd].name, font = "Arial 20")
    if data.cpu == True:
        canvas.create_text(data.width / 2, 2 * data.height / 3 + 60, \
            text="Click anywhere for the computer to make a move.", font = "Arial 20")

def pauseMousePressed(event, data):
    if data.width / 3 <= event.x <= 2 * data.width / 3 and \
    5.7 * data.height / 10 <= event.y <= 7.2 * data.height / 10:
        data.mode = "play"
        playMousePressed(event,data)

###########################################
# Animation starter code from Course Notes
###########################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 800)