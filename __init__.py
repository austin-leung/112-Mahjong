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

def init(data):
    data.mode = "start"
    data.images = []
    data.imageNames = []
    data.drawPile = [] 
    data.B = playerB.PlayerB()
    data.R = playerR.PlayerR()
    data.T = playerT.PlayerT()
    data.L = playerL.PlayerL()
    data.turnOrder = [data.B, data.R, data.T, data.L]
    data.turnInd = random.randint(0, 3)
    graphicsFunc.loadImages(data)
    graphicsFunc.loadSeaFlow(data)
    graphicsFunc.initialHands(data)
    graphicsFunc.loadBack(data)
    for image in data.images:
        data.imageNames.append(image[1])
    data.turnOrder[data.turnInd].addTile(data) # first player draws
    data.winningHand = data.turnOrder[data.turnInd].tiles + data.turnOrder[data.turnInd].melds
    data.winner = data.turnOrder[data.turnInd].name
    data.cpu = False
    data.cpus = []
    # L = ['6bamboo.png', '7bamboo.png', '9dot.png', '6bamboo.png', '8character.png','7character.png', \
    # '9dot.png', '6character.png','6bamboo.png', '8bamboo.png']
    # print(logic.winningTiles(data.imageNames, L))


def mousePressed(event, data):
    if data.mode == "play": playMousePressed(event, data)
    elif data.mode == "pong": graphicsFunc.pongMousePressed(event, data)
    elif data.mode == "chow": graphicsFunc.chowMousePressed(event, data)

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
            data.mode = "play"
    if data.mode == "play": 
        playKeyPressed(event, data)
        if data.cpu == True:
            data.cpus.append(type(data.R))
            data.cpus.append(type(data.L))
            data.cpus.append(type(data.T))

def timerFired(data):
    if data.mode == "play": playTimerFired(data)

def redrawAll(canvas, data):
    if data.mode == "start":
        canvas.create_rectangle(0, 0, data.width, data.height, fill="cyan")
        canvas.create_text(data.width / 2, data.height / 2 - 100, \
            text="Temporary Start Screen :~)", font = "Arial 40")
        canvas.create_text(data.width / 2, data.height / 2 + 20, \
            text="Press 'c' to play against three cpu", font = "Arial 25")
        canvas.create_text(data.width / 2, data.height / 2 + 100, font = "Arial 25",\
            text= "Press 'p' to play with revealed hands +")
        canvas.create_text(data.width / 2, data.height / 2 + 130, font = "Arial 25", \
            text= "full control over all players (testing/debugging)")
        canvas.create_text(data.width / 2, data.height / 2 + 180, font = "Arial 25", \
            text= "Press 'r' at any point to return to the start screen")
    elif data.mode == "play": 
        playRedrawAll(canvas, data)
    elif data.mode == "pong": 
        playRedrawAll(canvas, data)
        graphicsFunc.pongRedrawAll(canvas, data)
    elif data.mode == "chow":
        playRedrawAll(canvas, data)
        graphicsFunc.chowRedrawAll(canvas, data)
    elif data.mode == "win":
        playRedrawAll(canvas, data)
        graphicsFunc.winRedrawAll(canvas, data)


#---------------------- Play Mode -------------------------- #


def playMousePressed(event, data):
    cpuTurn = type(data.turnOrder[data.turnInd]) in data.cpus # if it's a cpu's turn
    if cpuTurn:
        # have cpu choose a tile
        chosenTile = random.choice(data.turnOrder[data.turnInd].tiles)
        event.x = chosenTile[0]
        event.y = chosenTile[1]
    # highlights tile if pressed
    graphicsFunc.tilePressed(event, data)
    if cpuTurn:
        # make event.x and event.y "press" the discard button
        event.x = data.width / 2
        event.y = 2 * data.height / 3 + 100
    # discards highlighted tile, changes turn, draws
    graphicsFunc.discardPressed(event, data)
    if len(data.drawPile) == 0:
        print("game over no one wins") # temp

def playKeyPressed(event,data):
    pass

def playTimerFired(data):
    pass

def playRedrawAll(canvas, data):
    # draw background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="green") 
    # draw remaining draw tile count
    canvas.create_text(data.width / 2, 2 * data.height / 3, text= "Tiles Left: " + \
        str(len(data.drawPile)), font = "Arial 20")
    # draw text indicating whose turn it is
    canvas.create_text(data.width / 2, 2 * data.height / 3 + 40, \
        text="Current Turn: " + data.turnOrder[data.turnInd].name, font = "Arial 20")
    if data.cpu == True:
        canvas.create_text(data.width / 2, 2 * data.height / 3 + 60, \
            text="Click anywhere for the computer to make a move.", font = "Arial 20")
    # discard button
    graphicsFunc.discardButton(canvas, data)
    # draw tiles
    for hand in data.turnOrder:
        hand.drawTiles(canvas, data)
        hand.drawMelds(canvas, data)
    # draw discard pile
    graphicsFunc.drawDiscard(canvas, data)



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