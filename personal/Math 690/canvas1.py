from tkinter import * 

class Window: 
    def __init__(self,width,height):
        self.window = Tk()
        self.window.geometry("800x800")
        self.width = width
        self.height = height
        self.canvaswidth = self.width/2
        self.canvasheight = self.height/2


        # Create the canvas for the graph/grid
        self.canvas = Canvas(self.window, width=self.canvaswidth, height=self.canvasheight)
        self.canvas.pack()

  # Spanning across columns



    
    def hframex(self, x, minX, maxX, width):
        return (x - minX) / (maxX - minX) * width
    def hframey(self, y, minY, maxY, height):
        return height - (y - minY)/(maxY-minY)*height
    def run(self):
        self.window.mainloop()
    def createLines(self, xMin, xMax, yMin, yMax):
        width = self.canvaswidth  # Use canvas width
        height = self.canvasheight  # Use canvas height
        for i in range(xMin, xMax + 1):
            x = self.hframex(i, xMin, xMax, width)
            if i != 0:
                self.canvas.create_line(x, 0, x, height)
            else:
                self.canvas.create_line(x, 0, x, height, width=5)
        for i in range(yMin, yMax + 1):
            y = self.hframey(i, yMin, yMax, height)
            if i != 0:
                self.canvas.create_line(0, y, width, y)
            else:
                self.canvas.create_line(0, y, width, y, width=5)

class Entry: 
    def __init__(self, window): 
        self.window = window
        self.labelxmin = Label(window, text = "Minimum x")
        self.labelxmin.pack()
        self.labelymin = Label(window, text = "Minimum y")
        self.labelymin.pack()
        self.labelxmax = Label(window, text = "Maximum x")
        # self.labelxmax.pack()
        self.labelymax = Label(window, text = "Maximum y")
        # self.labelymax.pack()

        # self.entryxmin = Tk.Entry(window, text ="")
def main():
    height = 800
    width = 800
    xmin = -5
    xmax = 5
    ymin = -5
    ymax = 5

    w = Window(width, height)
    form = Entry(w.window)

  

    # Create grid lines
    w.createLines(xmin, xmax, ymin, ymax)

    w.run()

main()


# Then in Python as you have the time:

# Write a program that 

# puts up a canvas of hmin to hmax and vmin to vmax (have the program use specific values for these).

#  uses conversion functions to convert a standard x coordinate to h-v coordinates and the same for y.

#   puts up an xy grid for -5 <= x <= 5 and -5 <= y <= 5 with a grid line at each integer value.

#   draws the x and y axes as thicker lines than the grid lines.