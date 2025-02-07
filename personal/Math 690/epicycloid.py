from tkinter import *
import math

class xySystem:
    def __init__(self,xmin,xmax,ymin,ymax,hmax,vmax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.hmax = hmax 
        self.vmax = vmax 
    def xtoh(self,x):
        self.a = (self.hmax) / (self.xmax - self.xmin) 
        self.b = (-self.hmax) / (self.xmax - self.xmin) * self.xmin 
        return self.a * x + self.b 
    def ytov(self,y):
        self.a = (self.vmax) / (self.ymin - self.ymax)
        self.b = (-self.vmax) / (self.ymin - self.ymax) * self.ymax 
        return self.a * y + self.b

class Win:
    def __init__(self,xMin,xMax,yMin,yMax,rsmall,increment,rbig):
        self.win = Tk()
        self.win.geometry("600x600")
        self.width = 400 
        self.height = 400
        self.canvas = Plot(self.win,self.width,self.height)
        self.canvas.pack()
        self.canvas.update()
        self.convert = xySystem(xMin,xMax,yMin,yMax,self.width,self.height)
        self.rsmall = rsmall
        self.rbig = rbig
        self.increment = increment
        # Initial setup
        self.setup()

        self.go_button = Button(self.win, text="Go", command=self.go)
        self.go_button.pack(pady=5)

        self.stop_button = Button(self.win, text="Stop", command=self.stop)
        self.stop_button.pack(pady=5)

        self.reset_button = Button(self.win, text="Reset", command=self.reset)
        self.reset_button.pack(pady=5)

        self.quit_button = Button(self.win, text="Quit", command=self.win.destroy)
        self.quit_button.pack(pady=5)

        self.isgo = False

    def setup(self):
        # Clears the canvas and re-create all objects in their initial state
        self.canvas.delete("all")
        self.circle = Circle(self.canvas,self.convert,self.rsmall,self.rbig,self.increment)
        self.xAxis = xAxis(self.canvas,self.convert) 
        self.yAxis = yAxis(self.canvas,self.convert)
        self.centralCircle = centralCircle(self.canvas,self.rbig,self.convert)
        self.point = Point(self.canvas,self.convert,self.circle,self.centralCircle,self.increment)
        self.diameter = Diameter(self.canvas,self.convert,self.circle,self.increment,self.centralCircle,self.point)
        self.trail = Trail(self.canvas,self.point)

    def go(self):
        if self.isgo == False:
            self.isgo = True
            self.animate()

    def stop(self):
        self.isgo = False 

    def reset(self):
        # Stop animation and reset everything
        self.stop()
        self.setup()

    def animate(self):
        if self.isgo:
            self.circle.move()
            self.point.move()
            self.diameter.move()
            self.trail.plot()
            self.canvas.update()
            self.canvas.after(200, self.animate)

class Plot(Canvas):
    def __init__(self, win, width, height):
        super().__init__(win,width=width,height=height,bg="white")
        self.width = width
        self.height = height

class Circle:
    def __init__ (self, canvas, xysystem, rsmall,rbig,increment):
        self.radius = rsmall
        self.rbig = rbig
        self.convert = xysystem
        self.canvas = canvas
        self.t=0
        self.centerX = self.computeCenterX()
        self.centerY = self.computeCenterY()
        self.plotX1 = self.centerX - self.radius
        self.plotY1 = self.centerY + self.radius 
        self.plotX2 = self.centerX + self.radius 
        self.plotY2 = self.centerY - self.radius 
        self.h1 = self.convert.xtoh(self.plotX1)
        self.v1 = self.convert.ytov(self.plotY1)
        self.h2 = self.convert.xtoh(self.plotX2)
        self.v2 = self.convert.ytov(self.plotY2)
        self.increment = increment
        self.circle = self.canvas.create_oval(self.h1,self.v1,self.h2,self.v2,outline="black")
    def computeCenterX(self):
        return (self.rbig + self.radius) * math.cos(self.t)
    def computeCenterY(self):
        return (self.rbig + self.radius) * math.sin(self.t)
    def move(self):
        self.canvas.delete(self.circle)
        self.t += self.increment
        self.centerX = self.computeCenterX()
        self.centerY = self.computeCenterY()
        self.plotX1 = self.centerX - self.radius
        self.plotY1 = self.centerY + self.radius 
        self.plotX2 = self.centerX + self.radius 
        self.plotY2 = self.centerY - self.radius 
        self.h1 = self.convert.xtoh(self.plotX1)
        self.v1 = self.convert.ytov(self.plotY1)
        self.h2 = self.convert.xtoh(self.plotX2)
        self.v2 = self.convert.ytov(self.plotY2)
        self.circle = self.canvas.create_oval(self.h1,self.v1,self.h2,self.v2,outline="black")

class xAxis:
    def __init__(self,canvas,xysystem):
        self.canvas = canvas
        self.convert = xysystem
        self.xmin = self.convert.xmin
        self.xmax = self.convert.xmax
        self.x1 = self.convert.xtoh(self.xmin)
        self.x2 = self.convert.xtoh(self.xmax)
        self.y = self.convert.ytov(0)
        self.canvas.create_line(self.x1,self.y,self.x2,self.y,fill="black")

class yAxis:
    def __init__ (self,canvas,xysystem):
        self.canvas = canvas
        self.convert = xysystem 
        self.ymin = self.convert.ymin 
        self.ymax = self.convert.ymax 
        self.y1 = self.convert.ytov(self.ymin)
        self.y2 = self.convert.ytov(self.ymax)
        self.x = self.convert.xtoh(0)
        self.canvas.create_line(self.x,self.y1,self.x,self.y2,fill="black")

class Point:
    def __init__(self, canvas, xysystem, circle,central,increment):
        self.canvas = canvas 
        self.convert = xysystem 
        self.circle = circle
        self.central = central
        self.bigr = self.central.radius
        self.radius = self.circle.radius
        self.t = 0
        self.theta = self.bigr / self.radius * self.t
        self.increment = increment

        # Compute the mathematical coordinates
        self.x = self.circle.centerX
        self.y = self.circle.centerY
        
        self.pointX = self.x - (self.circle.radius) * math.cos(self.t + self.theta) #unhardcode these later. 
        self.pointY = self.y - (self.circle.radius) * math.sin(self.t + self.theta)

        # Convert to screen coordinates and store them
        self.screenX = self.convert.xtoh(self.pointX)
        self.screenY = self.convert.ytov(self.pointY)
        
        # Create the initial point using screen coordinates
        self.point = self.canvas.create_oval(
            self.screenX - self.radius * 4, 
            self.screenY - self.radius * 4, 
            self.screenX + self.radius * 4, 
            self.screenY + self.radius * 4, 
            fill='red'
        )

        # Draw the initial point by calling move once
    def move(self):
        self.canvas.delete(self.point)
        self.t += self.increment
        self.theta = self.bigr / self.radius * self.t

        # Compute the mathematical coordinates
        self.x = self.circle.centerX
        self.y = self.circle.centerY
        
        self.pointX = self.x - (self.circle.radius) * math.cos(self.t + self.theta) #unhardcode these later. 
        self.pointY = self.y - (self.circle.radius) * math.sin(self.t + self.theta)

        # Convert to screen coordinates and store them
        self.screenX = self.convert.xtoh(self.pointX)
        self.screenY = self.convert.ytov(self.pointY)
        
        # Create the initial point using screen coordinates
        self.point = self.canvas.create_oval(
            self.screenX - self.radius * 4, 
            self.screenY - self.radius * 4, 
            self.screenX + self.radius * 4, 
            self.screenY + self.radius * 4, 
            fill='red'
        )

    # def move(self):
    #     # Compute point coordinates based on circle's current x-position
    #     self.x = (self.circle.x1 + self.circle.x2) / 2
    #     self.pointY = self.radius - self.radius * math.cos(self.x / self.radius)
    #     self.pointX = self.x - self.radius * math.sin(self.x / self.radius)

    #     # Convert to screen coordinates and store them
    #     self.screenX = self.convert.xtoh(self.pointX)
    #     self.screenY = self.convert.ytov(self.pointY)

    #     # If there's an existing point, delete it
    #     self.canvas.delete(self.point)

    #     # Draw the updated point using stored screen coordinates
    #     self.point = self.canvas.create_oval(
    #         self.screenX - 3, 
    #         self.screenY - 3, 
    #         self.screenX + 3, 
    #         self.screenY + 3, 
    #         fill='red'
    #     )
class Diameter:
    def __init__(self, canvas, xysystem, circle,increment,central,point):
        self.canvas = canvas 
        self.convert = xysystem 
        self.circle = circle
        self.radius = self.circle.radius
        self.central = central 
        self.bigr = self.central.radius
        self.t = 0
        self.theta = 0
        self.point = point
        self.increment = 0
        # self.x = self.circle.centerX
        # self.y = self.circle.centerY
        # Calculate mathematical coordinates
        # self.x1 = self.point.pointX
        # self.y1 = self.point.pointY
        # self.x2 = self.x - (self.circle.radius) * math.cos(math.pi + self.t + self.theta)  
        # self.y2 = self.y - (self.circle.radius) * math.sin(math.pi + self.t + self.theta)
        self.x = self.point.pointX
        self.y = self.point.pointY
        self.circx = self.circle.centerX
        self.circy = self.circle.centerY
        self.vecx = self.circx - self.x 
        self.vecy = self.circy - self.y 

        self.newX = self.x + 2 * self.vecx 
        self.newY = self.y + 2 * self.vecy
        self.screenX1 = self.convert.xtoh(self.x)
        self.screenY1 = self.convert.ytov(self.y)
        self.screenX2 = self.convert.xtoh(self.newX)
        self.screenY2 = self.convert.ytov(self.newY)
        # Convert to screen coordinates
        # self.screenX1 = self.convert.xtoh(self.x1)
        # self.screenY1 = self.convert.ytov(self.y1)
        # self.screenX2 = self.convert.xtoh(self.x2)
        # self.screenY2 = self.convert.ytov(self.y2)

        # Create the initial diameter line
        self.diameter = self.canvas.create_line(
            self.screenX1, self.screenY1,
            self.screenX2, self.screenY2,
            fill="red", width=2
        )

    def move(self):
        self.canvas.delete(self.diameter)
        self.x = self.point.pointX
        self.y = self.point.pointY
        self.circx = self.circle.centerX
        self.circy = self.circle.centerY
        self.vecx = self.circx - self.x 
        self.vecy = self.circy - self.y 

        self.newX = self.x + 2 * self.vecx 
        self.newY = self.y + 2 * self.vecy
        self.screenX1 = self.convert.xtoh(self.x)
        self.screenY1 = self.convert.ytov(self.y)
        self.screenX2 = self.convert.xtoh(self.newX)
        self.screenY2 = self.convert.ytov(self.newY)
        # Convert to screen coordinates
        # self.screenX1 = self.convert.xtoh(self.x1)
        # self.screenY1 = self.convert.ytov(self.y1)
        # self.screenX2 = self.convert.xtoh(self.x2)
        # self.screenY2 = self.convert.ytov(self.y2)

        # Create the initial diameter line
        self.diameter = self.canvas.create_line(
            self.screenX1, self.screenY1,
            self.screenX2, self.screenY2,
            fill="red", width=2
        )
    #     # Recompute the mathematical coordinates
    #     self.x = (self.circle.x1 + self.circle.x2) / 2
    #     self.pointY2 = self.radius - self.radius * math.cos(self.x / self.radius + math.pi)
    #     self.pointX2 = self.x - self.radius * math.sin(self.x / self.radius + math.pi)
    #     self.pointY1 = self.radius - self.radius * math.cos(self.x / self.radius)
    #     self.pointX1 = self.x - self.radius * math.sin(self.x / self.radius)

    #     # Convert to screen coordinates
    #     self.screenX1 = self.convert.xtoh(self.pointX1)
    #     self.screenY1 = self.convert.ytov(self.pointY1)
    #     self.screenX2 = self.convert.xtoh(self.pointX2)
    #     self.screenY2 = self.convert.ytov(self.pointY2)

    #     # Delete the old diameter line
    #     self.canvas.delete(self.diameter)

    #     # Draw the updated diameter line
    #     self.diameter = self.canvas.create_line(
    #         self.screenX1, self.screenY1,
    #         self.screenX2, self.screenY2,
    #         fill="red", width=2
    #     )
class Trail:
    def __init__(self, canvas, point):
        self.point = point
        self.canvas = canvas 
        self.oldX = self.point.screenX
        self.oldY = self.point.screenY
    def plot(self):
        newX = self.point.screenX
        newY = self.point.screenY
        
        
        self.trail = self.canvas.create_line(self.oldX, self.oldY, newX, newY, fill="red", width=2)

        self.oldX = newX
        self.oldY = newY

class centralCircle:
    def __init__(self,canvas,radius, xysystem):
        self.radius = radius
        self.canvas = canvas
        self.convert = xysystem
        self.plotX1 = -self.radius
        self.plotY1 = self.radius 
        self.plotX2 = self.radius 
        self.plotY2 = -self.radius 

        self.screenX1 = self.convert.xtoh(self.plotX1)
        self.screenY1 = self.convert.ytov(self.plotY1)
        self.screenX2 = self.convert.xtoh(self.plotX2)
        self.screenY2 = self.convert.ytov(self.plotY2)

        self.canvas.create_oval(self.screenX1,self.screenY1,self.screenX2,self.screenY2,outline="red")

xMin = -20
xMax = 20
yMin = -20
yMax = 20
smallR = 1.5
bigR = 5
inc = 0.1
x = Win(xMin,xMax,yMin,yMax,smallR,inc,bigR)
x.win.mainloop()