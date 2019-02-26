#!/usr/bin/python

"""
This implements the welcome page for the UU-GAME game platform.
The code contains a number constants for placement and language,
then follows creation of screen widgets.
At the end, there is a procedure, startgamecallback, that launches the game.
This procedure has access to the entered data (player names and human/computer
player).
- rb1value.get() = 1 ==> human player 1
- rb1value.get() = 2 ==> computer player 1
- rb2value.get() = 1 ==> human player 2
- rb2value.get() = 2 ==> computer player 2
- player1nameWidget.get() ==> human player 1 name
- player2nameWidget.get() ==> human player 2 name

(c) 2019 SEPM Group G
"""
import Tkinter as tk # tkinter in Py3
# from Tkinter import messagebox  # used for error messages Py3
import tkMessageBox


# Game constants
welcomeScreenTexts = ("UU-GAME",
                      "Welcome to UU-GAME",
                      "This is a two-player board game where pieces are placed on a board.\n"
                            "The players take turns. Each turn consists of\n"
                            " 1. placing the offered piece (if any) on the board,\n"
                            " 2. selecting a piece for the opponent.\n\n"
                            "Player 1 starts, by selecting a piece\n\n"
                            "Placing four pieces with the same property in a row wins.",
                      "Player 1",
                      "Player 2",
                      "Start",
                      "Error",
                      "Player 1 name is missing.",
                      "Player 2 name is missing",
                      "Enter player names or select computer opponent",
                      "Human",
                      "Computer")

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
# width x height
root.geometry("620x650")
root.resizable(0, 0)  # Don't allow resizing in the x or y direction
root.title(welcomeScreenTexts[0])

# Create an area to put widgets in, welcomeCanvas, in the top window
welcomeCanvas = tk.Canvas(root, bg=winBGcolor, width=800, height=700)
welcomeCanvas.place(x=0, y=0, width=1031, height=1031)


# Code to add widgets goes here...

# Page header
header = tk.Label(welcomeCanvas, anchor=tk.CENTER, font=("Helvetica", 30, "bold"), relief=tk.RAISED,
                  bg="lightpink1", text=welcomeScreenTexts[1])
header.place(x=leftMarginPos, y=headerTopPos, height=80, width=600)

# Intro text
intro = tk.Label(welcomeCanvas, anchor="nw", justify=tk.LEFT, bg="snow", padx=20, pady=20,
                 font=("Helvetica", 12),
                 text=welcomeScreenTexts[2])
intro.place(x=leftMarginPos, y=introTopPos, height=185, width=600)

# Prompt text for player selection screen section
promptText1 = tk.Label(welcomeCanvas, font=("Helvetica", 14), justify=tk.LEFT, text=welcomeScreenTexts[9])
promptText1.place(x=leftMarginPos, y=playerPromptTopPos, height=40, width=600)

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
    else:
        player1nameWidget.config(state=tk.DISABLED)


# Radio buttons for selection of player 1 type
rButton1 = tk.Radiobutton(welcomeCanvas, text=welcomeScreenTexts[10], font=("Helvetica", 14), variable=rb1value,
                          bg=winBGcolor, value=1, command=rb1callback)
rButton1.place(x=(leftMarginPos + 160), y=(player1ButtonTopPos - 3))
rButton1.select()
rButton2 = tk.Radiobutton(welcomeCanvas, text=welcomeScreenTexts[11], font=("Helvetica", 14), variable=rb1value,
                          bg=winBGcolor, value=2, command=rb1callback)
rButton2.place(x=(leftMarginPos + 160), y=(player1ButtonTopPos + 26))


# Player 1 name variable
player1name = tk.StringVar
# player1name.set("Player 1 name")

# Player 1 name entry field
player1nameWidget = tk.Entry(welcomeCanvas, bg="snow", font=("Helvetica", 14), relief=tk.SUNKEN,
                             textvariable=player1name)
player1nameWidget.place(x=(leftMarginPos + 280), y=player1ButtonTopPos)

# Selection of second player
# Create variable to hold player 2 selection (1 or 2)
rb2value = tk.IntVar()


def rb2callback():
    # Procedure executed when user selects user type for player 2
    if rb2value.get() == 1:
        player2nameWidget.config(state=tk.NORMAL)
    else:
        player2nameWidget.config(state=tk.DISABLED)


rButton3 = tk.Radiobutton(welcomeCanvas, text=welcomeScreenTexts[10], font=("Helvetica", 14), variable=rb2value,
                          bg=winBGcolor, value=1, command=rb2callback)
rButton3.place(x=(leftMarginPos + 160), y=(player2ButtonTopPos - 3))
rButton3.select()
rButton4 = tk.Radiobutton(welcomeCanvas, text=welcomeScreenTexts[11],
                          bg=winBGcolor, font=("Helvetica", 14), variable=rb2value, value=2, command=rb2callback)
rButton4.place(x=(leftMarginPos + 160), y=(player2ButtonTopPos + 26))

# Player 2 name variable
player2name = tk.StringVar
# Player 2 name entry field
player2nameWidget = tk.Entry(welcomeCanvas, bg="snow", font=("Helvetica", 14), relief=tk.SUNKEN,
                             textvariable=player2name)
player2nameWidget.place(x=(leftMarginPos + 280), y=player2ButtonTopPos)


def startgamecallback():
    # Procedure called when the start game button is pressed
    # Verify that player 1 is human & has a name or is computer
    if (rb1value.get() == 1) and (player1nameWidget.get() == ""):
        # Post error message "Player 1 name may not be empty"
        tkMessageBox.showerror(welcomeScreenTexts[6], welcomeScreenTexts[7])
        # tk.messagebox.showerror(welcomeScreenTexts[6], welcomeScreenTexts[7])
        return

    if (rb2value.get() == 1) and (player2nameWidget.get() == ""):
        # Post error message "Player 2 name may not be empty"
        tkMessageBox.showerror(welcomeScreenTexts[6], welcomeScreenTexts[8])
        # tk.messagebox.showerror(welcomeScreenTexts[6], welcomeScreenTexts[8])
        return

    # Start the game here, from this callback
    # Choices are
    #  - rb1value.get() = 1 ==> human player 1
    #  - rb1value.get() = 2 ==> computer player 1
    #  - player1nameWidget.get() ==> human player 1 name

    # At the end, terminate close this Window
    root.withdraw()
    root.destroy()

    initgamescreen()


# Start game button
startGameButton = tk.Button(welcomeCanvas, command=startgamecallback, font=("Helvetica", 14),
                            text=welcomeScreenTexts[5])
startGameButton.place(x=(leftMarginPos + 510), y=(player2ButtonTopPos + 60))

# Launch main event loop
root.mainloop()
