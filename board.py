import Tkinter as tk
import numpy as np
import random
import copy
from PIL import Image, ImageTk
from os import path

"""
Game class param @player1 name of first player @player2 name of second player, @AI the Ai that should be used
global canvasRP the box where remaining pieces are shown
global imageLocationsRP the cords to the images in canvasRP
global imagePaths the img folder
"""
class Game:
    def __init__(self, player1, player2, AI):
        global canvasRP
        global imageLocationsRP
        global imagePaths
        self.board = np.full((4,4), None, dtype = np.object_)
        self.pieces = [Piece(1,"square","black","line",1),Piece(2,"square","black","line",0),Piece(3,"square","black","dotted",1),Piece(4,"square","black","dotted",0),Piece(5,"square","white","line",1),Piece(6,"square","white","line",0),Piece(7,"square","white","dotted",1),Piece(8,"square","white","dotted",0),
        Piece(9,"round","black","line",1),Piece(10,"round","black","line",0),Piece(11,"round","black","dotted",1),Piece(12,"round","black","dotted",0),Piece(13,"round","white","line",1),Piece(14,"round","white","line",0),Piece(15,"round","white","dotted",1),Piece(16,"round","white","dotted",0)]
        self.remainingPieces = self.pieces
        self.nextPiece = Piece(0,0,0,0,0)
        self.turncount = 0
        self.event = 2
        self.player1 = player1
        self.player2 = player2
        self.exception = False
        self.indexRemainingPieces = [canvasRP.create_image(imageLocationsRP[c], image=imagePaths[c]['small']) for c in range(16)]
        self.nextPieceImg = None
        self.AI = AI

    """
    Method to see if a game state is final
    checks for 4 in a row for all attributes in the board of choice
    param @board anythe board that should be checked
    """
    @staticmethod
    def GAME_ENDED(board):
            for prop in ['shape', 'color', 'line', 'number']:
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
    Method for a human player to give a piece to the opponent
    removes the piece from remaining pieces and moves it into the box showing next piece
    if user inputs 0 the game will end
    global canvasNP the box for next piece
    global imagePaths the img folder
    """
    def givePiece(self):
        global canvasNP
        global imagePaths
        found = False
        for piece in range(0,16-self.turncount):
            if (self.remainingPieces[piece].id == contents.get()):
                self.nextPiece = self.remainingPieces[piece]  #nextpiece start as (0,0,0,0,0)
                found = True
                self.nextPieceImg = canvasNP.create_image([100,100], image=imagePaths[piece]['regular'])
        if (found == True):
            self.exception = False
            self.remainingPieces.remove(self.nextPiece)
            self.canvasRPhandler("delete", self.nextPiece.id-1)
            InstructionEntry.delete(first=0,last=10)
            self.turncount += 1
        else:
            if (contents.get() == 0):
                self.event = 3
            else:
                self.exception = True
                InstructionEntry.delete(first=0,last=10)
                InstructionLabel.config(text='Nonexisting piece, please choose a piece that is left between 1-16:')

    """
    Method for a human player to lay a piece on the board
    removes the piece from next piece and moves it into the box showing the game board on the designated spot from the player
    checks if the game has ended
    global canvasNP the box for next piece
    """
    def layPiece(self):
        global canvasNP
        cont = contents.get() - 1
        column = cont % 4
        row = cont // 4
        if (cont < -1 or cont >= 16 or self.board[row,column] != None):
            self.exception = True
            InstructionEntry.delete(first=0,last=10)
            InstructionLabel.config(text='Nonexisting or taken tile please enter free tile between 1-16:')
        elif (cont == -1):
            self.event = 3
        else:
            self.exception = False
            InstructionEntry.delete(first=0,last=10)
            self.board[row,column] = self.nextPiece
            if(Game.GAME_ENDED(self.board)==True):
                print("ended")
            self.pieceCanvas(self.nextPiece.id, cont)
            canvasNP.delete(self.nextPieceImg)

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

    """
    The central game cordinator, gets called on user inputs and sends out calls to
    the correct methods to continue the game
    calls on the AI if a player is None
    event 3 is quit and fets called when a player inputs 0 in givePiece function
    """
    def EVENT_HANDLER(self, e):
        if (self.event == 2):
            self.givePiece()
            if (self.exception != True):
                self.event = 1
                self.GAME_TURN()
        elif (self.event == 1):
            if (((1 + self.turncount % 2) != 1) and self.player2 == None):
                self.AIturn()
            else:
                self.layPiece()
                if (self.exception != True):
                    self.event = 2
                    self.GAME_TURN()
        elif (self.event == 3):
            quit

    """
    Calling the alpha beta AI for cords and a next piece
    execute a turn without taking inputs and using the info from the AI instead
    global canvasNP box for the next piece
    global imagePaths the img folder
    """
    def AIturn(self):
        global canvasNP
        global imagePaths
        AImove = self.AI.makeBestMove(self.board, self.remainingPieces, self.nextPiece) #skickar jag in riktiga eller copierar jag bara?
        print(AImove.location, AImove.score)
        self.board[AImove.location] = self.nextPiece
        print(self.board)
        if(Game.GAME_ENDED(self.board)==True):
            print("ended")
        self.pieceCanvas(self.nextPiece.id, AImove.location[0]*4 + AImove.location[1])
        canvasNP.delete(self.nextPieceImg)
        self.nextPiece = AImove.nextPiece
        self.nextPieceImg = canvasNP.create_image([100,100], image=imagePaths[self.nextPiece.id - 1]['regular'])
        self.remainingPieces.remove(self.nextPiece)
        self.canvasRPhandler("delete", self.nextPiece.id-1)
        self.turncount += 1
        self.event = 1
        self.GAME_TURN()

    """
    Updating user interface box with current players name and which instruction is given
    acting as a stall state while waiting for users input as to which EVENT_HANDLER is called
    """
    def GAME_TURN(self):
        if (self.event == 1):
            PlayerLabel.config(text='{}'.format(self.player1)) if ((1 + self.turncount % 2) == 1) else PlayerLabel.config(text='{}'.format(self.player2))
            InstructionLabel.config(text='Where to place current piece (1-16):')

        elif (self.event == 2):
            PlayerLabel.config(text='{}'.format(self.player1)) if ((1 + self.turncount % 2) == 1) else PlayerLabel.config(text='{}'.format(self.player2))
            InstructionLabel.config(text='Number of piece to give away (1-16):')

    """
    Options for canvasRP supports delete as of now since it's initiated elsewhere
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

"""
Class containing the AI which is based on minMax algorithm with alpha beta prouning
holds information about what difficulty you want to play on
otherwise it takes in the required information in it's functions to make a move absed on the current playing field
param @difficulty the difficulty you want to playy on in string format
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
    def makeBestMove(self, board, remainingPiecesCopy, nextPieceCopy):
        rand = 1 #random.randint(1,11)
        boardCopy = copy.deepcopy(board)

        if (self.difficulty == "easy"):
            if (rand > 1):
                locInfo = self.randomLocation(board)
                npInfo = self.randomNP(remainingPiecesCopy)
                return moveInfo(0, locInfo[0], locInfo[1], npInfo)
            else:
                return self.alphabeta(boardCopy, remainingPiecesCopy, nextPieceCopy, 0, float('-inf'), float('inf'), True)

        elif (self.difficulty == "medium"):
            if (rand > 3):
                locInfo = self.randomLocation(board)
                npInfo = self.randomNP(remainingPiecesCopy)
                return moveInfo(0, locInfo[0], locInfo[1], npInfo)
            else:
                return self.alphabeta(boardCopy, remainingPiecesCopy, nextPieceCopy, 0, float('-inf'), float('inf'), True)

        elif (self.difficulty == "hard"):
            if (rand > 7):
                locInfo = self.randomLocation(board)
                npInfo = self.randomNP(remainingPiecesCopy)
                return moveInfo(0, locInfo[0], locInfo[1], npInfo)
            else:
                return self.alphabeta(boardCopy, remainingPiecesCopy, nextPieceCopy, 0, float('-inf'), float('inf'), True)

    """
    Randomizes a location on the gameboard from all the empty tiles
    and returns it's cordinates
    param @board the current gameboard
    """
    def randomLocation(self, board):
        pieces = [(board[i % 4, i // 4], (i % 4, i // 4), i) for i in range(0, 15)]
        pieces = filter(lambda (piece, coord, loc): piece is None, pieces)
        piece = random.choice(pieces)
        return (piece[1], piece[2])

    """
    Randomizes a piece to give to the opponent from the remaining pieces array
    param @remainingPiecesCopy the array holding the remaining pieceCanvas
    """
    def randomNP(self, remainingPiecesCopy):
        return remainingPiecesCopy[random.randint(0,len(remainingPiecesCopy)-1)]

    """
    The minMax algorithm with alpha beta prouning
    iterates down through all possible solutions that doesn't get prouned and scores them if they are within a certain search depth
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
    def alphabeta(self, board, remainingPiecesCopy, nextPieceCopy, depth, a, b, maximizingPlayer):
        #if (depth > 10):
        #   print("rand")
        #   locInfo = self.randomLocation(board)
        #   npInfo = self.randomNP(remainingPiecesCopy)
        #   return moveInfo(0, locInfo[0], locInfo[1], npInfo)
        print(board)
        if (Game.GAME_ENDED(board)):
            if (maximizingPlayer):
                return moveInfo(20-depth, None,None,None)
            else:
                return moveInfo(depth-20,None,None,None)
        elif (remainingPiecesCopy == []):
            return moveInfo(0,None,None,None)

        if (maximizingPlayer):
            boardCopy = copy.deepcopy(board)
            value = moveInfo(float('-inf'),None,None,None)
            for i in range(len(boardCopy)):
                for j in range(len(boardCopy[i])):
                    if (boardCopy[i,j] == None):
                        boardCopy[i,j] = nextPieceCopy

                        for k in range(len(remainingPiecesCopy)):
                            nextPieceCopy = remainingPiecesCopy[k]
                            remainingPiecesCopy.remove(nextPieceCopy)
                            currentMove = self.alphabeta(boardCopy, remainingPiecesCopy, nextPieceCopy, depth + 1, a, b, False)
                            if (value.score <= currentMove.score):
                                value.score = currentMove.score
                                value.location = (i,j)
                                value.locationInt = i + j*4
                                value.nextPiece = nextPieceCopy
                            remainingPiecesCopy.append(nextPieceCopy)

                            a = max(a, value)
                            if (a >= b):
                                break
                        boardCopy[i,j] == None

            return value
        else:
            boardCopy = copy.deepcopy(board)
            value = moveInfo(float('inf'),None,None,None)
            for i in range(len(boardCopy)):
                for j in range(len(boardCopy[i])):
                    if (boardCopy[i,j] == None):
                        boardCopy[i,j] = nextPieceCopy

                        for k in range(len(remainingPiecesCopy)):
                            nextPieceCopy = remainingPiecesCopy[k]
                            remainingPiecesCopy.remove(nextPieceCopy)
                            currentMove = self.alphabeta(boardCopy, remainingPiecesCopy, nextPieceCopy, depth + 1, a, b, True)
                            if (value.score >= currentMove.score):
                                value.score = currentMove.score
                                value.location = (i,j)
                                value.locationInt = i + j*4
                                value.nextPiece = nextPieceCopy
                            remainingPiecesCopy.append(nextPieceCopy)

                            b = min(b, value)
                            if (a >= b):
                                break
                        boardCopy[i,j] == None

            return value


#    def maxMove(self, depth, boardCopy, remainingPieces, nextPiece):
#        print("max")
#        if depth > 15:
#            print("rand")
#            locInfo = self.randomLocation(boardCopy)
#            npInfo = self.randomNP(remainingPieces)
#            return moveInfo(0, locInfo[0], locInfo[1], npInfo)
#
#        remainingPiecesCopy = copy.copy(remainingPieces)
#        nextPieceCopy = copy.copy(nextPiece)
#        if (Game.GAME_ENDED(boardCopy) == True):
#            return moveInfo(20-depth,None,None,None)
#
#        max = moveInfo(float('-inf'),None,None,None)
#
#        for i in range(len(boardCopy)):
#            for j in range(len(boardCopy[i])):
#                if (boardCopy[i,j] == None):
#                    boardCopy[i,j] = nextPieceCopy
#
#                    for k in range(len(remainingPiecesCopy)):
#                        nextPieceCopy = remainingPiecesCopy[k]
#                        remainingPiecesCopy.remove(nextPieceCopy)
#
#                        currentMove = self.minMove(depth + 1, boardCopy, remainingPiecesCopy, nextPieceCopy)
#                        print(currentMove.score)
#                        if (currentMove.score > max.score):
#                            max.score = currentMove.score
#                            max.location = (i, j)
#                            max.locationInt = i*4 + j
#                            max.nextPiece = nextPieceCopy
#
#                        remainingPiecesCopy.append(nextPieceCopy)
#
#                    boardCopy[i,j] = None
#
#        return max
#
#
#    def minMove(self, depth, boardCopy, remainingPieces, nextPiece):
#        print("min")
#        if depth > 15:
#            print("rand")
#
#
#
#        remainingPiecesCopy = copy.copy(remainingPieces)
#        nextPieceCopy = copy.copy(nextPiece)
#        if (Game.GAME_ENDED(boardCopy) == True):
#            return moveInfo(depth-20,None,None,None)
#
#        min = moveInfo(float('inf'),None,None,None)
#
#        for i in range(len(boardCopy)):
#            for j in range(len(boardCopy[i])):
#                if (boardCopy[i,j] == None):
#                    boardCopy[i,j] = nextPieceCopy
#
#                    for k in range(len(remainingPiecesCopy)):
#                        nextPieceCopy = remainingPiecesCopy[k]
#                        remainingPiecesCopy.remove(nextPieceCopy)
#
#                        currentMove = self.maxMove(depth + 1, boardCopy, remainingPiecesCopy, nextPieceCopy)
#                        print(currentMove.score)
#                        if (currentMove.score < min.score):
#                            min.score = currentMove.score
#                            min.location = (i,j)
#                            min.locationInt = i*4 + j
#                            min.nextPiece = nextPieceCopy
#
#                        remainingPiecesCopy.append(nextPieceCopy)
#                    boardCopy[i,j] == None
#        print(min.score)
#        return min

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
The game init values
mostly startup of different canvases and GUI boxes
aswell as creating a Game and AI
"""
root = tk.Tk()
canvasGB = tk.Canvas(root, bg="white", height=1031, width=1031)
canvasGB.place(x=301,y=0, width=1031, height=1031)
canvasRP = tk.Canvas(root, bg="light grey", height=1031, width=300)
canvasRP.place(x=0, y=0, width = 300, height = 1031)
imageLocationsRP = [[150,34],[150,98],[150,162],[150,226],[150,290],[150,354],[150,418],[150,482],[150,546],[150,610],[150,674],[150,738],[150,802],[150,866],[150,930],[150,994]]
canvasNP = tk.Canvas(root, bg="light grey", height=200, width=200)
canvasNP.place(x=100, y=1050, width = 200, height = 200)

for x in range(4):
    for y in range(4):
        canvasGB.create_rectangle(
            5 + x * 257,
            5 + y * 257,
            255 + x * 257,
            255 + y * 257,
            fill = 'light grey',
            width = 5
        )

imageLocationsGB = [[130,130],[387,130],[644,130],[901,130],[130,387],[387,387],[644,387],[901,387],[130,644],[387,644],[644,644],[901,644],[130,901],[387,901],[644,901],[901,901]]
imagePaths = [
    tk.PhotoImage(file = path.dirname(__file__) + '/img/p' + str(i) + '.gif')
    for i in range(1, 17)
]
imagePaths = [
    {
        "regular": image,
        "small": image.subsample(3)
    }
    for image in imagePaths
]
contents = tk.IntVar()
PlayerLabel = tk.Label(root, text="")
PlayerLabel.place(x = 500, y = 1050)
InstructionLabel = tk.Label(root, text="")
InstructionLabel.place(x= 500, y=1085)

tictocAI = AI("easy")
tictoc = Game("1", None, tictocAI)
root.bind('<Return>', tictoc.EVENT_HANDLER)

PlayerLabel.config(text='{}'.format(tictoc.player1)) if ((1 + tictoc.turncount % 2) == 1) else PlayerLabel.config(text='{}'.format(tictoc.player2))
InstructionLabel.config(text='Number of piece to give away 1-16:')
InstructionEntry = tk.Entry(root, bd = 5)
InstructionEntry["textvariable"] = contents
InstructionEntry.place(x=500, y=1120)
tictoc.canvasRPhandler("start",1)
tictoc.GAME_TURN()

root.pack_slaves()

root.mainloop()
