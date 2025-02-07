from tkinter import *
import math

# --- Existing Coordinate System Class ---
class xySystem:
    def __init__(self, xmin, xmax, ymin, ymax, hmax, vmax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.hmax = hmax 
        self.vmax = vmax 
    def xtoh(self, x):
        self.a = (self.hmax) / (self.xmax - self.xmin) 
        self.b = (-self.hmax) / (self.xmax - self.xmin) * self.xmin 
        return self.a * x + self.b 
    def ytov(self, y):
        self.a = (self.vmax) / (self.ymin - self.ymax)
        self.b = (-self.vmax) / (self.ymin - self.ymax) * self.ymax 
        return self.a * y + self.b

# --- Existing Canvas Class ---
class Plot(Canvas):
    def __init__(self, win, width, height):
        super().__init__(win, width=width, height=height, bg="white")
        self.width = width
        self.height = height

# --- Existing Axes ---
class xAxis:
    def __init__(self, canvas, xysystem):
        self.canvas = canvas
        self.convert = xysystem
        self.xmin = self.convert.xmin
        self.xmax = self.convert.xmax
        self.x1 = self.convert.xtoh(self.xmin)
        self.x2 = self.convert.xtoh(self.xmax)
        self.y = self.convert.ytov(0)
        self.canvas.create_line(self.x1, self.y, self.x2, self.y, fill="black")

class yAxis:
    def __init__(self, canvas, xysystem):
        self.canvas = canvas
        self.convert = xysystem 
        self.ymin = self.convert.ymin 
        self.ymax = self.convert.ymax 
        self.y1 = self.convert.ytov(self.ymin)
        self.y2 = self.convert.ytov(self.ymax)
        self.x = self.convert.xtoh(0)
        self.canvas.create_line(self.x, self.y1, self.x, self.y2, fill="black")

# --- New Square Class (Rotating Square Wheel) ---
class Square:
    def __init__(self, canvas, converter, side, dtheta):
        self.canvas = canvas
        self.converter = converter
        self.side = side
        # The square's center remains at a constant y:
        self.centerY = side / math.sqrt(2)
        # Start with centerX = 0 (math coordinates)
        self.centerX = 0
        # Initial rotation: theta = 0 means that the bottom vertex is at angle -π/2,
        # which makes the square appear rotated 45° relative to an axis–aligned square.
        self.theta = 0
        self.dtheta = dtheta
        self.square = self.draw_square()
    def get_vertices(self):
        """
        Computes the vertices of the square using a rotation matrix.
        Returns a tuple of eight numbers: (x1, y1, x2, y2, x3, y3, x4, y4),
        corresponding to the bottom, right, top, and left vertices (in math coordinates).
        """
        r = self.side / math.sqrt(2)
        # Base (unrotated) vertices relative to the center:
        base_vertices = (
            (0, -r),  # bottom vertex
            (r, 0),   # right vertex
            (0, r),   # top vertex
            (-r, 0)   # left vertex
        )
        cos_t = math.cos(self.theta)
        sin_t = math.sin(self.theta)
        # Apply the rotation matrix to each base vertex:
        # Instead of storing the points in a list, we unpack the results into variables.
        x1 = self.centerX + (base_vertices[0][0] * cos_t - base_vertices[0][1] * sin_t)
        y1 = self.centerY + (base_vertices[0][0] * sin_t + base_vertices[0][1] * cos_t)
        
        x2 = self.centerX + (base_vertices[1][0] * cos_t - base_vertices[1][1] * sin_t)
        y2 = self.centerY + (base_vertices[1][0] * sin_t + base_vertices[1][1] * cos_t)
        
        x3 = self.centerX + (base_vertices[2][0] * cos_t - base_vertices[2][1] * sin_t)
        y3 = self.centerY + (base_vertices[2][0] * sin_t + base_vertices[2][1] * cos_t)
        
        x4 = self.centerX + (base_vertices[3][0] * cos_t - base_vertices[3][1] * sin_t)
        y4 = self.centerY + (base_vertices[3][0] * sin_t + base_vertices[3][1] * cos_t)
        
        return (x1, y1, x2, y2, x3, y3, x4, y4)

    def draw_square(self):
        vertices = self.get_vertices()
        pts = []
        # Iterate over vertices two at a time (each pair represents x and y)
        for i in range(0, len(vertices), 2):
            x_val = vertices[i]
            y_val = vertices[i+1]
            pts.append(self.converter.xtoh(x_val))
            pts.append(self.converter.ytov(y_val))
        return self.canvas.create_polygon(pts, outline="red", fill="")
    
    def move(self):
        # Update the rotation angle and horizontal position.
        # For rolling without slipping, the horizontal displacement equals (r * dtheta).
        r = self.side / math.sqrt(2)
        self.theta -= self.dtheta
        self.centerX += r * self.dtheta
        self.canvas.delete(self.square)
        self.square = self.draw_square()

# --- Existing Window Class (with minor modification to pass dtheta to Square) ---
class Win:
    def __init__(self, xMin, xMax, yMin, yMax, side, increment):
        self.win = Tk()
        self.win.geometry("600x600")
        self.width = 400 
        self.height = 400
        self.canvas = Plot(self.win, self.width, self.height)
        self.canvas.pack()
        self.canvas.update()
        self.convert = xySystem(xMin, xMax, yMin, yMax, self.width, self.height)
        self.side = side
        self.increment = increment
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
        self.canvas.delete("all")
        self.xAxis = xAxis(self.canvas, self.convert) 
        self.yAxis = yAxis(self.canvas, self.convert)
        self.square = Square(self.canvas, self.convert, self.side, self.increment)
        self.road = Roadway(self.convert,self.canvas,self.side)
        self.road.draw()

    def go(self):
        if not self.isgo:
            self.isgo = True
            self.animate()

    def stop(self):
        self.isgo = False 

    def reset(self):
        self.stop()
        self.setup()

    def animate(self):
        if self.isgo:
            self.square.move()
            self.canvas.update()
            self.canvas.after(200, self.animate)
class Roadway:
    def __init__(self, xysystem, canvas,side):
        self.convert = xysystem
        self.canvas = canvas 
        self.side = side
        self.theta = 0
        self.inc = 0.01
        self.r = self.side / math.sqrt(2)
    def draw(self):
        while(self.theta < math.pi / 2):

            self.currentPointX = self.calculateX(self.theta)
            self.currentPointY = self.calculateY(self.theta)
            self.nextPointX = self.calculateX(self.theta + self.inc)
            self.nextPointY = self.calculateY(self.theta + self.inc)
            self.canvas.create_line(self.currentPointX,self.currentPointY,self.nextPointX,self.nextPointY,fill="black",width=2)
            self.theta += self.inc
    def calculateX(self,t):
        return self.convert.xtoh(t*self.r - self.r * math.sin(t) + self.r / 2 * math.sin(t) * math.cos(t) + self.r / 2 * math.sin(t) * math.sin(t) + self.r / 2 * math.sin(t) * math.sin(t) * math.cos(t) + self.r / 2 * math.sin(t) * math.sin(t) * math.sin(t))
    def calculateY(self,t):
        return self.convert.ytov(self.r - self.r * math.cos(t) - self.r / 2 * math.sin(t) * math.sin(t) + self.r / 2 * math.sin(t) * math.cos(t) - self.r / 2 * math.sin(t) * math.sin(t) * math.sin(t) + self.r / 2 * math.sin(t) * math.sin(t) * math.cos(t))


# --- Main Program ---
xMin = -3.14
xMax = 3.14
yMin = -3.14
yMax = 3.14
side = 3.14  # side length of the square
inc = 0.1     # rotation increment (in radians per frame)
x = Win(xMin, xMax, yMin, yMax, side, inc)
x.win.mainloop()