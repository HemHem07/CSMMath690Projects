# import random

# class Pump:
#     def __init__(self):
#         self.occupied = False
#         self.time_remaining = 0

#     def start(self):
#         if not self.occupied:
#             self.occupied = True
#             self.time_remaining = 3  

#     def pump(self):
#         if self.occupied:
#             self.time_remaining -= 1
#             if self.time_remaining == 0:
#                 self.occupied = False

# class Line:
#     def __init__(self):
#         self.line = []

#     def add(self):
#         self.line.append("-")

#     def remove(self):
#         if self.line:
#             self.line.pop(0)

# class ArrivalManager:
#     def __init__(self):
#         self.num = 1
#         self.den = 3

#     def arrive_or_not(self):
#         return random.randint(self.num, self.den) == 1

# def simulate(total):
#     pump = Pump()
#     line = Line()
#     arrival_manager = ArrivalManager()
#     max = 0

#     for current in range(total):
#         if arrival_manager.arrive_or_not():
#             line.add()
#         if not pump.occupied and line.line:
#             line.remove()
#             pump.start()
#         pump.pump()
#         if not pump.occupied and line.line:
#             line.remove()
#             pump.start()
#         print(f"Minute {current}-{current+1}: Pump: {'occupied' if pump.occupied else 'free'}, Cars in line: {len(line.line)}")

# simulate(60)

import random
class Pump:
    def __init__(self):
        self.occupied = False
        self.time_remaining = 0

    def start(self):
        if not self.occupied:
            self.occupied = True
            self.time_remaining = 3  

    def pump(self):
        if self.occupied:
            self.time_remaining -= 1
            if self.time_remaining == 0:
                self.occupied = False

class Line:
    def __init__(self):
        self.line = []

    def add(self):
        self.line.append("-")

    def remove(self):
        if self.line:
            self.line.pop(0)

class ArrivalManager:
    def __init__(self):
        self.num = 1
        self.den = 3

    def arrive_or_not(self):
        return random.randint(self.num, self.den) == 1

def simulate(total):
    pump = Pump()
    line = Line()
    arrival_manager = ArrivalManager()
    max_length = 0

    for current in range(total):
        if arrival_manager.arrive_or_not():
            line.add()
        if not pump.occupied and line.line:
            line.remove()
            pump.start()
        pump.pump()
        if not pump.occupied and line.line:
            line.remove()
            pump.start()
        current_length = len(line.line)
        if current_length > max_length:
            max_length = current_length

    return max_length

num_simulations = 100
lengths = []  

for i in range(num_simulations):
    result = simulate(60)
    if result >= len(lengths):
        lengths.extend([0] * (result - len(lengths) + 1))
    lengths[result] += 1
    
bar_chart = "\n".join(f"{i} -- {'*' * freq}" for i, freq in enumerate(lengths) if freq > 0)

print(bar_chart)
