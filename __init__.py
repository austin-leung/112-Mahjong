# Animation starter code from Course Notes

from tkinter import *
import os
import random
import copy
import logic

####################################
# customize these functions
####################################

def init(data):
    data.mode = "start"
    data.images = []
    data.drawPile = [] 
    data.highlighted = []
    data.highlightedPieces = []
    data.handL = []
    data.handR = []
    data.handT = []
    data.handYou = []
    loadImages(data) 

def mousePressed(event, data):
    # use event.x and event.y
    if data.mode == "play": playMousePressed(event, data)


def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "p":
        data.mode = "play"
    if data.mode == "play": playKeyPressed(event, data)

def timerFired(data):
    if data.mode == "play": playTimerFired(data)

def redrawAll(canvas, data):
    # draw in canvas
    if data.mode == "start":
        canvas.create_text(data.width / 2, data.height / 2, text="press p to play")
    elif data.mode == "play": playRedrawAll(canvas, data)

def loadImages(data):
    path = os.getcwd() + "/Images/"
    for filename in os.listdir(path):
        if filename == ".DS_Store": # ignore this
            continue
        elif filename == "back.png": # don't add to draw pile, but keep track
            data.backPng = PhotoImage(file=path + filename)
            continue
        filepathName = path + filename
        # store in tuple, image, filename. filename is for ex. "2bamboo.png"
        data.images.append((PhotoImage(file=filepathName), filename)) 
    data.drawPile = copy.copy(data.images * 4) # 4 of each tile

    heightLeft = data.height / 2
    heightRight = data.height / 2
    widthTop = data.width / 2
    widthBot = data.width / 2

    # 13 per hand initially, 14 for the first player
    altMult = -1 # starts adding from center and then outwards
    for i in range(14):

        # left player
        randInd = random.randint(0,len(data.drawPile) - 1)
        data.handL.append([data.width / 10, heightLeft, data.drawPile[randInd], False])
        heightLeft += 45 * altMult * i
        altMult *= -1
        data.drawPile.pop(randInd)

    altMult = -1
    for i in range(14):
        # right player
        randInd = random.randint(0,len(data.drawPile) - 1)
        data.handR.append([9 * data.width / 10, heightRight, data.drawPile[randInd], False])
        heightRight += 45 * altMult * i
        altMult *= -1
        data.drawPile.pop(randInd)

    altMult = -1
    for i in range(14):
        # top player
        randInd = random.randint(0,len(data.drawPile) - 1)
        data.handT.append([widthTop, data.height / 12, data.drawPile[randInd], False])
        widthTop += 45 * altMult * i
        altMult *= -1
        data.drawPile.pop(randInd)

    altMult = -1
    for i in range(15):
        # bottom player (you)
        randInd = random.randint(0,len(data.drawPile) - 1)
        data.handYou.append([widthBot, 11 * data.height / 12, data.drawPile[randInd], False])
        widthBot += 45 * altMult * i
        altMult *= -1
        data.drawPile.pop(randInd)

#---------------------- Play Mode -------------------------- #

def playMousePressed(event, data):
    pressTile(event, data)
     
def pressTile(event, data):
    for hand in [data.handYou,data.handT,data.handR,data.handL]:
        #piecesToRemove = []
        #namesToRemove = []
        for piece in hand:
            x1 = piece[0] - 15
            y1 = piece[1] - 20
            x2 = piece[0] + 15
            y2 = piece[1] + 20
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                piece[3] = not piece[3]
                if piece[3] == True:
                    """
                    # add e.g. "1bamboo.png"
                    data.highlighted.append(piece[2][1])
                    data.highlightedPieces.append(piece)
                    """
                    piece[1] -= 20 # highlighted pieces are shifted up
                elif piece[3] == False:
                    """
                    data.highlighted.remove(piece[2][1])
                    data.highlightedPieces.remove(piece)
                    """
                    piece[1] += 20 # shift down when unhighlighted
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


def playKeyPressed(event,data):
    pass

def playTimerFired(data):
    pass

def playRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="green")
    canvas.create_text(data.width / 2, data.height / 2, text="you playin")
    for hand in [data.handT,data.handR,data.handL]:
        for piece in hand:
            pX = piece[0]
            pY = piece[1]
            threeDTileBack(canvas, pX, pY)
            canvas.create_image(pX, pY, image=data.backPng)
    for piece in data.handYou:
        pX = piece[0]
        pY = piece[1]
        threeDTile(canvas, pX, pY)
        canvas.create_image(pX, pY, image=piece[2][0])

# creates 3d appearing mahjong piece 
def threeDTile(canvas, pX, pY):
    canvas.create_rectangle(pX - 12, pY - 28, pX + 22, pY + 18,  fill ="red", width = 0)
    canvas.create_rectangle(pX - 14, pY - 25, pX + 20, pY + 19,  fill ="white", width = 0)
    canvas.create_rectangle(pX - 15, pY - 24, pX + 19, pY + 20,  fill ="white", width = 0)
    canvas.create_rectangle(pX - 16, pY - 23, pX + 18, pY + 21,  fill ="white", width = 0)
    canvas.create_rectangle(pX - 17, pY - 22, pX + 17, pY + 22,  fill ="white", width =0)

# creates 3d appearing mahjong piece 
def threeDTileBack(canvas, pX, pY):
    canvas.create_rectangle(pX - 11, pY - 23, pX + 18, pY + 17,  fill ="white", width = 0)
    canvas.create_rectangle(pX - 12, pY - 22, pX + 17, pY + 18,  fill ="white", width = 0)
    canvas.create_rectangle(pX - 13, pY - 21, pX + 16, pY + 19,  fill ="white", width = 0)
    canvas.create_rectangle(pX - 14, pY - 20, pX + 15, pY + 20,  fill ="white", width =0)
    

####################################
# use the run function as-is
####################################

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