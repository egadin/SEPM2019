"""
This implements the UU-GAME game platform.

(c) 2019 SEPM Group G
"""
#import socketio
import requests
import tkinter as tk
import numpy as np
import random
import copy
from PIL import Image, ImageTk
from os import path
#import mainpage * as main
from welcome import sio
from portal import sio



"""
Game class param @player1 name of first player @player2 name of second player, @AI the Ai that should be used
global canvasRP the box where remaining pieces are shown
global imageLocationsRP the coords to the images in canvasRP
global imagePaths to the img folder
"""
class Game:
    def __init__(self, player1, player2, AI1, AI2):
        global canvasRP # Canvas w remaining pieces
        global imageLocationsRP
        global imagePaths
        global sio
        # Attributes of the Game class
        # Fills with None of type np.object
        self.board = np.full((4,4), None, dtype = np.object_)
        self.pieces = [Piece(1,"round","black","dotted",0),Piece(2,"round","black","dotted",1),Piece(3,"round","black","line",0),Piece(4,"round","black","line",1),Piece(5,"round","blue","dotted",0),Piece(6,"round","blue","dotted",1),Piece(7,"round","blue","line",0),Piece(8,"round","blue","line",1),
        Piece(9,"square","black","dotted",0),Piece(10,"square","black","dotted",1),Piece(11,"square","black","line",0),Piece(12,"square","black","line",1),Piece(13,"square","blue","dotted",0),Piece(14,"square","blue","dotted",1),Piece(15,"square","blue","line",0),Piece(16,"square","blue","line",1)]
        self.remainingPieces = self.pieces
        self.nextPiece = None
        self.turncount = 0
        # Next thing for the event handler
        self.event = 2
        # Names of players
        self.player1 = None
        self.player2 = None
        # Inintiates the remaning pieces on the screen
        self.indexRemainingPieces = [canvasRP.create_image(imageLocationsRP[c], image=imagePaths[c]['small']) for c in range(16)]
        self.nextPieceImg = None
        self.AI1 = AI1
        self.AI2 = AI2

    """
    Method to see if a game state is final
    checks for 4 in a row for all attributes in the board of choice
    param @board anythe board that should be checked
    """
    @staticmethod
    def GAME_ENDED(board):
            for prop in ['shape', 'color', 'line', 'number']:
                # Check if a complete row is possible otherwise it goes to column check
                # (enough to check first place)
                for row in range(0, 4):
                    if not board[0, row]:
                        continue

                    for col in range(1, 4):
                        if not board[col, row]:
                            break

                        if vars(board[col, row])[prop] != vars(board[0, row])[prop]:
                            break
                    else:
                        return True

                # Check if a complete column is possible otherwise it goes to diagonal check
                for col in range(0, 4):
                    if not board[col, 0]:
                        continue

                    for row in range(1, 4):
                        if not board[col, row]:
                            break

                        if vars(board[col, row])[prop] != vars(board[col, 0])[prop]:
                            break
                    else:
                        return True

                # Diagonal check
                if board[0, 0]:
                    for diag in range(1, 4):
                        if not board[diag, diag]:
                            break

                        if not vars(board[0, 0])[prop] != vars(board[diag, diag])[prop]:
                            break
                    else:
                        return True

                if board[3, 0]:
                    for diag in range(1, 4):
                        if not board[4 - diag, diag]:
                            break

                        if not vars(board[3, 0])[prop] != vars(board[4 - diag, diag])[prop]:
                            break
                    else:
                        return True

            return False

    """
    The central game cordinator, gets called on user inputs and sends out calls to
    the correct methods to continue the game
    calls on the AI if a player is None
    event 3 is quit and fets called when a player inputs 0 in givePiece function
    param @e is dummy, forced by the caller
    """
    def EVENT_HANDLER(self, e):
        # Event values
        # - 1: layPiece
        # - 2: givePiece
        # - 3: quit
        if (self.event == 2):
            self.givePiece()
        elif (self.event == 1):
            if ((((1 + self.turncount % 2) != 1) and self.player2 == None) or ((1 + self.turncount % 2) == 1) and self.player1 == None):
                self.AIturn()
            else:
                self.layPiece()
        elif (self.event == 3): #Here you can call you function to go back to the main screen
            quit

    """
    Method for a human player to give a piece to the opponent
    removes the piece from remaining pieces and moves it into the box showing next piece
    if user inputs 0 the game will end
    global canvasNP the box for next piece
    global imagePaths the img folder
    """
    def givePiece(self):
        global canvasNP
        global imagePaths
        global terminalIO

        found = False
        for piece in range(0,16-self.turncount):
            #if (self.remainingPieces[piece].id == contents.get()):
            if (self.remainingPieces[piece].id == terminalIO.getInstruction()):
                self.nextPiece = self.remainingPieces[piece]  #nextpiece start as (0,0,0,0,0)
                found = True
                self.nextPieceImg = canvasNP.create_image([50,50], image=imagePaths[piece]['medium'])
        if (found == True):
            self.remainingPieces.remove(self.nextPiece)
            self.canvasRPhandler("delete", self.nextPiece.id-1)
            #InstructionEntry.delete(first=0,last=10)
            terminalIO.clearInstructionEntry()
            self.turncount += 1
            self.event = None
            sio.emit('nextPiece', {'id': int(self.nextPiece.id), 'shape': str(self.nextPiece.shape), 'color': str(self.nextPiece.color), 'line': str(self.nextPiece.line), 'number': self.nextPiece.number})
            #if (self.player1 == None or self.player2 == None):
             #   self.AIturn()
        else:
            if (terminalIO.getInstruction() == 0):
            #if (contents.get() == 0):
                self.event = 3
            else:
                #InstructionEntry.delete(first=0,last=10)
                #InstructionLabel.config(text='Nonexisting piece, please choose a piece that is left between 1-16:')
                terminalIO.clearInstructionEntry()
                terminalIO.updateInstructionLabel("instructionError1")
    """
    Method for a human player to lay a piece on the board
    removes the piece from next piece and moves it into the box showing the game board on the designated spot from the player
    checks if the game has ended
    global canvasNP the box for next piece
    """
    def layPiece(self):
        global canvasNP
        global terminalIO
        # User enters 0-16, decrement by 1 to make it -1 to 15
        cont = terminalIO.getInstruction() - 1
        #cont = contents.get() - 1
        column = cont % 4
        row = cont // 4
        if (cont < -1 or cont >= 16 or self.board[row,column] != None):
            #InstructionEntry.delete(first=0,last=10)
            #InstructionLabel.config(text='Nonexisting or taken tile please enter free tile between 1-16:')
            terminalIO.clearInstructionEntry()
            terminalIO.updateInstructionLabel("instructionError2")

        elif (cont == -1):
            self.event = 3
        else:
            #InstructionEntry.delete(first=0,last=10)
            terminalIO.clearInstructionEntry();
            sio.emit('board', cont)
            self.board[row,column] = self.nextPiece
            if(Game.GAME_ENDED(self.board)==True):
                print("ended") #here you can go back and break loop and such
            self.pieceCanvas(self.nextPiece.id, cont)
            canvasNP.delete(self.nextPieceImg)
            self.event = 2
            self.GAME_TURN()

    """
    help function for layPiece
    adding the image on the game boardCopy
    global canvasGB the box showing the game board
    global imagePaths the img folder
    global imageLocationsGB the cords to the boxes in canvasGB
    param @id the id of the piece that should be placed in the board
    param @canvas the number of the box where the piece should be placed
    """
    def pieceCanvas(self, id, canvas):
        global canvasGB
        global imagePaths
        global imageLocationsGB
        canvasGB.create_image(imageLocationsGB[canvas], image=imagePaths[id-1]['regular'])

    @sio.on('nextPiece')
    def nextpiece_event(data):
        global canvasNP
        global imagePaths
        self.nextPiece = Piece(data.id, data.shape, data.color, data.line, data.number)
        self.nextPiece = Piece(data['id'], data['shape'], data['color'], data['line'], data['number'])
        self.nextPieceImg = canvasNP.create_image([100,100], image=imagePaths[self.nextPiece.id-1]['regular'])
        self.remainingPieces.remove(self.nextPiece)
        self.canvasRPhandler("delete", self.nextPiece.id-1)
        self.event = 1
        self.turncount +=1
        self.GAME_TURN()

    @sio.on('board')
    def board_event(data):
        global canvasNP
        column = cont % 4
        row = cont // 4
        column = data % 4
        row = data // 4
        self.board[row,column] = self.nextPiece
        if(Game.GAME_ENDED(self.board)==True):
                print("ended") #here you can go back and break loop and such
        self.pieceCanvas(self.nextPiece.id, cont)
        canvasNP.delete(self.nextPieceImg)

    @sio.on('start game')
    def start_event():
        self.event = 1
        self.GAME_TURN()

    
    """
    Calling the alpha beta AI for cords and a next piece
    execute a turn without taking inputs and using the info from the AI instead
    global canvasNP box for the next piece
    global imagePaths the img folder
    """
    def AIturn(self):
        global canvasNP
        global imagePaths
        # Returns moveInfo object
        print(self.nextPiece)
        if(1+self.turncount%2 == 1):
            AImove = self.AI1.makeBestMove(self.board, self.remainingPieces, self.nextPiece, self.turncount) #skickar jag in riktiga eller copierar jag bara?
        else:
            AImove = self.AI2.makeBestMove(self.board, self.remainingPieces, self.nextPiece, self.turncount) #skickar jag in riktiga eller copierar jag bara?
        print(AImove.location, AImove.score, AImove.nextPiece)
        self.board[AImove.location] = self.nextPiece
        sio.emit('board', AImove.location[0]*4 + AImove.location[1])
        sio.emit('board', {'data':AImove.location[0]*4 + AImove.location[1]})
        if(Game.GAME_ENDED(self.board)==True):
            print("ended") #Do fancy stuff if you wannt to quit
        self.pieceCanvas(self.nextPiece.id, AImove.location[0]*4 + AImove.location[1])
        canvasNP.delete(self.nextPieceImg)
        for x in range(0,len(self.remainingPieces)):
            if (self.remainingPieces[x].id == AImove.nextPiece.id):
                self.nextPiece = self.remainingPieces[x]
        self.nextPieceImg = canvasNP.create_image([100,100], image=imagePaths[self.nextPiece.id - 1]['regular'])
        self.remainingPieces.remove(self.nextPiece)
        self.canvasRPhandler("delete", self.nextPiece.id-1)
        self.turncount += 1
        sio.emit('nextPiece', self.nextPiece)


    """
    Updating user interface box with current players name and which instruction is given
    acting as a stall state while waiting for users input as to which EVENT_HANDLER is called
    """
    def GAME_TURN(self):
        global terminalIO # class for handling player IO
        if (self.event == 1):
            #PlayerLabel.config(text='{}'.format(self.player1)) if ((1 + self.turncount % 2) == 1) else PlayerLabel.config(text='{}'.format(self.player2))
            #InstructionLabel.config(text='Where to place current piece (1-16):')
            if ((1 + self.turncount % 2) == 1):
                terminalIO.updatePlayerLabel(self.player1)
            else:
                terminalIO.updatePlayerLabel(self.player2)

            terminalIO.updateInstructionLabel("instructionPlace1")

        elif (self.event == 2):
            #PlayerLabel.config(text='{}'.format(self.player1)) if ((1 + self.turncount % 2) == 1) else PlayerLabel.config(text='{}'.format(self.player2))
            #InstructionLabel.config(text='Number of piece to give away (1-16):')
            if ((1 + self.turncount % 2) == 1):
                terminalIO.updatePlayerLabel(self.player1)
            else:
                terminalIO.updatePlayerLabel(self.player2)

            terminalIO.updateInstructionLabel("instructionSelect2")

    """
    Handles remaining pieces (currently only deletes)
    Options for canvasRP supports delete as of now since its initiated elsewhere
    param @action which action you want to perform in the handler
    param @number which piece you want to remove from the box
    global canvasRP the box for remaining pieces
    """
    def canvasRPhandler(self, action, number):
        global canvasRP
        if (action == "delete"):
            canvasRP.delete(self.indexRemainingPieces[number])

"""
Class containing the structure for a pieces
param @id identification for each piece so you can acces them
param @shape information about one of the binary parameters that a piece holds
param @color information about one of the binary parameters that a piece holds
param @line information about one of the binary parameters that a piece holds
param @number information about one of the binary parameters that a piece holds
"""
class Piece:
    def __init__(self, id, shape, color, line, number):
        self.id = id
        self.shape = shape
        self.color = color
        self.line = line
        self.number = number

    def __repr__(self):
        return "Piece(%d, %s, %s, %s, %d)" % (self.id, self.shape, self.color, self.line, self.number)

"""
Class containing the AI which is based on miniMax algorithm with alpha beta prouning
holds information about what difficulty you want to play on
otherwise it takes in the required information in it's functions to make a move absed on the current playing field
param @difficulty the difficulty you want to play on in string format
"""
class AI():
    def __init__(self, difficulty):
        self.difficulty = difficulty

    """
    Calls on the alphabeta which calculates the beest move and
    depending on your difficulty a certain percentage of the moves will be randomized
    param @board the current gameboard
    param @remainingPiecesCopy the array of remaining pieces
    param @nextPieceCopy the next piece that the AI should place
    """
    def makeBestMove(self, board, remainingPieces, nextPiece, turncount):
        rand = random.randint(1,11)
        boardCopy = copy.deepcopy(board)

        # Lookup table for level of difficulty.
        # translates names to thresholds for random function
        level = {
            "easy" : 1,
            "medium" : 3,
            "hard" : 7
        }

        if (rand > level[self.difficulty]):
            locInfo = self.randomLocation(board)
            npInfo = self.randomNP(remainingPieces)
            return moveInfo(0, locInfo[0], locInfo[1], npInfo)
        else:
            return self.alphabeta(boardCopy, remainingPieces, nextPiece, 0, float('-inf'), float('inf'), True, turncount)

        #
        # These should not be needed, unless more differentiated treatment is desired
        #
        if (self.difficulty == "easy"):
            if (rand > 1):
                locInfo = self.randomLocation(board)
                npInfo = self.randomNP(remainingPieces)
                return moveInfo(0, locInfo[0], locInfo[1], npInfo)
            else:
                return self.alphabeta(boardCopy, remainingPieces, nextPiece, 0, float('-inf'), float('inf'), True, turncount)

        elif (self.difficulty == "medium"):
            if (rand > 3):
                locInfo = self.randomLocation(board)
                npInfo = self.randomNP(remainingPieces)
                return moveInfo(0, locInfo[0], locInfo[1], npInfo)
            else:
                return self.alphabeta(boardCopy, remainingPieces, nextPiece, 0, float('-inf'), float('inf'), True, turncount)

        elif (self.difficulty == "hard"):
            if (rand > 7):
                locInfo = self.randomLocation(board)
                npInfo = self.randomNP(remainingPieces)
                return moveInfo(0, locInfo[0], locInfo[1], npInfo)
            else:
                return self.alphabeta(boardCopy, remainingPieces, nextPiece, 0, float('-inf'), float('inf'), True, turncount)

    """
    Randomizes a location on the gameboard from all the empty tiles
    and returns its cordinates
    param @board the current gameboard
    """
    def randomLocation(self, board):
        pieces = [(board[i % 4, i // 4], (i % 4, i // 4), i) for i in range(0, 15)]  #creates array for the matrix
        pieces = filter(lambda piece, coord, loc: piece is None, pieces)
        """
        dubbelceck this should return coords
        """
        if(pieces!=[]):
            piece = random.choice(pieces)
            return (piece[1], piece[2])
        else:
            return (None,None)
    """
    Randomizes a piece to give to the opponent from the remaining pieces array
    param @remainingPiecesCopy the array holding the remaining pieceCanvas
    """
    def randomNP(self, remainingPiecesCopy):
        return remainingPiecesCopy[random.randint(0,len(remainingPiecesCopy)-1)]

    """
    The minMax algorithm with alpha beta pruning
    iterates down through all possible solutions that doesn't get pruned and scores them if they are within a certain search depth
    otherwise it will give a random location and a neutral score
    returns the case with the highest score and sends back cordinates to lay the piece at and a number for the piece to give away
    param @board the gameboard
    param @remainingPiecesCopy the array of remaining pieces
    param @nextPieceCopy the next piece that should be placed
    param @depth the current depth which the algorithm is searching on
    param @a the alpha value
    param @b the beta value
    param @maximizingPlayer if the algorithm should be on min or max stage
    """
    def alphabeta(self, board, remainingPieces, nextPiece, depth, a, b, maximizingPlayer, turncount):
        if (len(remainingPieces)>=15):
           locInfo = self.randomLocation(board)
           npInfo = self.randomNP(remainingPieces)
           return moveInfo(0, locInfo[0], locInfo[1], npInfo)
        else:
            if (remainingPieces == []):
                return moveInfo(0,None,None,None)
            elif (Game.GAME_ENDED(board)):
                if (maximizingPlayer):
                    return moveInfo(depth-20, None,None,None)
                else:
                    return moveInfo(20-depth,None,None,None)
            elif (depth > (2 if turncount < 6 else 3)):
               locInfo = self.randomLocation(board)
               npInfo = self.randomNP(remainingPieces)
               return moveInfo(0, locInfo[0], locInfo[1], npInfo)

            if (maximizingPlayer):
                value = moveInfo(float('-inf'),None,None,None)
                boardCopy = copy.deepcopy(board)
                for i in range(len(boardCopy)):
                    for j in range(len(boardCopy[i])):
                        if (boardCopy[i,j] == None):
                            boardCopy[i,j] = nextPiece

                            for k in range(len(remainingPieces)):
                                remainingPiecesCopy = copy.deepcopy(remainingPieces)
                                nextPieceCopy = remainingPiecesCopy[k]
                                remainingPiecesCopy.remove(nextPieceCopy)
                                currentMove = self.alphabeta(boardCopy, remainingPiecesCopy, nextPieceCopy, depth + 1, a, b, False, turncount)
                                if (value.score <= currentMove.score):
                                    value.score = currentMove.score
                                    if (currentMove.locationInt==None):
                                        value.location = (i,j)
                                        value.locationInt = i + j*4
                                        value.nextPiece = nextPieceCopy
                                    else:
                                        value.location = currentMove.location
                                        value.locationInt = currentMove.locationInt
                                        value.nextPiece = currentMove.nextPiece

                                a = max(a, value)
                                if (a >= b):
                                    break
                            boardCopy[i,j] = None
                return value
            else:
                value = moveInfo(float('inf'),None,None,None)
                boardCopy = copy.deepcopy(board)
                for i in range(len(boardCopy)):
                    for j in range(len(boardCopy[i])):
                        if (boardCopy[i,j] == None):
                            boardCopy[i,j] = nextPiece

                            for k in range(len(remainingPieces)):
                                remainingPiecesCopy = copy.deepcopy(remainingPieces)
                                nextPieceCopy = remainingPiecesCopy[k]
                                remainingPiecesCopy.remove(nextPieceCopy)
                                currentMove = self.alphabeta(boardCopy, remainingPiecesCopy, nextPieceCopy, depth + 1, a, b, True, turncount)

                                if (value.score >= currentMove.score):
                                    value.score = currentMove.score
                                    if (currentMove.locationInt==None):
                                        value.location = (i,j)
                                        value.locationInt = i + j*4
                                        value.nextPiece = nextPieceCopy
                                    else:
                                        value.location = currentMove.location
                                        value.locationInt = currentMove.locationInt
                                        value.nextPiece = currentMove.nextPiece

                                b = min(b, value)
                                if (a >= b):
                                    break

                            boardCopy[i,j] = None
                return value


"""
Class containing the structure for moveInfo which is the return value for the AI
"""
class moveInfo():
    def __init__(self, score, location, locationInt, nextpiece):
        self.score = score
        self.location = location
        self.locationInt = locationInt
        self.nextPiece = nextpiece


"""
-------------------------------------------------------------------------------
This section implements scalable squares and general init of the screen.
If not called, the code will be dormant.
"""

"""
This class implements the terminal IO display. It has three fields --
two for output and one for input -- that it uses for player interaction.
Accessor methods are available for updating and reading values.
"""
class IOarea:
    """
    Sets up three text areas for:
    - PlayerLabel - player name prompt
    - InstructionLabel - what to do next
    - InstructioEntry - user entry
    Provides accessor methods. Messages to player are stored in a dictionary;
    accessed by key.
    Args:
    param @root - window to draw on
    param @x_start - x position to start drawing on
    param @y_start - y position to start drawing on
    """
    def __init__(self, root, x_start, y_start):

        #global PlayerLabel
        #global InstructionLabel
        #global InstructionEntry
        #global contents  # user entry

        self.outputTexts = {
            "instructionSelect1" : "Select piece to give away (number 1-16)\nand hit return. 0 terminates the game",
            "instructionSelect2" : "Select piece to give away (1-16)",
            "instructionError1" : "Nonexisting piece. Please choose a piece that is left (1-16)",
            "instructionError2" : "Nonexisting or taken tile. Please select a free tile number (1-16)",
            "instructionPlace1" : "Place offered piece on the board by selecting a tile number (1-16)",
            "instructionPlace2" : "",
            "winning" : "Winning move. Game ends.",
            "tie" : "Game is tied."
            }

        # Prompt for player (player 1 or 2)
        PlayerLabel = tk.Label(root, text="Player 1", font=("Helvetica", 14))
        PlayerLabel.place(x = x_start, y = (y_start + 25))
        self.PlayerLabel = PlayerLabel

        # Instructions to player
        InstructionLabel = tk.Label(root, text=self.outputTexts["instructionSelect1"], font=("Helvetica", 14), anchor="w")
        InstructionLabel.place(x=x_start, y=(y_start + 57))
        self.InstructionLabel = InstructionLabel
        contents = tk.IntVar()
        self.contents = contents

        # Players entry field
        InstructionEntry = tk.Entry(root, bd = 5, textvariable=contents, bg="snow", relief=tk.SUNKEN, font=("Helvetica", 14))
        InstructionEntry.place(x=x_start, y=(y_start + 95))
        self.InstructionEntry = InstructionEntry

        # Clear entry
        self.clearInstructionEntry()


    # Accessor methods

    # Used to prompt the next player with the name
    def updatePlayerLabel(self,txt):
        self.PlayerLabel.config(text=txt)

    # Used to prompt the player with next action (select/place)
    def updateInstructionLabel(self, key):
        txt = self.outputTexts[key]
        self.InstructionLabel.config(text=txt)

    # Returns the value entered by the player
    def getInstruction(self):
        return int(self.contents.get())

    # Clears the commend entered by the player
    def clearInstructionEntry(self):
        self.InstructionEntry.delete(first=0,last=10)



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
    side = 180  # Length of square side
    gap = 5     # Gap between the squares
    line = 2    # Extra slack between the squares

    # Resize window
    root.geometry(str(7 * (side + gap + line)) + "x" + str(6 * (side + gap + line)))

    # The two canvases that are created on the root window are
    # exported from this function
    global canvasGB
    global canvasNP

    # Next piece canvas
    xStartNP = side + gap + line + 10
    canvasNP = tk.Canvas(root, bg="light grey", relief=tk.RAISED)
    canvasNP.place(x=xStartNP, y=(4 * (side + gap + line) + 40), width=round(1.15 * side / 2), height=round(1.15 *side / 2))

    # Game Boad canvas
    xStartGB = side + gap + line +10
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

    # Canvas dimensions
    widthRP = 150
    heightRP = 890

    # Icon placement positions (a column)
    x_offset = 80  # x position of images
    delta_y = 50  # y distance between images (start at 0)

    # Remaining pieces canvas
    canvasRP = tk.Canvas(root, bg="light grey")
    canvasRP.place(x=10, y=0, width = widthRP, height = heightRP)

    # Set up locations for remaining pieces image locations
    imageLocationsRP = []
    for c in range(16):
        imageLocationsRP.append( [x_offset, 34 + delta_y * c] )

    # Set up icon locations in file system
    imagePaths = [
        tk.PhotoImage(file = path.dirname(__file__) + '/imgClr3/p' + str(i) + '.gif')
        for i in range(1, 17)
    ]

    # Set up dictionary with two sizes of respective image
    imagePaths = [
        {
            "regular": image,
            "medium" : image.subsample(2),
            "small": image.subsample(3),
            "tiny" : image.subsample(4)
        }
        for image in imagePaths
    ]

    # List with remaining pieces
    indexRemainingPieces = []
    # Draw icons in imageLocationsRP on canvas
    for c in range(16):
        indexRemainingPieces.append(canvasRP.create_image(imageLocationsRP[c], image=imagePaths[c]['tiny']))
        lbl = tk.Label(canvasRP, text=str(c + 1), font=("Helvetica", 14), anchor="center", bg="light grey", fg="dim grey")
        lbl.place(x=10, y=imageLocationsRP[c][1] - 25, width=30, height=50)

    return imagePaths, imageLocationsRP, indexRemainingPieces

@sio.on('init game')
def init_event(data):
    print("init board")
    """
    The game init values
    mostly startup of different canvases and GUI boxes
    aswell as creating a Game and AI
     - root is the main window that holds all the panes (called canvases)
    """
    root = tk.Tk()
    root.title("UU Game")
    root.geometry("1000x800")
    # GBheight is the height of the game squares canvas
    imageLocationsGB, GBheight = initGameScreen(root)
    imagePaths, imageLocationsRP, indexRemainingPieces = initRPcanvas(root)
    terminalIO = IOarea(root, 335, GBheight + 10)

    tictoc = Game(data.player1, data.player2, data.AI1, data.AI2)
    tictoc = Game(data['player1'], data['player2'], data['AI1'], data['AI2'])
    root.bind('<Return>', tictoc.EVENT_HANDLER)
    tictoc.canvasRPhandler("start",1)
    tictoc.GAME_TURN()

    root.pack_slaves()
    root.mainloop()