"""
This is a test file, intended to experiment with calling a function from
another file.
"""
import Tkinter as tk # tkinter in Py3
from os import path
from PIL import Image, ImageTk


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

    # Remaining pieces canvas
    canvasRP = tk.Canvas(root, bg="light grey")
    canvasRP.place(x=10, y=0, width = widthRP, height = heightRP)

    # Set up locations for remaining pieces image locations
    imageLocationsRP = []
    for c in range(16):
        imageLocationsRP.append( [x_offset, 34 + delta_y * c] )

    # Set up icon locations in file system
    imagePaths = [
        tk.PhotoImage(file = path.dirname(__file__) + '/imgClr1/p' + str(i) + '.gif')
        for i in range(1, 17)
    ]

    """
    # Set up dictionary with three sizes of respective image
    imagePaths = [
        {
            "regular": image,
            "small": image.subsample(3)
        }
        for image in imagePaths
    ]
    """
    imageDicts = []
    for image in imagePaths:
        imageDicts.append(
        {
            "regular": image,
            "small": image.subsample(3)
        })

    print("Number of icons: " + str(len(imageDicts)))
    for i in range(16):
        print("Image in pos " + str(i))
        print(imageDicts[i]['small'])


    # Draw icons in imageLocationsRP on canvas
    for c in range(16):
        print("Creating small image " + str(c))
        print(imageDicts[c]['small'])
        canvasRP.create_image(imageLocationsRP[c], image=imageDicts[c]['small'])
        lbl = tk.Label(canvasRP, text=str(c + 1), font=("Helvetica", 14), anchor="center", bg="light grey", fg="dim grey")
        lbl.place(x=10, y=imageLocationsRP[c][1] - 25, width=30, height=50)

    return imagePaths

"""
This class implements the terminal IO displayself. It has three fields --
two for output and one for input -- that it uses for player interaction.
Accessor methods are available for updating and reading values.
"""
class IOarea:
    """
    Sets up three text areas for:
    - PlayerLabel - player name prompt
    - InstructionLabel - what to do next
    - InstructioEntry - user entry
    Provides accessor methods
    Args:
    @root - window to draw on
    @x_start - x position to start drawing on
    @y_start - y position to start drawing on
    """
    def __init__(self, root, x_start, y_start):

        #global PlayerLabel
        #global InstructionLabel
        #global InstructionEntry
        #global contents  # user entry

        # Prompt for player (player 1 or 2)
        PlayerLabel = tk.Label(root, text="Player 1", font=("Helvetica", 14))
        PlayerLabel.place(x = x_start, y = (y_start + 10))
        self.PlayerLabel = PlayerLabel

        # Instructions to player
        InstructionLabel = tk.Label(root, text="Enter piece number to give away (1-16)\nand hit return. 0 terminates the game", font=("Helvetica", 14), anchor="w")
        InstructionLabel.place(x=x_start, y=(y_start + 45))
        self.InstructionLabel = InstructionLabel
        contents = tk.IntVar()
        self.contents = contents

        # Players entry field
        InstructionEntry = tk.Entry(root, bd = 5, textvariable=contents, bg="snow", relief=tk.SUNKEN, font=("Helvetica", 14))
        InstructionEntry.place(x=x_start, y=(y_start + 110))
        self.InstructionEntry = InstructionEntry


    # Accessor methods

    # Used to prompt the next player with the name
    def updatePlayerLabel(self,txt):
        self.PlayerLabel.config(text=txt)

    # Used to prompt the player with next action (select/place)
    def updateInstructionLabel(self, txt):
        self.InstructionLabel.config(text=txt)

    # Returns the value entered by the player
    def getInstruction(self):
        return int(self.contents.get())


"""
Starts the GAME_ENDEDArgs:
@player1name - (string) name of first player -- may be Null if AI is selected
@player2name - (string) name of second player -- may be Null if AI is selected
@player1orAI - player 1: 1 ==> human, 2 ==> AI
@player2orAI - player 2: 1 ==> human, 2 ==> AI
@AI1level - (string) easy, medium, or hard
@AI2level - (string) easy, medium, or hard
"""
def initGame(player1name, player2name, player1orAI, player2orAI, AI1level, AI2level):
    root = tk.Tk()
    root.title("UU Game")

    imageLocationsGB, GBheight = initGameScreen(root)
    imagePaths = initRPcanvas(root)
    IOarea1 = IOarea(root, 475, GBheight + 10)


# Launch main event loop
#root.mainloop()
