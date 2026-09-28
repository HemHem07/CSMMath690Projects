import random

class Dice:
    def roll(self):
        return int(6 * random.random() + 1) + int(6 * random.random() + 1)

class FirstRoll:
    def __init__(self):
        self.dice = Dice()
        self.point = 0

    def first_roll(self):  
        return self.dice.roll()
        
    def returnResult(self, roll):
        if roll == 7 or roll == 11:
            return "win"
        elif roll == 2 or roll == 3 or roll == 12:
            return "lose"
        else: 
            self.point = roll
        return self.point
    # split this up into 2 methods: one to do the first roll, the second to do the logic of it ()with an inputted number) so that it can be pslit up. 

class Point:
    def __init__(self, point):
        self.point = point
        self.dice = Dice()

    def continue_game(self, debug=False):
        while True:
            roll = self.dice.roll()

            if debug == True:
                print(f"Rolled: {roll}")

            if roll == self.point:
                return "win"
            elif roll == 7:
                return "lose"

class Game:
    def __init__(self, debug=False):
        self.dice = Dice()
        self.firstRoll = FirstRoll()
        self.cont = True
        self.result = None
        self.point = None
        self.debug = debug  

    def game(self):
        self.point = self.firstRoll.returnResult(self.firstRoll.first_roll())

        if self.debug:
            print(f"First roll result: {self.point}")

        if self.point == "win":
            return "win"
        elif self.point == "lose":
            return "lose"

        point_game = Point(self.point)
        return point_game.continue_game(debug=self.debug)

game = Game(debug=False) 
result = game.game()
print(f"Game result: {result}")

def simulation(num):
    game = Game(debug = False)
    wins = 0
    for i in range(num):
        result = game.game()
        if result == "win":
            wins += 1
    return wins 
def bigSimulation(num1,num2):
    results = []
    for i in range(num1):
        results.append(simulation(num2))
    return results

thing = bigSimulation(10,10000)
print(thing)
sum = 0
for item in thing: 
    sum += item
sum = sum/len(thing)    
print(sum/10000)