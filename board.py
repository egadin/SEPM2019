from Tkinter import *
import numpy as np

class piece:
    def __init__(id, shape, color, line, number):
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


def GAME_ENDED():
    for row in range(1,5):
        if ((board[1:row].shape == board[2:row].shape == board[3:row].shape == board[4:row].shape) and board[1:row] != nan or
        (board[1:row].color == board[2:row].color == board[3:row].color == board[4:row].color) and board[1:row] != nan or
        (board[1:row].line == board[2:row].line == board[3:row].line == board[4:row].line) and board[1:row] != nan or
        (board[1:row].number == board[2:row].number == board[3:row].number == board[4:row].number) and board[1:row] != nan):
            return True

    for col in range(1,5):
        if ((board[col:1].shape == board[col:2].shape == board[col:3].shape == board[col:4].shape) and board[1:row] != nan or
        (board[col:1].color == board[col:2].color == board[col:3].color == board[col:4].color) and board[1:row] != nan or
        (board[col:1].line == board[col:2].line == board[col:3].line == board[col:4].line) and board[1:row] != nan or
        (board[col:1].number == board[col:2].number == board[col:3].number == board[col:4].number) and board[1:row] != nan):
            return True

    if ((board[1:1].shape == board[2:2].shape == board[3:3].shape == board[4:4].shape) and board[1:1] != nan or
    (board[1:1].color == board[2:2].co1or == board[3:3].color == board[4:4].color) and board[1:1] != nan or
    (board[1:1].line == board[2:2].line == board[3:3].line == board[4:4].line) and board[1:1] != nan or
    (board[1:1].number == board[2:2].number == board[3:3].number == board[4:4].number) and board[1:1] != nan or
    (board[1:4].shape == board[2:3].shape == board[3:2].shape == board[4:1].shape) and board[4:1] != nan or
    (board[1:4].color == board[2:3].color == board[3:2].color == board[4:1].color) and board[4:1] != nan or
    (board[1:4].line == board[2:3].line == board[3:2].line == board[4:1].line) and board[4:1] != nan or
    (board[1:4].number == board[2:3].number == board[3:2].number == board[4:1].number) and board[4:1] != nan):
        return True

    else:
        return False

def GAME_TURN():
        def givePiece(event):
            for piece in pieces:
                if (piece.id == contents.get()):
                    nextPiece = contents.get()
            turncount =+ 1
            GAME_TURN()

        def layPiece(event):
            column = contents.get() % 4
            row = contents.get() / 4
            board[row : column] = nextPiece
            remainingPieces.remove(nextPiece)
            if (GAME_ENDED() == True):
                winner = 1 + turncount % 2

        if (turncount == 0):
            PlayerLabel.config(text='Player {}'.format(1 + turncount % 2))
            InstructionLabel.config(text='Number of piece to give away 1-16:')
            InstructionEntry.bind('<Return>', givePiece)

        else:
            PlayerLabel.config(text='Player {}'.format(1 + turncount % 2))
            InstructionLabel.config(text='Where to place current piece 1-16:')
            InstructionEntry.bind('<Return>', layPiece)
            InstructionLabel.config(text='Number of piece to give away 1-16:')
            InstructionEntry.bind('<Return>', givePiece)


board = np.empty((4,4,))
board[:]
pieces = [[1,"square","black","line",1],[2,"square","black","line",0],[3,"square","black","dotted",1],[4,"square","black","dotted",0],[5,"square","white","line",1],[6,"square","white","line",0],[7,"square","white","dotted",1],[8,"square","white","dotted",0],
[9,"round","black","line",1],[10,"round","black","line",0],[11,"round","black","dotted",1],[12,"round","black","dotted",0],[13,"round","white","line",1],[14,"round","white","line",0],[15,"round","white","dotted",1],[16,"round","white","dotted",0]]
remainingPieces = pieces
turncount = 0
nextPiece = piece

mainWindow = Tk()
canvas = Canvas(mainWindow, bg="white", height=2000, width=2000)
canvas.pack(side = RIGHT)
contents = StringVar()
PlayerLabel = Label(mainWindow, text="")
PlayerLabel.pack(side = LEFT)
InstructionLabel = Label(mainWindow, text="")
InstructionLabel.pack(side = LEFT)
InstructionEntry = Entry(mainWindow, bd = 5)
InstructionEntry["textvariable"] = contents
InstructionEntry.pack(side = RIGHT)
GAME_TURN()

mainWindow.mainloop()
