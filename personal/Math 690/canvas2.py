from tkinter import *
from tkinter import messagebox
import random

# ----------------------- Point Class -----------------------

class Point:
    def __init__(self, x, y):
        self.x = x  # Logical X coordinate
        self.y = y  # Logical Y coordinate

    def to_canvas_coordinates(self, minX, maxX, minY, maxY, canvas_width, canvas_height):
        """Convert logical coordinates to canvas coordinates."""
        canvas_x = (self.x - minX) / (maxX - minX) * canvas_width
        canvas_y = canvas_height - (self.y - minY) / (maxY - minY) * canvas_height
        return canvas_x, canvas_y

    def plot(self, canvas_widget, minX, maxX, minY, maxY, canvas_width, canvas_height, radius=2, color="white"):
        """Plot the point on the canvas."""
        canvas_x, canvas_y = self.to_canvas_coordinates(minX, maxX, minY, maxY, canvas_width, canvas_height)
        canvas_widget.draw_oval(canvas_x - radius, canvas_y - radius, canvas_x + radius, canvas_y + radius, fill=color, outline="")

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

# ----------------------- Vector Class -----------------------

class Vector: 
    def __init__(self, x, y): 
        self.x = x
        self.y = y 

    def print_info(self):
        print(f'[{self.x}, {self.y}]')

    def addTo(self, vec):
        newX = self.x + vec.getX()
        newY = self.y + vec.getY()
        return Vector(newX, newY)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

# ----------------------- Matrix Class -----------------------

class Matrix: 
    def __init__(self, a, b, c, d): 
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def print_info(self):
        print(f'[{self.a}  {self.b}]')
        print(f'[{self.c}  {self.d}]')

    def timesVect(self, vec):
        newX = self.a * vec.getX() + self.b * vec.getY()
        newY = self.c * vec.getX() + self.d * vec.getY()
        return Vector(newX, newY)

# ----------------------- Function Class -----------------------

class Function: 
    def __init__(self, Matrix, Vector):
        self.Matrix = Matrix
        self.Vector = Vector

    def print_info(self):
        print("f(x,y) = ")
        self.Matrix.print_info()
        print("* [x, y]")
        print("     + ", end="")
        self.Vector.print_info()

    def outFromVec(self, vector):
        firstVector = self.Matrix.timesVect(vector)
        returnVector = firstVector.addTo(self.Vector)
        return returnVector

# ----------------------- ListOfFuncs Class -----------------------

class ListOfFuncs:
    def __init__(self):
        self.list = []

    def addFunct(self, function):
        self.list.append(function)

    def output(self, n, vector):
        if n < 1 or n > len(self.list):
            raise ValueError("Function index out of range")
        function = self.list[n-1]
        return function.outFromVec(vector)

    def length(self):
        return len(self.list)

    def print_info(self):
        for idx, item in enumerate(self.list, start=1):
            print(f"Function {idx}:")
            item.print_info()

# ----------------------- Calculations Class -----------------------

class Calculations:
    def __init__(self, ListOfFunctions, Vector):
        self.listOfFunctions = ListOfFunctions
        self.length = ListOfFunctions.length()

    def applyTransformation(self, n, vector):
        self.result = self.listOfFunctions.output(n, vector)

    def returnResult(self):
        return self.result

# ----------------------- Manager Class -----------------------

class Manager: 
    def __init__(self, ListOfFunctions, calculations, Vector, num, Function):
        self.length = ListOfFunctions.length()
        self.listOfFunctions = ListOfFunctions
        self.vector = Vector
        self.num = num
        self.function = Function
        self.calculations = Calculations(self.listOfFunctions, self.vector)

    def run(self, num):
        for i in range(num):
            functionNum = random.randint(1, self.length)
            # Apply the nth function to the current vector
            self.vector = self.calculations.output(functionNum, self.vector)

# ----------------------- CanvasWidget Class -----------------------

class CanvasWidget:
    def __init__(self, parent, width, height, bg="black"):
        self.canvas = Canvas(parent, width=width, height=height, bg=bg)
        self.canvas.pack()
        self.width = width
        self.height = height

    def draw_line(self, x1, y1, x2, y2, **kwargs):
        self.canvas.create_line(x1, y1, x2, y2, **kwargs)

    def draw_text(self, x, y, text, **kwargs):
        self.canvas.create_text(x, y, text=text, **kwargs)

    def draw_oval(self, x1, y1, x2, y2, **kwargs):
        self.canvas.create_oval(x1, y1, x2, y2, **kwargs)

    def clear_canvas(self):
        self.canvas.delete("all")

    def print_info(self):
        print(f"Canvas size: {self.width}x{self.height}")

# ----------------------- BoundsEntry Class -----------------------

class BoundsEntry:
    def __init__(self, parent):
        self.frame = Frame(parent)
        self.frame.pack(pady=10)

        # Labels
        Label(self.frame, text="Min X").grid(row=0, column=0, padx=5)
        Label(self.frame, text="Min Y").grid(row=0, column=2, padx=5)
        Label(self.frame, text="Max X").grid(row=0, column=4, padx=5)
        Label(self.frame, text="Max Y").grid(row=0, column=6, padx=5)

        # Entries
        self.minX = Entry(self.frame, width=10)
        self.minY = Entry(self.frame, width=10)
        self.maxX = Entry(self.frame, width=10)
        self.maxY = Entry(self.frame, width=10)

        self.minX.grid(row=0, column=1)
        self.minY.grid(row=0, column=3)
        self.maxX.grid(row=0, column=5)
        self.maxY.grid(row=0, column=7)

        # Set default values
        self.minX.insert(0, "-5.0")
        self.minY.insert(0, "-5.0")
        self.maxX.insert(0, "5.0")
        self.maxY.insert(0, "5.0")

    def get_bounds(self):
        try:
            minX = float(self.minX.get())
            minY = float(self.minY.get())
            maxX = float(self.maxX.get())
            maxY = float(self.maxY.get())
            return minX, maxX, minY, maxY
        except ValueError:
            print("Invalid input for bounds. Please enter numeric values.")
            return -5.0, 5.0, -5.0, 5.0  # Fallback to default

    def print_info(self):
        print(f"Bounds: MinX={self.minX.get()}, MaxX={self.maxX.get()}, MinY={self.minY.get()}, MaxY={self.maxY.get()}")

# ----------------------- ActionButtons Class -----------------------

class ActionButtons:
    def __init__(self, main_window):
        self.main_window = main_window

        self.frame = Frame(self.main_window.window)
        self.frame.pack(pady=10)

        self.change_bounds_button = Button(self.frame, text="Change Bounds", command=self.change_bounds)
        self.change_bounds_button.pack(side=LEFT, padx=5)

        self.define_functions_button = Button(self.frame, text="Define Functions", command=self.define_functions)
        self.define_functions_button.pack(side=LEFT, padx=5)

        self.generate_points_button = Button(self.frame, text="Generate Points", command=self.generate_points)
        self.generate_points_button.pack(side=LEFT, padx=5)

        self.clear_points_button = Button(self.frame, text="Clear Points", command=self.clear_points)
        self.clear_points_button.pack(side=LEFT, padx=5)

        self.run_full_process_button = Button(self.frame, text="Run Full 75,000 Process", command=self.run_full_process)
        self.run_full_process_button.pack(side=LEFT, padx=5)

    def change_bounds(self):
        self.main_window.create_lines()
        print("Bounds changed.")

    def define_functions(self):
        FunctionInputWindow(self.main_window)
        print("Opened Function Definition Window.")

    def generate_points(self):
        self.main_window.generate_points(num_points=50)
        print("Generated 50 points.")

    def run_full_process(self):
        self.main_window.generate_points(num_points=100000)
        print("Ran full 75,000 point generation process.")

    def clear_points(self):
        self.main_window.clear_points()
        print("Cleared points.")

    def print_info(self):
        print("Action Buttons: Change Bounds, Define Functions, Generate Points, Clear Points, Run Full Process")

# ----------------------- FunctionInputWindow Class -----------------------

class FunctionInputWindow:
    def __init__(self, main_window):
        self.main_window = main_window
        self.window = Toplevel()
        self.window.title("Define Transformation Functions")
        self.window.geometry("500x600")

        # Prompt for the number of functions
        Label(self.window, text="Enter the number of functions:").pack(pady=10)
        self.num_functions_entry = Entry(self.window)
        self.num_functions_entry.pack(pady=5)
        Button(self.window, text="Submit", command=self.submit_num_functions).pack(pady=5)

    def submit_num_functions(self):
        try:
            self.num_functions = int(self.num_functions_entry.get())
            if self.num_functions <= 0:
                raise ValueError
            self.window.destroy()
            self.create_function_entries()
        except ValueError:
            print("Please enter a valid positive integer.")
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer.")

    def create_function_entries(self):
        self.entries_window = Toplevel()
        self.entries_window.title("Input Functions")
        self.entries_window.geometry("600x800")
        self.entries = []

        for i in range(self.num_functions):
            Label(self.entries_window, text=f"Function {i+1}", font=("Arial", 12, "bold")).pack(pady=10)

            frame = Frame(self.entries_window)
            frame.pack(pady=5)

            # Matrix Entries
            Label(frame, text="Matrix [a b; c d]").grid(row=0, column=0, columnspan=4, pady=2)
            a_entry = Entry(frame, width=5)
            b_entry = Entry(frame, width=5)
            c_entry = Entry(frame, width=5)
            d_entry = Entry(frame, width=5)
            a_entry.grid(row=1, column=0, padx=2)
            b_entry.grid(row=1, column=1, padx=2)
            c_entry.grid(row=1, column=2, padx=2)
            d_entry.grid(row=1, column=3, padx=2)

            # Vector Entries
            Label(frame, text="Vector [e; f]").grid(row=2, column=0, columnspan=4, pady=2)
            e_entry = Entry(frame, width=5)
            f_entry = Entry(frame, width=5)
            e_entry.grid(row=3, column=0, padx=2)
            f_entry.grid(row=3, column=1, padx=2)

            self.entries.append({
                'a': a_entry,
                'b': b_entry,
                'c': c_entry,
                'd': d_entry,
                'e': e_entry,
                'f': f_entry
            })

        Button(self.entries_window, text="Add All Functions", command=self.add_functions).pack(pady=20)

    def add_functions(self):
        try:
            for idx, entry in enumerate(self.entries):
                a = float(entry['a'].get())
                b = float(entry['b'].get())
                c = float(entry['c'].get())
                d = float(entry['d'].get())
                e = float(entry['e'].get())
                f = float(entry['f'].get())

                matrix = Matrix(a, b, c, d)
                vector = Vector(e, f)
                function = Function(matrix, vector)
                self.main_window.list_of_funcs.addFunct(function)

                print(f"Added Function {idx+1}:")
                function.print_info()

            self.entries_window.destroy()
            messagebox.showinfo("Success", "All functions have been added successfully!")
        except ValueError:
            print("Please enter valid numeric values for all matrix and vector entries.")
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for all matrix and vector entries.")

# ----------------------- MainWindow Class -----------------------

class MainWindow:
    def __init__(self, width, height):
        self.window = Tk()
        self.window.geometry(f"{width}x{height}")
        self.window.title("Point Plotter")
        self.width = width
        self.height = height
        self.canvas_width = self.width / 2
        self.canvas_height = self.height / 2

        # Initialize components
        self.bounds_entry = BoundsEntry(self.window)
        self.canvas_widget = CanvasWidget(self.window, self.canvas_width, self.canvas_height)
        self.action_buttons = ActionButtons(self)

        # Quit Button
        quit_button = Button(self.window, text="Quit", command=self.quit)
        quit_button.pack(pady=10)

        # Set default bounds
        self.minX = -5.0
        self.maxX = 5.0
        self.minY = -5.0
        self.maxY = 5.0

        # Initialize mathematical components
        self.list_of_funcs = ListOfFuncs()
        self.calculations = Calculations(self.list_of_funcs, Vector(1, 1))  # Starting Vector is (1,1)

    def quit(self):
        self.window.destroy()

    def create_lines(self):
        self.minX, self.maxX, self.minY, self.maxY = self.bounds_entry.get_bounds()

        self.canvas_widget.clear_canvas()

        width = self.canvas_width
        height = self.canvas_height

        label_offset_y = height * 0.02
        label_offset_x = width * 0.02

        # Draw vertical lines
        for i in range(int(self.minX), int(self.maxX) + 1):
            x = (i - self.minX) / (self.maxX - self.minX) * width
            line_width = 3 if i == 0 else 1
            self.canvas_widget.draw_line(x, 0, x, height, width=line_width, fill="gray")
            if i != 0 and i % 2 == 0:
                y_zero = (0 - self.minY) / (self.maxY - self.minY) * height
                y_zero = height - y_zero  # Invert y-axis
                self.canvas_widget.draw_text(x + label_offset_x, y_zero + label_offset_y, text=str(i), anchor=N, fill="white")

        # Draw horizontal lines
        for i in range(int(self.minY), int(self.maxY) + 1):
            y = (i - self.minY) / (self.maxY - self.minY) * height
            y = height - y  # Invert y-axis
            line_width = 3 if i == 0 else 1
            self.canvas_widget.draw_line(0, y, width, y, width=line_width, fill="gray")
            if i != 0 and i % 2 == 0:
                x_zero = (0 - self.minX) / (self.maxX - self.minX) * width
                self.canvas_widget.draw_text(x_zero - label_offset_x, y + label_offset_y, text=str(i), anchor=E, fill="white")

    def generate_points(self, num_points=50):
        minX, maxX, minY, maxY = self.minX, self.maxX, self.minY, self.maxY

        # Initialize the starting point
        initial_point = Point(1, 1)  # Starting at (1,1)
        initial_point.plot(self.canvas_widget, minX, maxX, minY, maxY, self.canvas_width, self.canvas_height)

        current_vector = Vector(1, 1)  # Starting vector

        for _ in range(num_points):
            if self.list_of_funcs.length() == 0:
                print("No functions defined. Please add functions first.")
                messagebox.showerror("No Functions", "Please define transformation functions before generating points.")
                break
            function_num = random.randint(1, self.list_of_funcs.length())
            transformed_vector = self.list_of_funcs.output(function_num, current_vector)

            # Create and plot the new point
            new_point = Point(transformed_vector.getX(), transformed_vector.getY())
            new_point.plot(self.canvas_widget, minX, maxX, minY, maxY, self.canvas_width, self.canvas_height)

            # Update the current vector
            current_vector = transformed_vector

    def clear_points(self):
        self.canvas_widget.clear_canvas()
        self.create_lines()

    def run(self):
        self.create_lines()
        self.window.mainloop()

    def print_info(self):
        print(f"Window size: {self.width}x{self.height}")
        self.bounds_entry.print_info()
        self.canvas_widget.print_info()
        self.action_buttons.print_info()

# ----------------------- Main Function -----------------------

def main():
    height = 800
    width = 800

    main_window = MainWindow(width, height)
    main_window.print_info()

    # # Predefine Sierpinski's Triangle functions
    # A = Matrix(0.5, 0, 0, 0.5)
    # a = Vector(0, 0)
    # b = Vector(0.5, 0)
    # c = Vector(0.25, 0.433)  # Approximately height of an equilateral triangle with side length 0.5
    # f1 = Function(A, a)
    # f2 = Function(A, b)
    # f3 = Function(A, c)

    # main_window.list_of_funcs.addFunct(f1)
    # main_window.list_of_funcs.addFunct(f2)
    # main_window.list_of_funcs.addFunct(f3)

    # print("Predefined Sierpinski's Triangle functions added.")
    main_window.run()

main()
# make it so its not in sep window, only one set of input, not x num of funcs. 