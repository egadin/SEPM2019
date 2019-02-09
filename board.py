import Tkinter as tk
import numpy as np

class Game:
    def __init__(self, player1, player2):
        self.board = np.full((4,4), None, dtype = np.object_)
        self.pieces = [Piece(1,"square","black","line",1),Piece(2,"square","black","line",0),Piece(3,"square","black","dotted",1),Piece(4,"square","black","dotted",0),Piece(5,"square","white","line",1),Piece(6,"square","white","line",0),Piece(7,"square","white","dotted",1),Piece(8,"square","white","dotted",0),
        Piece(9,"round","black","line",1),Piece(10,"round","black","line",0),Piece(11,"round","black","dotted",1),Piece(12,"round","black","dotted",0),Piece(13,"round","white","line",1),Piece(14,"round","white","line",0),Piece(15,"round","white","dotted",1),Piece(16,"round","white","dotted",0)]
        self.remainingPieces = self.pieces
        self.nextPiece = Piece(0,0,0,0,0)
        self.turncount = 0
        self.event = 2
        self.player1 = player1
        self.player2 = player2
        self.filledcanvas = []

    def GAME_ENDED(self):
        for row in range(1,5):
            if ((board[(1,row)].shape == board[(2,row)].shape == board[(3,row)].shape == board[(4,row)].shape) and board[(1,row)] != NAN or
            (board[(1,row)].color == board[(2,row)].color == board[(3,row)].color == board[(4,row)].color) and board[(1,row)] != NAN or
            (board[(1,row)].line == board[(2,row)].line == board[(3,row)].line == board[(4,row)].line) and board[(1,row)] != NAN or
            (board[(1,row)].number == board[(2,row)].number == board[(3,row)].number == board[(4,row)].number) and board[(1,row)] != NAN):
                return True

        for col in range(1,5):
            if ((board[(col,1)].shape == board[(col,2)].shape == board[(col,3)].shape == board[(col,4)].shape) and board[(1,row)] != NAN or
            (board[(col,1)].color == board[(col,2)].color == board[(col,3)].color == board[(col,4)].color) and board[(1,row)] != NAN or
            (board[(col,1)].line == board[(col,2)].line == board[(col,3)].line == board[(col,4)].line) and board[(1,row)] != NAN or
            (board[(col,1)].number == board[(col,2)].number == board[(col,3)].number == board[(col,4)].number) and board[(1,row)] != NAN):
                return True

        if ((board[(1,1)].shape == board[(2,2)].shape == board[(3,3)].shape == board[(4,4)].shape) and board[(1,1)] != NAN or
        (board[(1,1)].color == board[(2,2)].co1or == board[(3,3)].color == board[(4,4)].color) and board[(1,1)] != NAN or
        (board[(1,1)].line == board[(2,2)].line == board[(3,3)].line == board[(4,4)].line) and board[(1,1)] != NAN or
        (board[(1,1)].number == board[(2,2)].number == board[(3,3)].number == board[(4,4)].number) and board[(1,1)] != NAN or
        (board[(1,4)].shape == board[(2,3)].shape == board[(3,2)].shape == board[(4,1)].shape) and board[(4,1)] != NAN or
        (board[(1,4)].color == board[(2,3)].color == board[(3,2)].color == board[(4,1)].color) and board[(4,1)] != NAN or
        (board[(1,4)].line == board[(2,3)].line == board[(3,2)].line == board[(4,1)].line) and board[(4,1)] != NAN or
        (board[(1,4)].number == board[(2,3)].number == board[(3,2)].number == board[(4,1)].number) and board[(4,1)] != NAN):
            return True

        else:
            return False


    def givePiece(self):
        for piece in range(0,16-self.turncount):
            if (self.remainingPieces[piece].id == contents.get()):
                self.nextPiece = self.remainingPieces[piece]  #nextpiece start as (0,0,0,0,0)
        InstructionEntry.delete(first=0,last=10)
        self.turncount += 1

    def layPiece(self):
        cont = contents.get()
        column = cont % 4
        row = (cont // 4) if (cont > 3) else 1
        InstructionEntry.delete(first=0,last=10)
        self.board[(row,column)] = self.nextPiece
        self.remainingPieces.remove(self.nextPiece)
        self.pieceCanvas(self.nextPiece.id, cont)

    def pieceCanvas(self, id, canvas):
        global boardCanvas
        global imagePaths
        gameCanvas.create_image(imagePoints[canvas-1], image=imagePaths[canvas-1])
        self.filledcanvas.extend(canvas)

    def EVENT_HANDLER(self, e):
        if (self.event == 2):
            self.givePiece()
            self.event = 1
            self.GAME_TURN()
        elif (self.event == 1):
            self.layPiece()
            self.event = 2
            self.GAME_TURN()
        else:
            quit


    def GAME_TURN(self):
        if (self.event == 1):
            PlayerLabel.config(text='{}'.format(self.player1)) if ((1 + self.turncount % 2) == 1) else PlayerLabel.config(text='{}'.format(self.player2))
            InstructionLabel.config(text='Where to place current piece 1-16:')

        elif (self.event == 2):
            PlayerLabel.config(text='{}'.format(self.player1)) if ((1 + self.turncount % 2) == 1) else PlayerLabel.config(text='{}'.format(self.player2))
            InstructionLabel.config(text='Number of piece to give away 1-16:')


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

tictoc = Game("1", "2")


root = tk.Tk()
root.bind('<Return>', tictoc.EVENT_HANDLER)
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
imagePoints = [[130,130],[387,130],[644,130],[901,130],[130,387],[387,387],[644,387],[901,387],[130,644],[387,644],[644,644],[901,644],[130,901],[387,901],[644,901],[901,901]]
photo1 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p1.gif')
photo2 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p2.gif')
photo3 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p3.gif')
photo4 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p4.gif')
photo5 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p5.gif')
photo6 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p6.gif')
photo7 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p7.gif')
photo8 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p8.gif')
photo9 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p9.gif')
photo10 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p10.gif')
photo11 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p11.gif')
photo12 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p12.gif')
photo13 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p13.gif')
photo14 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p14.gif')
photo15 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p15.gif')
photo16 = tk.PhotoImage(file = '/home/erik/Documents/skola/SEPM/SEPM2019/img/p16.gif')
imagePaths = [photo1, photo2, photo3, photo4, photo5, photo6, photo7, photo8, photo9, photo10, photo11, photo12, photo13, photo14, photo15, photo16]
contents = tk.IntVar()
PlayerLabel = tk.Label(root, text="")
PlayerLabel.pack()
InstructionLabel = tk.Label(root, text="")
InstructionLabel.pack()
PlayerLabel.config(text='{}'.format(tictoc.player1)) if ((1 + tictoc.turncount % 2) == 1) else PlayerLabel.config(text='{}'.format(tictoc.player2))
InstructionLabel.config(text='Number of piece to give away 1-16:')
InstructionEntry = tk.Entry(root, bd = 5)
InstructionEntry["textvariable"] = contents
InstructionEntry.pack()

tictoc.GAME_TURN

root.mainloop()
