"""
This is a test file, intended to experiment with calling a function from
another file.
"""
import tkinter as tk # tkinter in Py3

class waitingGamesListBox:
    def __init__(self, win, xPos, yPos):
        # Define scrollbar
        scrollbar = tk.Scrollbar(win, orient="vertical")
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        # Define listbox, add scrollbar update command
        waitingGamesLb = tk.Listbox(win, yscrollcommand = scrollbar.set)
        waitingGamesLb.place(xPos,yPos)
        # Add listbox update command
        scrollbar.config(command = waitingGamesLb.yview)
        # Add list box as attribute of this instance
        listBox = waitingGamesListBox


    def update(self,gamesList):
        for aGame in gamesList:
            self.listBox.insert(tk.END, aGame)


    def addGame(self, aGame):
        self.listBox.insert(tk.END, aGame)


    #def deleteGame(self, aGame)

root = tk.Tk()
root.title("UU Game")
root.geometry("800x500")

lb = waitingGamesListBox(root, 10, 10)

# Launch main event loop
root.mainloop()
