"""
This is a test file, intended to experiment with calling a function from
another file.
"""
import Tkinter as tk # tkinter in Py3
from os import path


"""
Draws squares on game board canvas
Args:
@canvasGB -
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
            image_x = round(side / 2) + gap + x * side_step
            image_y = round(side / 2) + gap + x * side_step
            imageLocationsGB.append( [image_x, image_y] )
    return imageLocationsGB


"""
Creates and exports two canvases for game board and next piece.
Draws board squares. The size of the squares can be configured here, by changing
the three constants, side, gap, and line.
Args:
@root - window to draw on
Returns:
imageLocationsGB - list with line-by-line corordinates of square centers
"""
def initGameScreen(root):

    # Board square size
    side = 105  # Length of square side
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

    return imageLocationsGB

"""
Creates and exports the canvas for remaining pieces.
Sets up and exports imagePaths, a list of paths to the piece image files.
Args:
@root - window to draw on
"""
def initRPcanvas( root ):
    # Export global variables
    global canvasRP
    global imagePaths

    # Canvas dimensions
    widthRP = 200
    heightRP = 1031

    # Icon placement positions (a column)
    x_offset = 100  # x position of images
    delta_y = 64  # y distance between images (start at 0)

    # Remaining pieces canvas
    canvasRP = tk.Canvas(root, bg="light grey")
    canvasRP.place(x=0, y=0, width = widthRP, height = heightRP)

    # Set up locations for remaining pieces image locations
    imageLocationsRP = []
    for c in range(16):
        imageLocationsRP.append( [x_offset, 34 + delta_y * c] )

    # Set up icon locations in file system
    imagePaths = [
        tk.PhotoImage(file = path.dirname(__file__) + '/imgClr1/p' + str(i) + '.gif')
        for i in range(1, 17)
    ]

    # Set up dictionary with three sizes of respective image
    imagePaths = [
        {
            "regular": image,
            "medium" : image.subsample(2),
            "small": image.subsample(3)
        }
        for image in imagePaths
    ]

    # Draw icons in imageLocationsRP on canvas
    for c in range(16):
        canvasRP.create_image(imageLocationsRP[c], image=imagePaths[c]['small'])


root = tk.Tk()
root.title("UU Game")

initGameScreen(root)
initRPcanvas(root)

# Launch main event loop
root.mainloop()
