import Tkinter as tk
import numpy as np

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


def givePiece():
    global turncount
    global nextPiece
    for piece in range(0,16-turncount):
        if (remainingPieces[piece].id == contents.get()):
            nextPiece = remainingPieces[piece]
    InstructionEntry.delete(first=0,last=10)
    turncount =+ 1

def layPiece():
    global nextPiece
    global remainingPieces
    global board
    column = contents.get() % 4
    row = (contents.get() // 4) if (contents.get() > 3) else 1
    InstructionEntry.delete(first=0,last=10)
    board[row:column] = nextPiece
    remainingPieces.remove(nextPiece)


def EVENT_HANDLER(e):
    global event
    if (event == 2):
        givePiece()
        event = 1
        GAME_TURN()
    elif (event == 1):
        layPiece()
        event = 2
        GAME_TURN()
    else:
        quit


def GAME_TURN():
    global event
    global turncount
    if (event == 1):
        PlayerLabel.config(text='Player {}'.format(1 + turncount % 2))
        InstructionLabel.config(text='Where to place current piece 1-16:')

    elif (event == 2):
        PlayerLabel.config(text='Player {}'.format(1 + turncount % 2))
        InstructionLabel.config(text='Number of piece to give away 1-16:')


board = np.empty((4,4,))
board[:]
pieces = [Piece(1,"square","black","line",1),Piece(2,"square","black","line",0),Piece(3,"square","black","dotted",1),Piece(4,"square","black","dotted",0),Piece(5,"square","white","line",1),Piece(6,"square","white","line",0),Piece(7,"square","white","dotted",1),Piece(8,"square","white","dotted",0),
Piece(9,"round","black","line",1),Piece(10,"round","black","line",0),Piece(11,"round","black","dotted",1),Piece(12,"round","black","dotted",0),Piece(13,"round","white","line",1),Piece(14,"round","white","line",0),Piece(15,"round","white","dotted",1),Piece(16,"round","white","dotted",0)]
remainingPieces = pieces
turncount = 0
nextPiece = Piece(0, 0, 0, 0, 0)
event = 2

root = tk.Tk()
root.bind('<Return>', EVENT_HANDLER)
gameCanvas = tk.Canvas(root, bg="white", height=1031, width=1031)
gameCanvas.pack()

c1=gameCanvas.create_rectangle(5, 5, 255, 255, fill = 'light grey', width = 5)
c2=gameCanvas.create_rectangle(262, 5, 512, 255, fill = 'light grey', width = 5)
c3=gameCanvas.create_rectangle(519, 5, 769, 255, fill = 'light grey', width = 5)
c4=gameCanvas.create_rectangle(776, 5, 1026, 255, fill = 'light grey', width = 5)
c5=gameCanvas.create_rectangle(5, 262, 255, 512, fill = 'light grey', width = 5)
c6=gameCanvas.create_rectangle(262, 262, 512, 512, fill = 'light grey', width = 5)
c7=gameCanvas.create_rectangle(519, 262, 769, 512, fill = 'light grey', width = 5)
c8=gameCanvas.create_rectangle(776, 262, 1026, 512, fill = 'light grey', width = 5)
c9=gameCanvas.create_rectangle(5, 519, 255, 769, fill = 'light grey', width = 5)
c10=gameCanvas.create_rectangle(262, 519, 512, 769, fill = 'light grey', width = 5)
c11=gameCanvas.create_rectangle(519, 519, 769, 769, fill = 'light grey', width = 5)
c12=gameCanvas.create_rectangle(776, 519, 1026, 769, fill = 'light grey', width = 5)
c13=gameCanvas.create_rectangle(5, 776, 255, 1026, fill = 'light grey', width = 5)
c14=gameCanvas.create_rectangle(262, 776, 512, 1026, fill = 'light grey', width = 5)
c15=gameCanvas.create_rectangle(519, 776, 769, 1026, fill = 'light grey', width = 5)
c16=gameCanvas.create_rectangle(776, 776, 1026, 1026, fill = 'light grey', width = 5)
contents = tk.IntVar()
PlayerLabel = tk.Label(root, text="")
PlayerLabel.pack()
InstructionLabel = tk.Label(root, text="")
InstructionLabel.pack()
InstructionEntry = tk.Entry(root, bd = 5)
InstructionEntry["textvariable"] = contents
InstructionEntry.pack()

GAME_TURN()

root.mainloop()
