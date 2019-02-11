import Tkinter as tk
import numpy as np
from PIL import Image, ImageTk

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
        self.indexRemainingPieces = []

    def GAME_ENDED(self):
        for row in range(0,4):
            if (self.board[(0,row)] == None or self.board[(1,row)] == None or self.board[(2,row)] == None or self.board[(3,row)] == None):
                a = False
            else:
                if ((self.board[(0,row)].shape == self.board[(1,row)].shape == self.board[(2,row)].shape == self.board[(3,row)].shape) and self.board[(0,row)] or
                (self.board[(0,row)].color == self.board[(1,row)].color == self.board[(2,row)].color == self.board[(3,row)].color) and self.board[(0,row)] or
                (self.board[(0,row)].line == self.board[(1,row)].line == self.board[(2,row)].line == self.board[(3,row)].line) and self.board[(0,row)] or
                (self.board[(0,row)].number == self.board[(1,row)].number == self.board[(2,row)].number == self.board[(3,row)].number) and self.board[(0,row)]):
                    return True

        for col in range(0,4):
            if (self.board[col,0] == None or self.board[col,1] == None or self.board[col,2] == None or self.board[col,3] == None):
                a = False
            else:
                if ((self.board[(col,0)].shape == self.board[(col,1)].shape == self.board[(col,2)].shape == self.board[(col,3)].shape) and self.board[(0,row)] or
                (self.board[(col,0)].color == self.board[(col,1)].color == self.board[(col,2)].color == self.board[(col,3)].color) and self.board[(0,row)] or
                (self.board[(col,0)].line == self.board[(col,1)].line == self.board[(col,2)].line == self.board[(col,3)].line) and self.board[(0,row)] or
                (self.board[(col,0)].number == self.board[(col,1)].number == self.board[(col,2)].number == self.board[(col,3)].number) and self.board[(0,row)]):
                    return True

        if (self.board[(0,0)] == None or self.board[(1,1)] == None or self.board[(2,2)] == None or self.board[(3,3)] == None):
            a = False
        else:
            if ((self.board[(0,0)].shape == self.board[(1,1)].shape == self.board[(2,2)].shape == self.board[(3,3)].shape) and self.board[(0,0)] or
            (self.board[(0,0)].color == self.board[(1,1)].co0or == self.board[(2,2)].color == self.board[(3,3)].color) and self.board[(0,0)] or
            (self.board[(0,0)].line == self.board[(1,1)].line == self.board[(2,2)].line == self.board[(3,3)].line) and self.board[(0,0)] or
            (self.board[(0,0)].number == self.board[(1,1)].number == self.board[(2,2)].number == self.board[(3,3)].number) and self.board[(0,0)]):
                return True

        if (self.board[(0,3)] == None or self.board[(1,2)] == None or self.board[(2,1)] == None or self.board[(3,0)] == None):
            a = False
        else:
            if ((self.board[(0,3)].shape == self.board[(1,2)].shape == self.board[(2,1)].shape == self.board[(3,0)].shape) and self.board[(3,0)] or
            (self.board[(0,3)].color == self.board[(1,2)].color == self.board[(2,1)].color == self.board[(3,0)].color) and self.board[(3,0)] or
            (self.board[(0,3)].line == self.board[(1,2)].line == self.board[(2,1)].line == self.board[(3,0)].line) and self.board[(3,0)] or
            (self.board[(0,3)].number == self.board[(1,2)].number == self.board[(2,1)].number == self.board[(3,0)].number) and self.board[(3,0)]):
                return True

        if (a==False):
            return False


    def givePiece(self):
        for piece in range(0,16-self.turncount):
            if (self.remainingPieces[piece].id == contents.get()):
                self.nextPiece = self.remainingPieces[piece]  #nextpiece start as (0,0,0,0,0)
        InstructionEntry.delete(first=0,last=10)
        self.turncount += 1

    def layPiece(self):
        cont = contents.get() - 1
        column = cont % 4
        row = cont // 4
        InstructionEntry.delete(first=0,last=10)
        self.board[(row,column)] = self.nextPiece
        if(self.GAME_ENDED()==True):
            print("ended")
        self.remainingPieces.remove(self.nextPiece)
        self.remainingPiecesCanvashandler("delete", self.nextPiece.id)
        self.pieceCanvas(self.nextPiece.id, cont + 1)

    def pieceCanvas(self, id, canvas):
        global boardCanvas
        global imagePaths
        global imagePoints
        gameCanvas.create_image(imagePoints[canvas-1], image=imagePaths[id-1])

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

    def remainingPiecesCanvashandler(self, action, number):
        global remainingImagePoints
        global imagePaths
        global remainingPiecesCanvas
        if (action == "start"):
            r1 = remainingPiecesCanvas.create_image(remainingImagePoints[0], image=imagePaths[0])#.resize((60,60), Image.ANTIALIAS))
            r2 = remainingPiecesCanvas.create_image(remainingImagePoints[1], image=imagePaths[1])#.resize((60,60), Image.ANTIALIAS))
            r3 = remainingPiecesCanvas.create_image(remainingImagePoints[2], image=imagePaths[2])#.resize((60,60), Image.ANTIALIAS))
            r4 = remainingPiecesCanvas.create_image(remainingImagePoints[3], image=imagePaths[3])#.resize((60,60), Image.ANTIALIAS))
            r5 = remainingPiecesCanvas.create_image(remainingImagePoints[4], image=imagePaths[4])#.resize((60,60), Image.ANTIALIAS))
            r6 = remainingPiecesCanvas.create_image(remainingImagePoints[5], image=imagePaths[5])#.resize((60,60), Image.ANTIALIAS))
            r7 = remainingPiecesCanvas.create_image(remainingImagePoints[6], image=imagePaths[6])#.resize((60,60), Image.ANTIALIAS))
            r8 = remainingPiecesCanvas.create_image(remainingImagePoints[7], image=imagePaths[7])#.resize((60,60), Image.ANTIALIAS))
            r9 = remainingPiecesCanvas.create_image(remainingImagePoints[8], image=imagePaths[8])#.resize((60,60), Image.ANTIALIAS))
            r10 = remainingPiecesCanvas.create_image(remainingImagePoints[9], image=imagePaths[9])#.resize((60,60), Image.ANTIALIAS))
            r11 = remainingPiecesCanvas.create_image(remainingImagePoints[10], image=imagePaths[10])#.resize((60,60), Image.ANTIALIAS))
            r12 = remainingPiecesCanvas.create_image(remainingImagePoints[11], image=imagePaths[11])#.resize((60,60), Image.ANTIALIAS))
            r13 = remainingPiecesCanvas.create_image(remainingImagePoints[12], image=imagePaths[12])#.resize((60,60), Image.ANTIALIAS))
            r14 = remainingPiecesCanvas.create_image(remainingImagePoints[13], image=imagePaths[13])#.resize((60,60), Image.ANTIALIAS))
            r15 = remainingPiecesCanvas.create_image(remainingImagePoints[14], image=imagePaths[14])#.resize((60,60), Image.ANTIALIAS))
            r16 = remainingPiecesCanvas.create_image(remainingImagePoints[15], image=imagePaths[15])#.resize((60,60), Image.ANTIALIAS))
            self.indexRemainingPieces.append(r1)
            self.indexRemainingPieces.append(r2)
            self.indexRemainingPieces.append(r3)
            self.indexRemainingPieces.append(r4)
            self.indexRemainingPieces.append(r5)
            self.indexRemainingPieces.append(r6)
            self.indexRemainingPieces.append(r7)
            self.indexRemainingPieces.append(r8)
            self.indexRemainingPieces.append(r9)
            self.indexRemainingPieces.append(r10)
            self.indexRemainingPieces.append(r11)
            self.indexRemainingPieces.append(r12)
            self.indexRemainingPieces.append(r13)
            self.indexRemainingPieces.append(r14)
            self.indexRemainingPieces.append(r15)
            self.indexRemainingPieces.append(r16)
        elif (action == "delete"):
            print(number)
            print(self.indexRemainingPieces)
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

tictoc = Game("1", "2")


root = tk.Tk()
root.bind('<Return>', tictoc.EVENT_HANDLER)
gameCanvas = tk.Canvas(root, bg="white", height=1031, width=1031)
gameCanvas.place(x=301,y=0, width=1031, height=1031)
remainingPiecesCanvas = tk.Canvas(root, bg="light grey", height=1031, width=300)
remainingPiecesCanvas.place(x=0, y=0, width = 300, height = 1031)
remainingImagePoints = [[150,64],[150,128],[150,192],[150,256],[150,320],[150,384],[150,448],[150,512],[150,576],[150,640],[150,704],[150,768],[150,832],[150,896],[150,960],[150,1024]]

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
PlayerLabel.place(x = 500, y = 1050)
InstructionLabel = tk.Label(root, text="")
InstructionLabel.place(x= 500, y=1085)
PlayerLabel.config(text='{}'.format(tictoc.player1)) if ((1 + tictoc.turncount % 2) == 1) else PlayerLabel.config(text='{}'.format(tictoc.player2))
InstructionLabel.config(text='Number of piece to give away 1-16:')
InstructionEntry = tk.Entry(root, bd = 5)
InstructionEntry["textvariable"] = contents
InstructionEntry.place(x=500, y=1120)
tictoc.remainingPiecesCanvashandler("start",1)
tictoc.GAME_TURN

root.mainloop()
