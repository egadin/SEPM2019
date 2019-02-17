import Tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from os import path

class Game:
    def __init__(self, player1, player2):
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

    def GAME_ENDED(self):
        for row in range(0,4):
            if (self.board[(0,row)] == None or self.board[(1,row)] == None or self.board[(2,row)] == None or self.board[(3,row)] == None):
                pass
            elif ((self.board[(0,row)].shape == self.board[(1,row)].shape == self.board[(2,row)].shape == self.board[(3,row)].shape) and self.board[(0,row)] or
                (self.board[(0,row)].color == self.board[(1,row)].color == self.board[(2,row)].color == self.board[(3,row)].color) and self.board[(0,row)] or
                (self.board[(0,row)].line == self.board[(1,row)].line == self.board[(2,row)].line == self.board[(3,row)].line) and self.board[(0,row)] or
                (self.board[(0,row)].number == self.board[(1,row)].number == self.board[(2,row)].number == self.board[(3,row)].number) and self.board[(0,row)]):
                    return True

        for col in range(0,4):
            if (self.board[col,0] == None or self.board[col,1] == None or self.board[col,2] == None or self.board[col,3] == None):
                pass
            elif ((self.board[(col,0)].shape == self.board[(col,1)].shape == self.board[(col,2)].shape == self.board[(col,3)].shape) and self.board[(0,row)] or
                (self.board[(col,0)].color == self.board[(col,1)].color == self.board[(col,2)].color == self.board[(col,3)].color) and self.board[(0,row)] or
                (self.board[(col,0)].line == self.board[(col,1)].line == self.board[(col,2)].line == self.board[(col,3)].line) and self.board[(0,row)] or
                (self.board[(col,0)].number == self.board[(col,1)].number == self.board[(col,2)].number == self.board[(col,3)].number) and self.board[(0,row)]):
                    return True

        if (self.board[(0,0)] == None or self.board[(1,1)] == None or self.board[(2,2)] == None or self.board[(3,3)] == None):
            pass
        elif ((self.board[(0,0)].shape == self.board[(1,1)].shape == self.board[(2,2)].shape == self.board[(3,3)].shape) and self.board[(0,0)] or
            (self.board[(0,0)].color == self.board[(1,1)].co0or == self.board[(2,2)].color == self.board[(3,3)].color) and self.board[(0,0)] or
            (self.board[(0,0)].line == self.board[(1,1)].line == self.board[(2,2)].line == self.board[(3,3)].line) and self.board[(0,0)] or
            (self.board[(0,0)].number == self.board[(1,1)].number == self.board[(2,2)].number == self.board[(3,3)].number) and self.board[(0,0)]):
                return True

        if (self.board[(0,3)] == None or self.board[(1,2)] == None or self.board[(2,1)] == None or self.board[(3,0)] == None):
            pass
        elif ((self.board[(0,3)].shape == self.board[(1,2)].shape == self.board[(2,1)].shape == self.board[(3,0)].shape) and self.board[(3,0)] or
            (self.board[(0,3)].color == self.board[(1,2)].color == self.board[(2,1)].color == self.board[(3,0)].color) and self.board[(3,0)] or
            (self.board[(0,3)].line == self.board[(1,2)].line == self.board[(2,1)].line == self.board[(3,0)].line) and self.board[(3,0)] or
            (self.board[(0,3)].number == self.board[(1,2)].number == self.board[(2,1)].number == self.board[(3,0)].number) and self.board[(3,0)]):
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
            if(self.GAME_ENDED()==True):
                print("ended")
            self.remainingPieces.remove(self.nextPiece)
            self.remainingPiecesCanvashandler("delete", self.nextPiece.id-1)
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
            self.layPiece()
            if (self.exception != True):
                self.event = 2
                self.GAME_TURN()
        elif (self.event == 3):
            quit


    def GAME_TURN(self):
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

    def id():
        doc = "The id property."
        def fget(self):
            return self._id
        def fset(self, value):
            self._id = value
        def fdel(self):
            del self._id
        return locals()
    id = property(**id())

    def shape():
        doc = "The shape property."
        def fget(self):
            return self._shape
        def fset(self, value):
            self._shape = value
        def fdel(self):
            del self._shape
        return locals()
    shape = property(**shape())

    def color():
        doc = "The color property."
        def fget(self):
            return self._color
        def fset(self, value):
            self._color = value
        def fdel(self):
            del self._color
        return locals()
    color = property(**color())

    def line():
        doc = "The line property."
        def fget(self):
            return self._line
        def fset(self, value):
            self._line = value
        def fdel(self):
            del self._line
        return locals()
    line = property(**line())

    def number():
        doc = "The number property."
        def fget(self):
            return self._number
        def fset(self, value):
            self._number = value
        def fdel(self):
            del self._number
        return locals()
    number = property(**number())

class AI():
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def makeBestMove(self, board, remainingPiecesCopy, nextPieceCopy):
        self.boardCopy = board
        self.remainingPiecesCopy = remainingPiecesCopy
        self.nextPieceCopy = nextPieceCopy

        return self.maxMove(0)

        def maxMove(self, depth):
            if (self.GAME_ENDED() == True):
                return moveInfo(20-depth,None,None)

            max = moveInfo(None,None,None)

            for i in range(len(self.boardCopy)):
                for j in range(len(self.boardCopy[i])):
                    if (self.boardCopy[i,j] == None):
                        self.boardCopy[i,j] = nextPieceCopy

                        for k in range(remainingPiecesCopy):
                            nextPieceCopy = remainingPiecesCopy[k]
                            remainingPiecesCopy.delete(nextPieceCopy)
                            currentMove = self.minMove(depth + 1)

                            if (currentMove.score > max):
                                max.score = currentMove.score
                                max.location = [i,j]
                                max.nextPiece = nextPieceCopy

                            remainingPiecesCopy.append(nextPieceCopy)

                        self.boardCopy[i,j] == None
            return max


        def minMove(self, depth):
            if (self.GAME_ENDED() == True):
                return moveInfo(depth-20,None,None)

            min = moveInfo(None,None,None)

            for i in range(len(self.boardCopy)):
                for j in range(len(self.boardCopy[i])):
                    if (self.boardCopy[i,j] == None):
                        self.boardCopy[i,j] = nextPieceCopy

                        for k in range(remainingPiecesCopy):
                            nextPieceCopy = remainingPiecesCopy[k]
                            remainingPiecesCopy.delete(nextPieceCopy)
                            currentMove = self.maxMove(depth + 1)

                            if (currentMove.score < min):
                                min.score = currentMove.score
                                min.location = [i,j]
                                min.nextPiece = nextPieceCopy

                            remainingPiecesCopy.append(nextPieceCopy)

                        self.boardCopy[i,j] == None
            return min

    def GAME_ENDED(self):
        for row in range(0,4):
            if (self.boardCopy[(0,row)] == None or self.boardCopy[(1,row)] == None or self.boardCopy[(2,row)] == None or self.boardCopy[(3,row)] == None):
                pass
            elif ((self.boardCopy[(0,row)].shape == self.boardCopy[(1,row)].shape == self.boardCopy[(2,row)].shape == self.boardCopy[(3,row)].shape) and self.boardCopy[(0,row)] or
                (self.boardCopy[(0,row)].color == self.boardCopy[(1,row)].color == self.boardCopy[(2,row)].color == self.boardCopy[(3,row)].color) and self.boardCopy[(0,row)] or
                (self.boardCopy[(0,row)].line == self.boardCopy[(1,row)].line == self.boardCopy[(2,row)].line == self.boardCopy[(3,row)].line) and self.boardCopy[(0,row)] or
                (self.boardCopy[(0,row)].number == self.boardCopy[(1,row)].number == self.boardCopy[(2,row)].number == self.boardCopy[(3,row)].number) and self.boardCopy[(0,row)]):
                    return True

        for col in range(0,4):
            if (self.boardCopy[col,0] == None or self.boardCopy[col,1] == None or self.boardCopy[col,2] == None or self.boardCopy[col,3] == None):
                pass
            elif ((self.boardCopy[(col,0)].shape == self.boardCopy[(col,1)].shape == self.boardCopy[(col,2)].shape == self.boardCopy[(col,3)].shape) and self.boardCopy[(0,row)] or
                (self.boardCopy[(col,0)].color == self.boardCopy[(col,1)].color == self.boardCopy[(col,2)].color == self.boardCopy[(col,3)].color) and self.boardCopy[(0,row)] or
                (self.boardCopy[(col,0)].line == self.boardCopy[(col,1)].line == self.boardCopy[(col,2)].line == self.boardCopy[(col,3)].line) and self.boardCopy[(0,row)] or
                (self.boardCopy[(col,0)].number == self.boardCopy[(col,1)].number == self.boardCopy[(col,2)].number == self.boardCopy[(col,3)].number) and self.boardCopy[(0,row)]):
                    return True

        if (self.boardCopy[(0,0)] == None or self.boardCopy[(1,1)] == None or self.boardCopy[(2,2)] == None or self.boardCopy[(3,3)] == None):
            pass
        elif ((self.boardCopy[(0,0)].shape == self.boardCopy[(1,1)].shape == self.boardCopy[(2,2)].shape == self.boardCopy[(3,3)].shape) and self.boardCopy[(0,0)] or
            (self.boardCopy[(0,0)].color == self.boardCopy[(1,1)].co0or == self.boardCopy[(2,2)].color == self.boardCopy[(3,3)].color) and self.boardCopy[(0,0)] or
            (self.boardCopy[(0,0)].line == self.boardCopy[(1,1)].line == self.boardCopy[(2,2)].line == self.boardCopy[(3,3)].line) and self.boardCopy[(0,0)] or
            (self.boardCopy[(0,0)].number == self.boardCopy[(1,1)].number == self.boardCopy[(2,2)].number == self.boardCopy[(3,3)].number) and self.boardCopy[(0,0)]):
                return True

        if (self.boardCopy[(0,3)] == None or self.boardCopy[(1,2)] == None or self.boardCopy[(2,1)] == None or self.boardCopy[(3,0)] == None):
            pass
        elif ((self.boardCopy[(0,3)].shape == self.boardCopy[(1,2)].shape == self.boardCopy[(2,1)].shape == self.boardCopy[(3,0)].shape) and self.boardCopy[(3,0)] or
            (self.boardCopy[(0,3)].color == self.boardCopy[(1,2)].color == self.boardCopy[(2,1)].color == self.boardCopy[(3,0)].color) and self.boardCopy[(3,0)] or
            (self.boardCopy[(0,3)].line == self.boardCopy[(1,2)].line == self.boardCopy[(2,1)].line == self.boardCopy[(3,0)].line) and self.boardCopy[(3,0)] or
            (self.boardCopy[(0,3)].number == self.boardCopy[(1,2)].number == self.boardCopy[(2,1)].number == self.boardCopy[(3,0)].number) and self.boardCopy[(3,0)]):
                return True

        return False

class moveInfo():
    def __init__(self, score, location, nextpiece):
        self.score = score
        self.location = location
        self.nextPiece = nextPiece



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

tictoc = Game("1", "2")

root.bind('<Return>', tictoc.EVENT_HANDLER)

PlayerLabel.config(text='{}'.format(tictoc.player1)) if ((1 + tictoc.turncount % 2) == 1) else PlayerLabel.config(text='{}'.format(tictoc.player2))
InstructionLabel.config(text='Number of piece to give away 1-16:')
InstructionEntry = tk.Entry(root, bd = 5)
InstructionEntry["textvariable"] = contents
InstructionEntry.place(x=500, y=1120)
tictoc.remainingPiecesCanvashandler("start",1)
tictoc.GAME_TURN

root.mainloop()
