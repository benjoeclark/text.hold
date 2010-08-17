#!/usr/bin/env python
import random
import time
import math

cellSymbols = ['*', '.', '>', '@', '^']

class Hold(object):
    def __init__(self):
        self.width = 10
        self.height = 10
        self.cells = []
        for cell in xrange(self.width*self.height):
            self.cells.append(Cell())
        self.adventurer = Adventurer()
        self.mobs = [self.adventurer]
        self.cells[self.getValidPosition()] = self.adventurer
        for mob in xrange(10):
            self.mobs.append(Mob())
            self.cells[self.getValidPosition()] = self.mobs[-1]

    def update(self):
        for mob in self.mobs:
            if not mob.dead:
                view = self.getView(mob)
                mob.show(view, self)
        for mob in self.mobs:
            if mob.dead:
                self.mobs.pop(self.mobs.index(mob))

    def getView(self, character):
        index = self.cells.index(character)
        position = self.calculatePosition(index)
        view = []
        for cellIndex in xrange(len(self.cells)):
            if index != cellIndex:
                cellPosition = self.calculatePosition(cellIndex)
                vector = [cellPosition[0] - position[0], cellPosition[1] - position[1]]
                if self.distance(vector) <= character.range:
                    view.append((vector, self.cells[cellIndex]))
        return view

    def attack(self, attacker, defender):
        index = self.cells.index(defender)
        defender.dead = True
        self.cells[index] = Cell()

    def move(self, mover, direction):
        if direction != [0, 0]:
            origin = self.cells.index(mover)
            position = self.calculatePosition(origin)
            destination = self.calculateIndex([position[0]+direction[0], position[1]+direction[1]])
            self.cells[destination] = mover
            self.cells[origin] = Cell()

    def distance(self, vector):
        return math.sqrt(vector[0]**2 + vector[1]**2)

    def calculatePosition(self, index):
        x = index % self.width
        y = index / self.width
        return [x, y]

    def calculateIndex(self, position):
        return position[1] * self.width + position[0]

    def getValidPosition(self):
        position = None
        while not self.isValidPosition(position):
            position = random.randint(0, self.height-1) * self.width + random.randint(0, self.width-1)
        return position

    def isValidPosition(self, position):
        if position is None:
            return False
        if self.cells[position].symbol != ' ':
            return False
        return True

    def __str__(self):
        output = []
        for row in xrange(self.height):
            output.append('')
            for column in xrange(self.width):
                output[-1] += self.cells[row*self.width + column].symbol
        return '\n'.join(output)

class Cell(object):
    def __init__(self, symbol=' '):
        self.symbol = symbol
        self.range = 0
        self.dead = False

class Adventurer(Cell):
    def __init__(self, symbol='@'):
        self.symbol = symbol
        self.range = 3
        self.movement = 2
        self.dead = False

    def show(self, view, hold):
        target = None
        directions = []
        for v in view:
            vector, mob = v
            if mob.symbol != ' ':
                target = mob
            elif hold.distance(vector) <= self.movement:
                directions.append(vector)
        if target is not None:
            hold.attack(self, target)
        elif len(directions) > 0:
            hold.move(self, random.choice(directions))

class Mob(Cell):
    def __init__(self, symbol='*'):
        self.symbol = symbol
        self.range = 1
        self.movement = 1
        self.dead = False

    def show(self, view, hold):
        directions = [[0, 0]]
        for v in view:
            vector, mob = v
            if mob.symbol == ' ' and hold.distance(vector) <= self.movement:
                directions.append(vector)
        if len(directions) > 0:
            hold.move(self, random.choice(directions))

class Game(object):
    def __init__(self):
        self.hold = Hold()
        self.running = False
        self.fps = 1

    def play(self):
        self.running = True
        while self.running:
            print '\n'*100
            print self.hold
            self.hold.update()
            time.sleep(1./self.fps)

def main():
    game = Game()
    game.play()

if __name__ == '__main__':
    main()
