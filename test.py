"""
This is a test file, intended to experiment with calling a function from
another file.
"""
import tkinter as tk # tkinter in Py3
from os import path
from PIL import Image, ImageTk
import socketio
import asynci

await socketio.AsyncClient().connect()
"""
Draws squares on game board canvas
Args:
@canvasGB - the canvas to draw on
@side - length of square side
@gap - gap between the squares
@line - width of edge line
Returns:
@Image locations list
"""
def drawGameBoardSquares(canvasGB, side, gap, line):
    side_step = side + gap + line
    # Image locations list
    imageLocationsGB = []

    # Draw rectangles line by line
    for y in range(4):
        for x in range(4):
            canvasGB.create_rectangle(
                gap + x * side_step,
                gap + y * side_step,
                side + gap + x * side_step,
                side + gap + y * side_step,
                fill = 'light grey',
                outline='dark grey',
                width = 5
            )
            # Also calculate middle points of squares
            image_x = x * side_step + round(side / 2) + gap
            image_y = y * side_step + round(side / 2) + gap
            imageLocationsGB.append( [image_x, image_y] )
            # Also place position number on squares
            lbl = tk.Label(canvasGB, text=str( x + 1 + y * 4), font=("Helvetica", 24, "bold"), fg="dark grey")
            lbl.place(x=image_x - 25, y=image_y - 25, width=50, height=50)  # center placement
            # lbl.place(x=(gap + x * side_step + 5), y=(gap + y * side_step) + 5)  # corner placement

    return imageLocationsGB


"""
Creates and exports two canvases for game board and next piece.
Draws board squares. The size of the squares can be configured here, by changing
the three constants, side, gap, and line.
Args:
@root - window to draw on
Returns:
imageLocationsGB - list with line-by-line corordinates of square centers
height of game board
"""
def initGameScreen(root):

    # Board square size
    side = 150  # Length of square side
    gap = 5     # Gap between the squares
    line = 2    # Extra slack between the squares

    # Resize window
    root.geometry(str(7 * (side + gap + line)) + "x" + str(6 * (side + gap + line)))

    # The two canvases that are created on the root window are
    # exported from this function
    global canvasGB
    global canvasNP

    # Next piece canvas
    xStartNP = 2 * (side + gap + line)
    canvasNP = tk.Canvas(root, bg="light grey")
    canvasNP.place(x=xStartNP, y=(4 * (side + gap + line) + 10), width = (side + line), height = (side + line))

    # Game Boad canvas
    xStartGB = 2 * (side + gap + line)
    canvasGB = tk.Canvas(root, bg="white")
    canvasGB.place(x=xStartGB, y=0, width=(4 * (side + gap + line) + 5), height=(4 * (side + gap + line) + 5))
    imageLocationsGB = drawGameBoardSquares( canvasGB, side, gap, line );

    return imageLocationsGB, 4 * (side + gap + line)

"""
Creates and exports the canvas for remaining pieces.
The pieces and corresponding labels are drawn on the canvas.
Args:
@root - window to draw on
Return:
@imagePaths - a list of paths to the piece image files
"""
def initRPcanvas( root ):
    # Export global variables
    global canvasRP
    global imagePaths

    # Canvas dimensions
    widthRP = 150
    heightRP = 1031

    # Icon placement positions (a column)
    x_offset = 80  # x position of images
    delta_y = 64  # y distance between images (start at 0)

    def update(self,gamesList):
        for aGame in gamesList:
            self.listBox.insert(tk.END, aGame)


    def addGame(self, aGame):
        self.listBox.insert(tk.END, aGame)


    #def deleteGame(self, aGame)

root = tk.Tk()
root.title("UU Game")
root.geometry("800x500")

lb = waitingGamesListBox(root, 10, 10)

# Launch main event loop
root.mainloop()
