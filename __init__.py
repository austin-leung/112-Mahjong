# __init__.py is the main file where everything is run from

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
import assist

random.seed(11)
# ---------------------- Control Center ------------------------- #
# Mode structure from course notes

def init(data):
    data.mode = "start"
    data.assistMode = False
    data.images = []
    data.imageNames = []
    data.imageDict = {}
    data.imagesL = []
    data.imagesR = []
    data.imageDictL = {}
    data.imageDictR = {}
    data.drawPile = [] 
    data.discPile = []
    data.B = playerB.PlayerB()
    data.R = playerR.PlayerR()
    data.T = playerT.PlayerT()
    data.L = playerL.PlayerL()
    data.turnOrder = [data.B, data.R, data.T, data.L]
    data.turnInd = random.randint(0, 3)
    graphicsFunc.loadImages(data)
    graphicsFunc.loadImagesL(data)
    graphicsFunc.loadImagesR(data)
    graphicsFunc.loadSeaFlow(data)
    graphicsFunc.initialHands(data)
    graphicsFunc.loadMisc(data)
    for image in data.images:
        data.imageNames.append(image[1])
        data.imageDict[image[1]] = image[0]
    data.turnOrder[data.turnInd].addTile(data) # first player draws
    data.winningHand = data.turnOrder[data.turnInd].tiles + data.turnOrder[data.turnInd].melds
    data.winner = data.turnOrder[data.turnInd].name
    data.handSco = ["rawr", "lol\nlolz\nlolo"]
    data.cpu = False
    data.cpus = [] 
    data.numPlayers = 1
    data.paused = False
    data.meldsFirst = False
    data.widthIncr = 0
    data.heightIncr = 0
    data.loser = ""
    data.showHeuristics = False
    data.hardAI = False
    data.showTiles = False

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
        if data.width / 2 - 60 <= event.x <= data.width / 2 + 60 and\
        data.height / 2 + 200 <= event.y <= data.height / 2 + 320:
            data.hardAI = not data.hardAI
        if data.width / 2 + 150 <= event.x <= data.width / 2 + 270 and\
        data.height / 2 + 200 <= event.y <= data.height / 2 + 320:
            data.meldsFirst = not data.meldsFirst
    elif data.mode == "play": playMousePressed(event, data)
    elif data.mode == "pong": graphicsFunc.pongMousePressed(event, data)
    elif data.mode == "chow": graphicsFunc.chowMousePressed(event, data)
    elif data.mode == "pause": graphicsFunc.pauseMousePressed(event, data)
    elif data.mode == "drawn": graphicsFunc.drawnMousePressed(event, data)
    elif data.mode == "win": graphicsFunc.winMousePressed(event, data)
    if data.mode == "toStart": # back to start mode
        init(data)

def keyPressed(event, data):
    if event.keysym == "p": # play with full control, all tiles revealed 
        data.mode = "play"
    elif event.keysym == "q": # for testing
        data.mode = "win"
    elif event.keysym == "r": # for resetting
        init(data)
    elif event.keysym == "s": # toggle sort method
        data.meldsFirst = not data.meldsFirst
        print("Sort by melds first? " + str(data.meldsFirst))
    elif event.keysym == "h": # toggle printing heuristics
        data.showHeuristics = not data.showHeuristics
        print("Print out heuristics? " + str(data.showHeuristics))
    elif event.keysym == "a": # toggle printing heuristics
        data.hardAI = not data.hardAI
        print("Is the AI difficulty on hard? " + str(data.hardAI))
    if event.keysym == "d": # shows all tiles to debug
        data.showTiles = not data.showTiles
        print("Showing all tiles? " + str(data.showTiles))
    if data.mode == "play": 
        playKeyPressed(event, data)

def timerFired(data):
    if data.mode == "play": playTimerFired(data)
    elif data.mode == "moving": graphicsFunc.movingTimerFired(data)

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
        if data.hardAI == False:
            canvas.create_image(data.width / 2, data.height / 2 + 260, image = data.assistCheckBigPng)
            canvas.create_text(data.width / 2, data.height / 2 + 300, text = "Easy AI", font="Sans 18", \
            fill = "white")
        elif data.hardAI == True:
            canvas.create_image(data.width / 2, data.height / 2 + 260, image = data.assistCheckedBigPng)
            canvas.create_text(data.width / 2, data.height / 2 + 300, text = "Hard AI", font="Sans 18", \
            fill = "white")
        if data.meldsFirst == False:
            canvas.create_image(data.width / 2 + 210, data.height / 2 + 260, image = data.assistCheckBigPng)
            canvas.create_text(data.width / 2 + 210, data.height / 2 + 300, text = "Sort by type", font="Sans 18", \
            fill = "white")
        elif data.meldsFirst == True:
            canvas.create_image(data.width / 2 + 210, data.height / 2 + 260, image = data.assistCheckedBigPng)
            canvas.create_text(data.width / 2 + 210, data.height / 2 + 300, text = "Sort melds first", font="Sans 14", \
            fill = "white")
    
        """
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
    elif data.mode == "drawn":
        playRedrawAll(canvas, data)
        graphicsFunc.drawnRedrawAll(canvas, data)
    elif data. mode == "moving":
        playRedrawAll(canvas, data)
        graphicsFunc.movingTile(canvas, data)

#---------------------- Play Mode -------------------------- #

def playMousePressed(event, data):
    if assist.assistModePressed(event, data) != None:
        return # don't go to next turn, etc. if you click on the assist mode check
    if data.assistMode == True:
        data.turnOrder[data.turnInd].recTiles = logic.discAI(data)
    if data.turnOrder[data.turnInd].name == "Left":
        print(data.turnOrder[data.turnInd].tiles)
    # skip right to nextTurn(data) if you were waiting to continue turn
    if data.paused == False:
        cpuTurn = type(data.turnOrder[data.turnInd]) in data.cpus # if it's a cpu's turn
        if cpuTurn:
            if data.hardAI == False:
                # AI: have cpu choose a tile among non-melded tiles 
                bestTiles = logic.discAIEasy(data)
                # bestTiles should only have tiles not already in a meld left
            elif data.hardAI == True:
                # AI: have cpu choose a tile to discard among equally high heuristic value hand outcomes 
                bestTiles = logic.discAI(data)
            chosenTileName = random.choice(bestTiles)
            chosenTile = None 
            for tile in data.turnOrder[data.turnInd].tiles:
                if chosenTileName == tile[2][1]:
                    chosenTile = tile
            event.x = chosenTile[0]
            event.y = chosenTile[1]
        # highlights tile if pressed
        graphicsFunc.tilePressed(event, data)
        if cpuTurn: 
            # make event.x and event.y "press" the discard button
            event.x = data.width / 2 - 200
            event.y = data.height / 2 + 200
        # can't discard if you have no tile highlighted
        if data.turnOrder[data.turnInd].highlighted == None:
            return 
        # discards highlighted tile, returns None unless a human player discards
        if graphicsFunc.discardPressed(event, data) != None:
            if data.mode == "pause": # don't change turn and add the tile yet if paused
                return
            graphicsFunc.nextTurn(data) # change turn and add tile
            data.paused = False
            if data.assistMode == True:
                data.turnOrder[data.turnInd].recTiles = logic.discAI(data)
            if len(data.drawPile) == 0:
                data.mode = "drawn"
                print("Game over no one wins.") # temp
    else: # after you've come back from pausing
        graphicsFunc.nextTurn(data) # change turn and add tile
        data.paused = False
        if data.assistMode == True:
            data.turnOrder[data.turnInd].recTiles = logic.discAI(data)
        if len(data.drawPile) == 0:
            data.mode = "drawn"
            print("Game over, no one wins.") # temp

def playKeyPressed(event,data):
    pass

def playTimerFired(data):
    pass

def playRedrawAll(canvas, data):
    # draw background
    canvas.create_image(data.width / 2, data.height / 2, image = data.greenBGPng)
    canvas.create_rectangle(data.width / 2 - 265, data.height / 2 - 265,\
        data.width / 2 + 260, data.height / 2 + 193, width = 1)
    canvas.create_image(data.width / 2, data.height / 2 - 250, image = data.sunlightPng)
    graphicsFunc.drawGo(canvas, data)
    # only show the winning tiles if not cpu
    if data.assistMode == True and type(data.turnOrder[data.turnInd]) not in data.cpus:
        assist.drawWinningTiles(data, canvas)
        assist.drawRecommendedTiles(data, canvas)
    assist.drawCheck(canvas, data)
    # discard button
    graphicsFunc.discardButton(canvas, data)
    # draw tiles
    for hand in data.turnOrder:
        hand.drawTiles(canvas, data)
        hand.drawMelds(canvas, data)
    # draw discard pile
    graphicsFunc.drawDiscard(canvas, data)
    # draw remaining draw tile count
    canvas.create_text(data.width / 2 - 80, 2 * data.height / 3 + 125, text= "Tiles Left: " + \
        str(len(data.drawPile)), font = "Arial 15", fill = "light goldenrod")
    if data.cpu == True:
        canvas.create_text(data.width / 2 - 80, 2 * data.height / 3 + 88, \
            text="Click\nanywhere for\na cpu move.", font = "Arial 15", fill = "gold2")

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