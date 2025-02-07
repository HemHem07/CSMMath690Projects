import math
from tkinter import * 
import tkinter as tk

class Win: 
    def __init__(self):
        self.win = Tk()
        self.win.title("Solar System Simulation")
        self.win.geometry("600x650")

        width = 400
        ht = 400

        # Quit Button
        self.quit_button = Button(self.win, text="Quit", command=self.win.destroy)
        self.quit_button.pack(pady=5)

        # Canvas for drawing
        self.canvas = Plot(self.win, width, ht)
        self.canvas.pack()
        self.canvas.update()

        # Control Buttons
        self.go_button = Button(self.win, text="Go", command=self.go)
        self.go_button.pack(pady=5)

        self.stop_button = Button(self.win, text="Stop", command=self.stop)
        self.stop_button.pack(pady=5)

        # Animation Parameters
        self.isgo = False
        self.speed = 10
        self.radiusSun = 25

        # Create Sun
        self.sun = createSun(self.radiusSun, self.canvas)
        self.sun.plotSun()

        # Manage List of Planets
        self.listOfPlanets = listOfPlanets(self.canvas)

        # Add Planet Button
        self.add_planet_button = Button(self.win, text="Add Planet", command=self.listOfPlanets.addPlanet)
        self.add_planet_button.pack(pady=5)

        # Time Variable
        self.t = 0

    def go(self):
        if not self.isgo:
            self.isgo = True
            self.animate()

    def stop(self): 
        self.isgo = False 

    def animate(self):
        if self.isgo:
            self.t += 0.5
            self.listOfPlanets.moveAllPlanets(self.t)
            self.canvas.update()
            self.canvas.after(self.speed, self.animate) 
class Plot(Canvas):
    def __init__(self, win, width, ht): 
        Canvas.__init__(self, win, width=width, height=ht, bg="black")
        self.width = width
        self.height = ht

class createSun: 
    def __init__(self, radius, canvas):
        self.radius = radius
        self.canvas = canvas
        self.update_center()

    def update_center(self):
        self.xCenter = self.canvas.winfo_width() / 2
        self.yCenter = self.canvas.winfo_height() / 2

    def plotSun(self): 
        self.canvas.update_idletasks()  # Ensure accurate dimensions
        self.update_center()
        self.sun = self.canvas.create_oval(
            self.xCenter - self.radius, self.yCenter - self.radius,
            self.xCenter + self.radius, self.yCenter + self.radius,
            fill="yellow", outline="orange"
        )

class planet:
    def __init__(self, distance, canvas, radius): 
        self.canvas = canvas
        self.distance = distance
        self.radius = radius
        self.update_center()

    def update_center(self):
        self.xCenter = self.canvas.winfo_width() / 2
        self.yCenter = self.canvas.winfo_height() / 2 

    def createPlanet(self):
        self.update_center()
        x = self.xCenter + self.distance
        y = self.yCenter
        self.planet = self.canvas.create_oval(
            x - self.radius, y - self.radius,
            x + self.radius, y + self.radius,
            fill="white", outline="white"
        )

    def planetOrbit(self, t):
        self.update_center()
        x = self.xCenter + self.distance * math.cos(-t)
        y = self.yCenter + self.distance * math.sin(-t)
        self.canvas.coords(
            self.planet,
            x - self.radius, y - self.radius,
            x + self.radius, y + self.radius
        )

class listOfPlanets:
    def __init__(self, canvas):
        self.planets = []
        self.periodValues = []
        self.canvas = canvas

    def add_existing_planet(self, planet_obj):
        self.planets.append(planet_obj)
        self.periodValues.append(math.pow(planet_obj.distance, 1.5))  # Kepler's Third Law

    def addPlanet(self):
        # Create a pop-up window using Toplevel()
        self.entries_window = Toplevel()
        self.entries_window.title("Add Planet")
        self.entries_window.grab_set()  # Make the window modal

        # Labels and Entry widgets for distance and radius
        distance_label = Label(self.entries_window, text="Distance from Sun:")
        distance_label.pack(pady=5)
        distance_entry = Entry(self.entries_window)
        distance_entry.pack(pady=5)

        radius_label = Label(self.entries_window, text="Radius of Planet:")
        radius_label.pack(pady=5)
        radius_entry = Entry(self.entries_window)
        radius_entry.pack(pady=5)

        # Function to handle adding the planet
        def submit():
            distance = float(distance_entry.get())  # Get the distance value
            radius = float(radius_entry.get())      # Get the radius value

            # Create a new planet instance
            new_planet = planet(distance, self.canvas, radius)
            new_planet.createPlanet()               # Draw the planet immediately

            # Add the new planet and its period to the respective lists
            self.planets.append(new_planet)
            self.periodValues.append(math.pow(distance, 1.5))  # Kepler's Third Law

            # Close the pop-up window
            self.entries_window.destroy()

        # Button to submit the values and add the planet
        add_button = Button(self.entries_window, text="Add", command=submit)
        add_button.pack(pady=10)

    def moveAllPlanets(self, t):
        for i, planet_obj in enumerate(self.planets):
            period = self.periodValues[i]
            scaled_t = t /(period / 50 ) # Scale time by period to get the angle
            planet_obj.planetOrbit(scaled_t)

# Initialize and run the application
x = Win()
x.win.mainloop()