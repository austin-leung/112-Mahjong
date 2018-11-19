# Animation starter code from Course Notes

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.mode = "start"
    loadImages(data) # always load images in init!


# from course notes
def loadImages(data):
    tiles = 38 
    data.images = [ ]
    for tile in range(tiles):
        filename = "Regular/%d.png" % tile
        # resizing code from https://stackoverflow.com/questions/6582387/image-resize-under-photoimage
        data.images.append(PhotoImage(file=filename))

    data.board = []
    heightLeft = data.height - 100
    heightRight = data.height - 100
    widthTop = data.width - 105
    widthBot = data.width - 105
    for i in range(14):
        # left player
        data.board.append((data.width / 10, heightLeft, data.images[0]))
        heightLeft -= 45
        # right player
        data.board.append((9 * data.width / 10, heightRight, data.images[0]))
        heightRight -= 45
        # top player
        data.board.append((widthTop, data.height / 12, data.images[0]))
        widthTop -= 45
        # bottom player (you)
        imagey = random.randint(1, 37)
        data.board.append((widthBot, 11 * data.height / 12, data.images[imagey]))
        widthBot -= 45


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

def playMousePressed(event, data):
    pass

def playKeyPressed(event,data):
    pass

def playTimerFired(data):
    pass

import random
def playRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="green")
    canvas.create_text(data.width / 2, data.height / 2, text="you playin")
    for piece in data.board:
        canvas.create_rectangle(piece[0] - 17, piece[1] - 22, piece[0] + 17, piece[1] + 22,  fill ="white")
        canvas.create_image(piece[0], piece[1], image=piece[2] )
    

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