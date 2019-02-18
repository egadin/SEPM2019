import Tkinter as tk
import numpy as np
import random
import copy
from PIL import Image, ImageTk
from os import path

class Game:
    def __init__(self, player1, player2, AI):
        global remainingPiecesCanvas
        global remainingImagePoints
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
        self.indexRemainingPieces = [remainingPiecesCanvas.create_image(remainingImagePoints[c], image=imagePaths[c]['small']) for c in range(16)]
        self.nextPieceImg = None
        self.AI = AI

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

    def givePiece(self):
        global nextPieceCanvas
        global imagePaths
        found = False
        for piece in range(0,16-self.turncount):
            if (self.remainingPieces[piece].id == contents.get()):
                self.nextPiece = self.remainingPieces[piece]  #nextpiece start as (0,0,0,0,0)
                found = True
                self.nextPieceImg = nextPieceCanvas.create_image([100,100], image=imagePaths[piece]['regular'])
        if (found == True):
            self.exception = False
            self.remainingPieces.remove(self.nextPiece)
            self.remainingPiecesCanvashandler("delete", self.nextPiece.id-1)
            InstructionEntry.delete(first=0,last=10)
            self.turncount += 1
        else:
            if (contents.get() == 0):
                self.event = 3
            else:
                self.exception = True
                InstructionEntry.delete(first=0,last=10)
                InstructionLabel.config(text='Nonexisting piece, please choose a piece that is left between 1-16:')

    def layPiece(self):
        global nextPieceCanvas
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
            self.pieceCanvas(self.nextPiece.id, cont + 1)
            nextPieceCanvas.delete(self.nextPieceImg)

    def pieceCanvas(self, id, canvas):
        global boardCanvas
        global imagePaths
        global imagePoints
        gameCanvas.create_image(imagePoints[canvas-1], image=imagePaths[id-1]['regular'])

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

    def AIturn(self):
        global nextPieceCanvas
        global imagePaths
        print(self.remainingPieces)
        AImove = self.AI.makeBestMove(self.board, self.remainingPieces, self.nextPiece) #skickar jag in riktiga eller copierar jag bara?
        print(self.remainingPieces)
        print(AImove.location)
        self.board[AImove.location] = self.nextPiece
        if(Game.GAME_ENDED(self.board)==True):
            print("ended")
        self.pieceCanvas(self.nextPiece.id, AImove.locationInt + 1)
        nextPieceCanvas.delete(self.nextPieceImg)
        self.nextPiece = AImove.nextPiece
        self.nextPieceImg = nextPieceCanvas.create_image([100,100], image=imagePaths[self.nextPiece.id - 1]['regular'])
        self.remainingPieces.remove(self.nextPiece)
        self.remainingPiecesCanvashandler("delete", self.nextPiece.id-1)
        self.turncount += 1
        self.event = 1
        self.GAME_TURN()

    def GAME_TURN(self):
        print(self.board)
        if (self.event == 1):
            PlayerLabel.config(text='{}'.format(self.player1)) if ((1 + self.turncount % 2) == 1) else PlayerLabel.config(text='{}'.format(self.player2))
            InstructionLabel.config(text='Where to place current piece 1-16:')

        elif (self.event == 2):
            PlayerLabel.config(text='{}'.format(self.player1)) if ((1 + self.turncount % 2) == 1) else PlayerLabel.config(text='{}'.format(self.player2))
            InstructionLabel.config(text='Number of piece to give away 1-16:')

    def remainingPiecesCanvashandler(self, action, number):
        global remainingPiecesCanvas
        if (action == "delete"):
            remainingPiecesCanvas.delete(self.indexRemainingPieces[number])

class Piece:
    def __init__(self, id, shape, color, line, number):
        self.id = id
        self.shape = shape
        self.color = color
        self.line = line
        self.number = number

class AI():
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def makeBestMove(self, board, remainingPiecesCopy, nextPieceCopy):
        rand = random.randint(1,11)
        if (self.difficulty == "easy"):
            if (rand > 1):
                locInfo = self.randomLocation(board)
                npInfo = self.randomNP(remainingPiecesCopy)
                return moveInfo(0, locInfo[0], locInfo[1], npInfo)
            else:
                return self.maxMove(0, board, remainingPiecesCopy, nextPieceCopy)

        elif (self.difficulty == "medium"):
            if (rand > 3):
                locInfo = self.randomLocation(board)
                npInfo = self.randomNP(remainingPiecesCopy)
                return moveInfo(0, locInfo[0], locInfo[1], npInfo)
            else:
                return self.maxMove(0, board, remainingPiecesCopy, nextPieceCopy)

        elif (self.difficulty == "hard"):
            if (rand > 7):
                locInfo = self.randomLocation(board)
                npInfo = self.randomNP(remainingPiecesCopy)
                return moveInfo(0, locInfo[0], locInfo[1], npInfo)
            else:
                return self.maxMove(0, board, remainingPiecesCopy, nextPieceCopy)

    def randomLocation(self, board):
        pieces = [(board[i % 4, i // 4], (i % 4, i // 4), i) for i in range(0, 15)]
        pieces = filter(lambda (piece, coord, loc): piece, pieces)

        piece = random.choice(pieces)

        return (piece[1], piece[2])

    def randomNP(self, remainingPiecesCopy):
        return remainingPiecesCopy[random.randint(0,len(remainingPiecesCopy)-1)]

    def maxMove(self, depth, board, remainingPieces, nextPiece):
        if depth > 1:
            locInfo = self.randomLocation(board)
            npInfo = self.randomNP(remainingPieces)
            return moveInfo(0, locInfo[0], locInfo[1], npInfo)

        boardCopy = copy.deepcopy(board)
        remainingPiecesCopy = copy.copy(remainingPieces)
        nextPieceCopy = copy.copy(nextPiece)
        if (Game.GAME_ENDED(boardCopy) == True):
            return moveInfo(depth-20,None,None,None)

        max = moveInfo(None,None,None,None)

        for i in range(len(boardCopy)):
            for j in range(len(boardCopy[i])):
                if (boardCopy[i,j] == None):
                    boardCopy[i,j] = nextPieceCopy

                    for k in range(len(remainingPiecesCopy)):
                        nextPieceCopy = remainingPiecesCopy[k]
                        remainingPiecesCopy.remove(nextPieceCopy)

                        currentMove = self.minMove(depth + 1, boardCopy, remainingPiecesCopy, nextPieceCopy)

                        if (currentMove.score > max):
                            max.score = currentMove.score
                            max.location = (i, j)
                            max.locationInt = (i*4 + j)
                            max.nextPiece = nextPieceCopy

                        remainingPiecesCopy.append(nextPieceCopy)

                    boardCopy[i,j] = None

        return max


    def minMove(self, depth, board, remainingPieces, nextPiece):
        if depth > 1:
            locInfo = self.randomLocation(board)
            npInfo = self.randomNP(remainingPieces)
            return moveInfo(0, locInfo[0], locInfo[1], npInfo)

        boardCopy = copy.deepcopy(board)
        remainingPiecesCopy = copy.copy(remainingPieces)
        nextPieceCopy = copy.copy(nextPiece)
        if (Game.GAME_ENDED(boardCopy) == True):
            return moveInfo(20-depth,None,None,None)

        min = moveInfo(float('inf'),None,None,None)

        for i in range(len(boardCopy)):
            for j in range(len(boardCopy[i])):
                if (boardCopy[i,j] == None):
                    boardCopy[i,j] = nextPieceCopy

                    for k in range(len(remainingPiecesCopy)):
                        nextPieceCopy = remainingPiecesCopy[k]
                        remainingPiecesCopy.remove(nextPieceCopy)

                        currentMove = self.maxMove(depth + 1, boardCopy, remainingPiecesCopy, nextPieceCopy)

                        if (currentMove.score < min):
                            min.score = currentMove.score
                            min.location = (i,j)
                            min.locationInt = (i*4 + j)
                            min.nextPiece = nextPieceCopy

                        remainingPiecesCopy.append(nextPieceCopy)

                    boardCopy[i,j] == None
        return min

class moveInfo():
    def __init__(self, score, location, locationInt, nextpiece):
        self.score = score
        self.location = location
        self.locationInt = locationInt
        self.nextPiece = nextpiece

root = tk.Tk()
gameCanvas = tk.Canvas(root, bg="white", height=1031, width=1031)
gameCanvas.place(x=301,y=0, width=1031, height=1031)
remainingPiecesCanvas = tk.Canvas(root, bg="light grey", height=1031, width=300)
remainingPiecesCanvas.place(x=0, y=0, width = 300, height = 1031)
remainingImagePoints = [[150,34],[150,98],[150,162],[150,226],[150,290],[150,354],[150,418],[150,482],[150,546],[150,610],[150,674],[150,738],[150,802],[150,866],[150,930],[150,994]]
nextPieceCanvas = tk.Canvas(root, bg="light grey", height=200, width=200)
nextPieceCanvas.place(x=100, y=1050, width = 200, height = 200)

for x in range(4):
    for y in range(4):
        gameCanvas.create_rectangle(
            5 + x * 257,
            5 + y * 257,
            255 + x * 257,
            255 + y * 257,
            fill = 'light grey',
            width = 5
        )

imagePoints = [[130,130],[387,130],[644,130],[901,130],[130,387],[387,387],[644,387],[901,387],[130,644],[387,644],[644,644],[901,644],[130,901],[387,901],[644,901],[901,901]]
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
tictoc.remainingPiecesCanvashandler("start",1)
tictoc.GAME_TURN()

root.pack_slaves()

root.mainloop()
