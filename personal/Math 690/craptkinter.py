from crap import Dice, FirstRoll, Game
from tkinter import *




class Window: 
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1200x1200")
        quitButton = Button(self.window, text = "Quit", command=self.quit)
        self.rollLabel = Label(self.window, text="Roll Dice")
        self.rollLabel.pack()
        self.statusLabel = Label(self.window, text ="")
        self.statusLabel.pack()
        self.rollButton = Button(self.window, text = "Roll Dice", command = self.rollDice)
        self.rollButton.pack()
        self.game = Game()
        self.first_roll_done = False
        self.point = 0
        quitButton.pack()
        self.window.mainloop()
    def quit(self):
        self.window.destroy()
    def rollDice(self):
        if not self.first_roll_done:
            result = self.game.firstRoll.first_roll()
            self.rollLabel.config(text=f"First roll result: {result}")
            if result == 7 or result == 11:
                self.statusLabel.config(text=f"You win! You rolled a {result}")
                self.rollButton.config(state="disabled")
            elif result == 2 or result == 3 or result == 12:
                self.statusLabel.config(text=f"You lose! You rolled a {result}")
                self.rollButton.config(state="disabled")
            else:
                self.point = result
                self.statusLabel.config(text=f"Point is now: {self.point}")
                self.first_roll_done = True
        else: 
            result = self.game.dice.roll()
            self.rollLabel.config(text=f"Rolled {result}")
            if result == self.point:
                self.statusLabel.config(text=f"You win! Rolled: {result}")
                self.rollButton.config(state="disabled")
            elif result == 7:
                self.statusLabel.config(text=f"You lose! Rolled: {result}")
                self.rollButton.config(state="disabled")
            else:
                self.statusLabel.config(text=f"Point is still {self.point}. You rolled a {result}")
w = Window()