#!/usr/bin/python

"""
This implements the welcome page for the UU-GAME game portal.

(c) 2019 SEPM Group G
"""
import tkinter as tk # tkinter in Py3
from tkinter import messagebox  # used for error messages Py3
#import tkMessageBox
#

# Imported from server
class gamelobby:
    def __init__(self, player1id, player2id, player1, player2, winner, room):
        self.id = id
        self.player1id = player1id
        self.player2id = player2id
        self.player1 = player1
        self.player2 = player2
        self.winner = winner
        self.room = room

    def getPlayer1Name(self):
        if (self.player1 == None):
            return "None"
        else:
            return self.player1

    def getPlayer2Name(self):
        if (self.player2 == None):
            return "None"
        else:
            return self.player2

    """
    Intended to provide more than the name, as a string
    """
    def getPlayer1info(self):
        return self.getPlayer1Name()

    def getPlayer2info(self):
        return self.getPlayer2Name()



class waitingGamesListBox:
    def __init__(self, portal, xPos, yPos):
        # Get canvas to draw on
        win = portal.canvas
        # Define scrollbar
        scrollbar = tk.Scrollbar(win, orient="vertical")
        scrollbar.pack( side = tk.RIGHT, fill = "y" )
        # Define listbox, add scrollbar update command
        waitingGamesLb = tk.Listbox(win, yscrollcommand = scrollbar.set, font=("Helvetica", 12))
        waitingGamesLb.place(x = xPos, y = yPos)
        # Add listbox update command
        scrollbar.config(command = waitingGamesLb.yview)
        # Add list box as attribute of this instance
        self.listBox = waitingGamesLb
        # List with all waiting games
        self.gamesList = []

        waitingGamesLb.bind('<<ListboxSelect>>', self.listBoxCallback)

    """
    param @gamesList contains the following objects as elements:
    class gamelobby:
        self.id = id
        self.player1id = player1id
        self.player2id = player2id
        self.player1 = player1
        self.player2 = player2
        self.winner = winner
        self.room = room
    """
    def update(self,gamesList):
        for aGame in gamesList:
            self.listBox.insert(tk.END, aGame.player1)
        self.gamesList = gamesList

    """
    Adds a gameLobby (a waiting game)
    param @aGame -- the game lobby to be added
    """
    def addGame(self, aGame):
        self.listBox.insert(tk.END, aGame.player1)
        self.gamesList.append(aGame)

    """
    Deletes a gameLobby (a waiting game)
    param @aGame -- the game lobby (a waiting game) to be deleted
    """
    def deleteGame(self, aGame):
        for i in range(len(self.gamesList)):
            if (self.gamesList[i] == aGame):
                self.listBox.delete(i)
                self.gamesList.pop(i)

    def listBoxCallback(self, clickEvent):
        # Save selected game
        self.portal.selectedWaitingGameNumber = self.listBox.curselection()
        # self.portal has a button that needs enabling
        self.portal.joinGameButton.config(state=tk.NORMAL)



class complexDialog:
    def __init__(self, subSelf):
        # Create dialog window, called "root"
        root = tk.Tk()

        # width x height
        root.geometry("620x450")
        root.resizable(0, 0)  # Don't allow resizing in the x or y direction

        # Start corordinates
        self.leftMarginPos = 10
        self.topMarginPos = 10
        # Window background color
        self.winBGcolor = "light grey"
        canvas = tk.Canvas(root, bg=self.winBGcolor)
        # Make it larger than needed
        canvas.place(x=0, y=0, width=1031, height=1031)
        self.win = root



"""
Implements new game dialog
param @portal the launching object, a portalScreen
"""
class newGameDialog(complexDialog):

    def __init__(self, portal):
        super().__init__(self)

        self.win.geometry("540x300")
        self.player1ButtonTopPos = 70
        self.player2ButtonTopPos = 140

        # Use local variable for the texts
        portalTexts = portal.texts
        # Store launching portal as an attribute
        self.portal = portal
        # Dialog window header text
        self.win.title(portalTexts["newDlgHead"])

        # Prompt text for player 1
        promptText1 = tk.Label(self.win, anchor="center", font=("Helvetica", 14), text=portalTexts["actPrompt1"])
        promptText1.place(x=self.leftMarginPos, y=self.topMarginPos, width=520, height=40)

        # Left label for player 1
        promptText1 = tk.Label(self.win, anchor=tk.CENTER, font=("Helvetica", 14), text=portalTexts["pl1"], bg="light steel blue")
        promptText1.place(x=self.leftMarginPos, y=self.player1ButtonTopPos, height=60, width=150)

        # Player 1 name
        namePrompt1 = tk.Label(self.win, anchor="w", font=("Helvetica", 14), text=portalTexts["name"], bg = self.winBGcolor)
        namePrompt1.place(x=(self.leftMarginPos + 165), y=self.player1ButtonTopPos)

        # Player 1 name variable
        self.player1name = tk.StringVar()
        # player1name.set("Player 1 name")

        # Player 1 name entry field
        player1nameWidget = tk.Entry(self.win, bg="snow", font=("Helvetica", 14), relief=tk.SUNKEN,
                                     textvariable=self.player1name)
        player1nameWidget.place(x=(self.leftMarginPos + 240), y=self.player1ButtonTopPos, width=280)
        self.player1nameWidget = player1nameWidget

        # Selection of second player
        # Left label for player 2
        promptText2 = tk.Label(self.win, anchor=tk.CENTER, font=("Helvetica", 14), text=portalTexts["pl2"], bg="light steel blue")
        promptText2.place(x=self.leftMarginPos, y=self.player2ButtonTopPos, height=60, width=150)

        # Create variable to hold player 2 selection (1 or 2)
        self.rb2value = tk.IntVar()
        # Radio buttons for opponent selection
        rButton3 = tk.Radiobutton(self.win, text=portalTexts["humanPl"], font=("Helvetica", 14), variable=self.rb2value,
                                    value=1, command=self.rb2callback, bg = self.winBGcolor)
        rButton3.place(x=(self.leftMarginPos + 160), y=(self.player2ButtonTopPos - 3))
        rButton3.select()
        rButton4 = tk.Radiobutton(self.win, text=portalTexts["compPl"], font=("Helvetica", 14), variable=self.rb2value,
                                    value=2, command=self.rb2callback, bg = self.winBGcolor)
        rButton4.place(x=(self.leftMarginPos + 160), y=(self.player2ButtonTopPos + 26))

        # Player 2 AI level
        ai2value = tk.StringVar()
        self.player2AIlevelWidget = tk.Spinbox(self.win, font=("Helvetica", 14), textvariable=ai2value, values=("easy", "medium", "hard"))
        self.player2AIlevelWidget.place(x=(self.leftMarginPos + 420), y=(self.player2ButtonTopPos + 30), width=100)
        # Initially disable
        self.player2AIlevelWidget.config(state=tk.DISABLED)

        # Cancel button
        cancelDlgButton = tk.Button(self.win, command=self.cancelDlgCallback, font=("Helvetica", 14),
                                    text=portalTexts["cancelLbl"])
        cancelDlgButton.place(x=(self.leftMarginPos + 300), y=(self.player2ButtonTopPos + 100), width=100)

        # Start button
        startGameButton = tk.Button(self.win, command=self.newGameCallback, font=("Helvetica", 14),
                                    text=portalTexts["okLbl"])
        startGameButton.place(x=(self.leftMarginPos + 410), y=(self.player2ButtonTopPos + 100), width=100)

    def rb2callback(self):
        # Procedure executed when user selects user type for player 2
        if self.rb2value.get() == 1:
            self.player2AIlevelWidget.config(state=tk.DISABLED)
            print("In callback. Self: " + str(type(self)))
        else:
            self.player2AIlevelWidget.config(state=tk.NORMAL)

    def cancelDlgCallback(self):
        self.win.withdraw()

    def newGameCallback(self):
        if (self.player1nameWidget.get() == ""):
            # Post error message "Player 2 name may not be empty"
            messagebox.showerror(self.portal.texts["error"], self.portal.texts["noName"])
            # tk.messagebox.showerror(portalScreenTexts[6], portalScreenTexts[8])
            return

        # Create new game for player 1
        newGame = gamelobby(1, 2, self.player1nameWidget.get(), "AI", None, None)
        # List of waiting games
        self.portal.waitingGamesLB.addGame(newGame)

        # Hide dialog
        self.win.withdraw()



class joinGameDialog(complexDialog):
    def __init__(self, portal):
        super().__init__(self)

        portalTexts = portal.texts

        self.win.geometry("540x300")
        self.player1ButtonTopPos = 70
        self.player2ButtonTopPos = 140

        # Dialog window header text
        self.win.title(portalTexts["joinDlgHead"])

        # Prompt text for player 1
        promptText1 = tk.Label(self.win, anchor="center", font=("Helvetica", 14), text=portalTexts["actPrompt2"])
        promptText1.place(x=self.leftMarginPos, y=self.topMarginPos, width=520, height=40)

        # Left label for player 1 (the existing player)
        promptText1 = tk.Label(self.win, anchor=tk.CENTER, font=("Helvetica", 14), text=portalTexts["pl1"], bg="light steel blue")
        promptText1.place(x=self.leftMarginPos, y=self.player1ButtonTopPos, height=60, width=150)

        # Player 1 name (the waiting player)
        namePrompt1 = tk.Label(self.win, anchor="w", font=("Helvetica", 14), text=portalTexts["name"], bg = self.winBGcolor)
        namePrompt1.place(x=(self.leftMarginPos + 165), y=self.player1ButtonTopPos)
        # portal is the launching object.
        # portal.waitingGamesLB is the listbox-holding object
        # portal.waitingGamesLB.gamesList is the list of waiting games
        # ----
        # portal.selectedWaitingGameNumber holds the listbox selection data
        player1nameLbl = tk.Label(self.win, anchor="w", font=("Helvetica", 14), bg = self.winBGcolor,
            text=str(portal.waitingGamesLB.gamesList[portal.selectedWaitingGameNumber[0]].player1))
        player1nameLbl.place(x=(self.leftMarginPos + 240), y=self.player1ButtonTopPos, width=150)

        # Left label for player 2 (the joining player)
        promptText2 = tk.Label(self.win, anchor=tk.CENTER, font=("Helvetica", 14), text=portalTexts["pl2"], bg="light steel blue")
        promptText2.place(x=self.leftMarginPos, y=self.player2ButtonTopPos, height=60, width=150)

        # Player 2 name prompt
        namePrompt2 = tk.Label(self.win, anchor="w", font=("Helvetica", 14), text=portalTexts["name"], bg = self.winBGcolor)
        namePrompt2.place(x=(self.leftMarginPos + 165), y=self.player2ButtonTopPos)

        # Player 2 name variable
        player2name = tk.StringVar()
        # Player 2 name entry field
        player2nameWidget = tk.Entry(self.win, bg="snow", font=("Helvetica", 14), relief=tk.SUNKEN,
                                     textvariable=player2name)
        player2nameWidget.place(x=(self.leftMarginPos + 240), y=self.player2ButtonTopPos, width=280)
        self.player2nameWidget = player2nameWidget

        # Cancel button
        cancelDlgButton = tk.Button(self.win, command=self.cancelDlgCallback, font=("Helvetica", 14),
                                    text=portalTexts["cancelLbl"])
        cancelDlgButton.place(x=(self.leftMarginPos + 300), y=(self.player2ButtonTopPos + 100), width=100)

        # Start button
        startGameButton = tk.Button(self.win, command=self.newGameCallback, font=("Helvetica", 14),
                                    text=portalTexts["okLbl"])
        startGameButton.place(x=(self.leftMarginPos + 410), y=(self.player2ButtonTopPos + 100), width=100)

    def cancelDlgCallback(self):
        self.win.withdraw()

    def newGameCallback(self):
        if (self.player2nameWidget.get() == ""):
            # Post error message "Player 2 name may not be empty"
            messagebox.showerror(self.portal.texts["error"], self.portal.texts["noName"])
            # tk.messagebox.showerror(portalScreenTexts[6], portalScreenTexts[8])
            return

        # Join selected game

        # Hide dialog
        self.win.withdraw()

class portalScreen:
    def __init__(self):
        # Game constants
        portalScreenTexts = {
            "winName"   : "UU-GAME",
            "head"      : "UU-GAME Portal",
            "instr"     : "This is a two-player board game where pieces are placed on a board.\n"
                              "The players take turns. Each turn consists of\n"
                              " 1. placing the offered piece (if any) on the board,\n"
                              " 2. selecting a piece for the opponent.\n\n"
                              "Player 1 starts, by selecting a piece from the list on the left.\n\n"
                              "Placing four pieces with the same property in a row wins.",
            "actPrompt0": "Create a new game or select an existing one to join",
            "actPrompt1": "Enter name and select opponent",
            "actPrompt2": "Enter name to join the game",
            "name"      : "Name",
            "newGame"   : "New Game",
            "joinGame"  : "Join Game",
            "newDlgHead": "Player and Opponent Info",
            "joinDlgHead":"Player and Opponent Info",
            "pl1"       : "Player 1",
            "pl2"       : "Player 2",
            "humanPl"   : "Wait for human opponent",
            "compPl"    : "Play now. Computer level",
            "noName"    : "Player name is missing",
            "okLbl"     : "OK",
            "cancelLbl" : "Cancel",
            "quitLbl"   : "Quit",
            "error"     : "Error"
            }
        # Save texts as an attribute
        self.texts = portalScreenTexts

        # Widget top/left positions (constants added are vertical sizes)
        leftMarginPos =                              10
        headerTopPos =                               10
        introTopPos = headerTopPos +                 90
        playerPromptTopPos = introTopPos +          220
        player1ButtonTopPos = playerPromptTopPos +   60
        player2ButtonTopPos = player1ButtonTopPos +  80

        # Window background color
        winBGcolor = "light grey"

        # Create main window, called "root"
        root = tk.Tk()
        # Store this window as an attribute
        self.win = root
        # width x height
        root.geometry("620x650")
        root.resizable(0, 0)  # Don't allow resizing in the x or y direction
        root.title(portalScreenTexts["winName"])

        # Create an area to put widgets in, welcomeCanvas, in the top window
        welcomeCanvas = tk.Canvas(root, bg=winBGcolor, width=800, height=700)
        welcomeCanvas.place(x=0, y=0, width=1031, height=1031)
        self.canvas = welcomeCanvas

        # Page header
        header = tk.Label(welcomeCanvas, anchor=tk.CENTER, font=("Helvetica", 30, "bold"), relief=tk.RAISED,
                          bg="lightpink1", text=portalScreenTexts["head"])
        header.place(x=leftMarginPos, y=headerTopPos, height=80, width=600)

        # Intro text
        intro = tk.Label(welcomeCanvas, anchor="nw", justify=tk.LEFT, bg="snow", padx=20, pady=20,
                         font=("Helvetica", 12),
                         text=portalScreenTexts["instr"])
        intro.place(x=leftMarginPos, y=introTopPos, height=185, width=600)

        # Prompt text for player selection screen section
        promptText1 = tk.Label(welcomeCanvas, font=("Helvetica", 14), justify=tk.LEFT, text=portalScreenTexts["actPrompt0"])
        promptText1.place(x=leftMarginPos, y=playerPromptTopPos, height=40, width=600)

        # Listbox w waiting games
        waitingGamesLB = waitingGamesListBox(self, leftMarginPos + 130, player1ButtonTopPos)
        # Store as an attribute
        self.waitingGamesLB = waitingGamesLB
        # Also let LB have a pointer to self (this portal)
        waitingGamesLB.portal = self

        # Start game button
        newGameButton = tk.Button(welcomeCanvas, command=self.newGameCallback, font=("Helvetica", 14),
                                    text=portalScreenTexts["newGame"])
        newGameButton.place(x=leftMarginPos, y=player1ButtonTopPos, width = 120)

        # Join waiting game button
        joinGameButton = tk.Button(welcomeCanvas, command=self.joinGameCallback, font=("Helvetica", 14),
                                    text=portalScreenTexts["joinGame"])
        joinGameButton.place(x=leftMarginPos, y=player1ButtonTopPos + 50, width = 120)
        joinGameButton.config(state=tk.DISABLED)
        # Store as attribute, so itcan be reached from callback method
        self.joinGameButton = joinGameButton

        # Init number of selected waiting game
        self.selectedWaitingGameNumber = None


    # New game button callback
    def newGameCallback(portal):
        dlg = newGameDialog(portal)


    # Joing existing game callback
    def joinGameCallback(portal):
        dlg = joinGameDialog(portal)



portal = portalScreen()


"""
---------------------------------------^^-------------------------------------
"""
"""
# Prompt text for radio buttons
promptText1 = tk.Label(welcomeCanvas, anchor=tk.CENTER, font=("Helvetica", 14), text=welcomeScreenTexts[3])
promptText1.place(x=leftMarginPos, y=player1ButtonTopPos, height=60, width=150)

promptText2 = tk.Label(welcomeCanvas, anchor=tk.CENTER, font=("Helvetica", 14), text=welcomeScreenTexts[4])
promptText2.place(x=leftMarginPos, y=player2ButtonTopPos, height=60, width=150)

# Selection of first player
# Create variable to hold player 1 selection (1 or 2)
rb1value = tk.IntVar()


def rb1callback():
    # Procedure executed when user selects user type for player 1
    if rb1value.get() == 1:
        player1nameWidget.config(state=tk.NORMAL)
        player1AIlevelWidget.config(state=tk.DISABLED)
    else:
        player1nameWidget.config(state=tk.DISABLED)
        player1AIlevelWidget.config(state=tk.NORMAL)


# Radio buttons for selection of player 1 type
rButton1 = tk.Radiobutton(welcomeCanvas, text=welcomeScreenTexts[10], font=("Helvetica", 14), variable=rb1value,
                          bg=winBGcolor, value=1, command=rb1callback)
rButton1.place(x=(leftMarginPos + 160), y=(player1ButtonTopPos - 3))
rButton1.select()
rButton2 = tk.Radiobutton(welcomeCanvas, text=welcomeScreenTexts[11], font=("Helvetica", 14), variable=rb1value,
                          bg=winBGcolor, value=2, command=rb1callback)
rButton2.place(x=(leftMarginPos + 160), y=(player1ButtonTopPos + 26))


# Player 1 name variable
player1name = tk.StringVar()
# player1name.set("Player 1 name")

# Player 1 name entry field
player1nameWidget = tk.Entry(welcomeCanvas, bg="snow", font=("Helvetica", 14), relief=tk.SUNKEN,
                             textvariable=player1name)
player1nameWidget.place(x=(leftMarginPos + 280), y=player1ButtonTopPos)

# Player 1 AI level
ai1value = tk.StringVar()
player1AIlevelWidget = tk.Spinbox(welcomeCanvas, font=("Helvetica", 14), textvariable=ai1value, values=("easy", "medium", "hard"))
player1AIlevelWidget.place(x=(leftMarginPos + 280), y=(player1ButtonTopPos + 30))
# Initially disabled
player1AIlevelWidget.config(state=tk.DISABLED)

# Selection of second player
# Create variable to hold player 2 selection (1 or 2)
rb2value = tk.IntVar()


def rb2callback():
    # Procedure executed when user selects user type for player 2
    if rb2value.get() == 1:
        player2nameWidget.config(state=tk.NORMAL)
        player2AIlevelWidget.config(state=tk.DISABLED)
    else:
        player2nameWidget.config(state=tk.DISABLED)
        player2AIlevelWidget.config(state=tk.NORMAL)


rButton3 = tk.Radiobutton(welcomeCanvas, text=welcomeScreenTexts[10], font=("Helvetica", 14), variable=rb2value,
                          bg=winBGcolor, value=1, command=rb2callback)
rButton3.place(x=(leftMarginPos + 160), y=(player2ButtonTopPos - 3))
rButton3.select()
rButton4 = tk.Radiobutton(welcomeCanvas, text=welcomeScreenTexts[11],
                          bg=winBGcolor, font=("Helvetica", 14), variable=rb2value, value=2, command=rb2callback)
rButton4.place(x=(leftMarginPos + 160), y=(player2ButtonTopPos + 26))

# Player 2 name variable
player2name = tk.StringVar()
# Player 2 name entry field
player2nameWidget = tk.Entry(welcomeCanvas, bg="snow", font=("Helvetica", 14), relief=tk.SUNKEN,
                             textvariable=player2name)
player2nameWidget.place(x=(leftMarginPos + 280), y=player2ButtonTopPos)

# Player 2 AI level
ai2value = tk.StringVar()
player2AIlevelWidget = tk.Spinbox(welcomeCanvas, font=("Helvetica", 14), textvariable=ai2value, values=("easy", "medium", "hard"))
player2AIlevelWidget.place(x=(leftMarginPos + 280), y=(player2ButtonTopPos + 30))
# Initially disable
player2AIlevelWidget.config(state=tk.DISABLED)


def startgamecallback():
    # Procedure called when the start game button is pressed

    global player1name
    global player2name
    global rb1value
    global rb2value

    # Verify that player 1 is human & has a name or is computer
    if (rb1value.get() == 1) and (player1nameWidget.get() == ""):
        # Post error message "Player 1 name may not be empty"
        messagebox.showerror(welcomeScreenTexts[6], welcomeScreenTexts[7])
        # tk.messagebox.showerror(welcomeScreenTexts[6], welcomeScreenTexts[7])
        return

    if (rb2value.get() == 1) and (player2nameWidget.get() == ""):
        # Post error message "Player 2 name may not be empty"
        messagebox.showerror(welcomeScreenTexts[6], welcomeScreenTexts[8])
        # tk.messagebox.showerror(welcomeScreenTexts[6], welcomeScreenTexts[8])
        return

    # Hide this window
    root.withdraw()

    # Start the game here, from this callback
    # Choices are
    #  - rb1value.get() = 1 ==> human player 1
    #  - rb1value.get() = 2 ==> computer player 1
    #  - player1nameWidget.get() ==> human player 1 name
    #  - player1AIlevelWidget.get() ==> AI player level (easy/medium/hard)
    initGame(player1nameWidget.get(), player2nameWidget.get(), rb1value.get(), rb2value.get(), player1AIlevelWidget.get(), player2AIlevelWidget.get())

    # At the end, terminate close this Window
    root.destroy()



# Callback for the quit button. Quits app.

def quitgamecallback():
    raise SystemExit()


# Start game button
startGameButton = tk.Button(welcomeCanvas, command=startgamecallback, font=("Helvetica", 14),
                            text=welcomeScreenTexts[5])
startGameButton.place(x=(leftMarginPos + 450), y=(player2ButtonTopPos + 90))

# Quit game button
quitGameButton = tk.Button(welcomeCanvas, command=quitgamecallback, font=("Helvetica", 14),
                            text=welcomeScreenTexts[12])
quitGameButton.place(x=(leftMarginPos + 10), y=(player2ButtonTopPos + 90))
"""

# Launch main event loop
portal.win.mainloop()

#sio.emit('join game', {'name':xxx})
#sio.emit('create game')
#sio.emit('create game', {'player1':xxx, 'player2':xxx})
