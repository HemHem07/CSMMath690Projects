class reversePolishNotation():
    def __init__(self, equation):
        self.eq = equation
        self.i = -1

    def returnNext(self):
        self.i += 1
        if self.i < len(self.eq):
            return self.eq[self.i]
        else:
            return -1

    def print(self):
        print(self.eq)


class Computer():
    def __init__(self, equation):
        self.rpn = reversePolishNotation(equation)
        self.stack = []

    def isInt(self, char):
        if char == '+' or char == '-' or char == '*' or char == '/':
            return False
        else:
            return True

    def compute(self, int1, int2, operator):
        if operator == '+':
            return int1 + int2
        elif operator == '-':
            return int1 - int2
        elif operator == '*':
            return int1 * int2
        else:
            return int1 / int2

    def computeExpression(self):
        go = True
        while go:
            char = self.rpn.returnNext()
            if char == -1:
                go = False
            elif self.isInt(char):
                self.stack.append(int(char))
            else:
                result = self.compute(self.stack[-2], self.stack[-1], char)
                self.stack.pop()
                self.stack.pop()
                self.stack.append(result)
        return self.stack

    def print(self):
        self.rpn.print()
    def returnResult(self):
        self.result = computeExpression()
        return self.result[0] 
class Parser(): 
    def __init__(self, equation):
        self.equation = equation

    def split(self):
        return self.equation.find('-')  # Find the index of '-'
        

    def returnLeft(self):
        if (self.split() > 0):
            return self.equation[:self.split()]  # Return everything before '-'

    def returnRight(self):
        if (self.split() > 0):

            return self.equation[self.split() + 1:]  # Return everything after '-'

    def returnMiddle(self):
        if (self.split() > 0):
            return self.equation[self.split()]  # Return the '-' itself

    
        
class Tree:
    def __init__(self, target):
        self.leftFlag = True
        self.rightFlag = True
        if len(target) != 0:
            x = self.findOperator(target, "+")
            if x == -1:
                x = self.findOperator(target, "-")
            if x == -1:
                x = self.findOperator(target, "*")
            if x == -1:
                x = self.findOperator(target, "/")
            if x != -1:
                left = target[:x]
                right = target[x+1:]
                self.node = target[x]
            else:
                left = ""
                right = ""
                self.node = target
            if len(left) > 0:
                self.leftTree = Tree(left)
            else:
                self.leftFlag = False
            if len(right) > 0:
                self.rightTree = Tree(right)
            else:
                self.rightFlag = False

    def print(self):
        print(self.node)
        if self.leftFlag:
            self.leftTree.print()
        if self.rightFlag:
            self.rightTree.print()

    def findOperator(self, string, operator):
        i = 0
        returnVal = -1
        while i < len(string):
            if string[i] == operator:
                returnVal = i
                break
            i += 1
        return returnVal

    def traverseLeft(self):
        returnVal = ""
        if self.leftFlag:
            returnVal += self.leftTree.traverseLeft()
        if self.rightFlag:
            returnVal += self.rightTree.traverseLeft()
        returnVal += self.node
        return returnVal

# x = Computer([5,3,"+",12,15,"+","*"])
# print(x.computeExpression())

x="2+5-6*7+4"
tree = Tree(x)
# tree.print()
print(tree.traverseLeft())
computer = Computer(tree.traverseLeft())
result = computer.returnResult()
print(result)
# next: after plus, check for minus. 
# then *, then /
# test case: 2 + 5 - 6 + 7
# print("hello"[0:-1])
# print(tree.findPlus(['2','3','+','5']))