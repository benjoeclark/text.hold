#!/usr/bin/env python
import random
import sys
import os
import time
import math

cellSymbols = ['*', '.', '>', '@', '^']
SPACE = ' '
WALLS = ['#', '|', '-']

def sign(value):
    return 1 if value > 0 else -1

def abs(value):
    if sign(value) == -1:
        return -1 * value
    return value

def distance(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2)

class Hold(object):
    def __init__(self, level=1, data=None):
        if data is None:
            self.width = 10
            self.height = 10
            self.cells = []
            verticalWalls = [10, 20, 30, 40, 50, 60, 70, 80,
                19, 29, 39, 49, 59, 69, 79, 89]
            horizontalWalls = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
                25, 26, 27, 28,
                41, 42, 43, 44, 45,
                65, 66, 67, 68]
            for cell in xrange(self.width*self.height):
                if cell in verticalWalls:
                    self.cells.append(Wall('#'))
                elif cell in horizontalWalls:
                    self.cells.append(Wall('#'))
                else:
                    self.cells.append(Cell())
            self.adventurer = Adventurer(level)
            self.mobs = [self.adventurer]
            self.cells[self.getValidPosition()] = self.adventurer
            for mob in xrange(10):
                self.mobs.append(Mob())
                self.cells[self.getValidPosition()] = self.mobs[-1]
        else:
            self.width = None
            self.height = data.count('\n')
            self.adventurer = Adventurer(level)
            self.mobs = [self.adventurer]
            index = 0
            self.cells = []
            for element in data:
                if element == '\n':
                    if self.width is None:
                        self.width = index
                elif element == '@':
                    self.cells.append(self.adventurer)
                elif element == '#':
                    self.cells.append(Wall('#'))
                elif element == '*':
                    self.mobs.append(Mob())
                    self.cells.append(self.mobs[-1])
                elif element == 'H':
                    self.mobs.append(Human())
                    self.cells.append(self.mobs[-1])
                elif element == 'E':
                    self.mobs.append(Elf())
                    self.cells.append(self.mobs[-1])
                elif element == 'D':
                    self.mobs.append(Dragon())
                    self.cells.append(self.mobs[-1])
                elif element == 'd':
                    self.mobs.append(Dwarf())
                    self.cells.append(self.mobs[-1])
                elif element == 's':
                    self.mobs.append(Snake())
                    self.cells.append(self.mobs[-1])
                elif element == 'k':
                    self.mobs.append(Kobold())
                    self.cells.append(self.mobs[-1])
                elif element == 'h':
                    self.mobs.append(Halfling())
                    self.cells.append(self.mobs[-1])
                elif element == 'l':
                    self.mobs.append(Lizard())
                    self.cells.append(self.mobs[-1])
                elif element == 'W':
                    self.mobs.append(Wizard())
                    self.cells.append(self.mobs[-1])
                else:
                    self.cells.append(Cell())
                if element != '\n':
                    index += 1

    def update(self):
        for mob in self.mobs:
            if not mob.dead:
                view = self.getView(mob)
                mob.show(view, self)
        for mob in self.mobs:
            if mob.dead:
                self.mobs.pop(self.mobs.index(mob))

    def checkGameOver(self):
        if self.adventurer not in self.mobs:
            return False
        if len(self.mobs) <= 1:
            return False
        return True

    def getView(self, character):
        index = self.cells.index(character)
        position = self.calculatePosition(index)
        view = []
        for cellIndex in xrange(len(self.cells)):
            if index != cellIndex:
                cellPosition = self.calculatePosition(cellIndex)
                vector = [cellPosition[0] - position[0], cellPosition[1] - position[1]]
                if distance(vector) <= character.range:
                    view.append((vector, self.cells[cellIndex]))
        return self.filterView(view)

    def filterView(self, view):
        toRemove = []
        for index in range(len(view)):
            for other in range(len(view)):
                if index != other:
                    pos = view[index][0]
                    dist = distance(pos)
                    otherPos = view[other][0]
                    otherDist = distance(otherPos)
                    if otherDist < dist and self.dotProduct(pos, otherPos) > 0:
                        if self.perpendicularSquared(pos, otherPos) < 0.5 and \
                            view[other][1].symbol in WALLS:
                            toRemove.append(index)
                            break
        toRemove.reverse()
        for index in toRemove:
            view.pop(index)
        return view

    def dotProduct(self, v1, v2):
        return v1[0]*v2[0] + v1[1]*v2[1]

    def perpendicularSquared(self, v1, v2):
        return v2[0]**2+v2[1]**2 - self.dotProduct(v1, v2)**2/float(v1[0]**2+v1[1]**2)

    def attack(self, attacker, defender):
        defender.hp -= attacker.ap
        if defender.hp <= 0:
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

class Wall(Cell):
    def __init__(self, symbol='|'):
        self.symbol = symbol
        self.range = 0
        self.dead = False

class Mob(Cell):
    def __init__(self, symbol='*'):
        self.setAttributes(symbol, range=2, movement=1)

    def setAttributes(self, symbol='*', range=1, movement=1, weaponRange=1, hp=4, ap=1, local=True):
        self.symbol = symbol
        self.range = range
        self.movement = movement
        self.weaponRange = weaponRange
        self.maxhp = hp
        self.hp = hp
        self.ap = ap
        self.local = local
        self.dead = False

    def show(self, view, hold):
        targets = []
        directions = []
        for v in view:
            vector, mob = v
            if mob.range > 0 and self.local != mob.local:
                targets.append((distance(vector), mob))
            elif mob.symbol == ' ' and distance(vector) <= self.movement:
                directions.append(vector)
        if len(targets) > 0:
            dist, target = self.getTarget(targets)
            if dist > self.weaponRange:
                # move toward target
                direction = None
                for v in view:
                    vector, mob = v
                    if mob == target:
                        direction = vector
                movesLeft = self.movement
                x = 0
                y = 0
                while movesLeft > 0 and distance([direction[0]-x, direction[1]-y]) > self.weaponRange:
                    if abs(direction[0] - x) > abs(direction[1] - y) and [x+sign(direction[0]), y] in directions:
                        x += sign(direction[0])
                    elif [x, y+sign(direction[1])] in directions:
                        y += sign(direction[1])
                    else:
                        break
                hold.move(self, self.chooseDirection(([x, y],)))
            else:
                hold.attack(self, target)
        elif len(directions) > 0:
            hold.move(self, self.chooseDirection(directions))

    def chooseDirection(self, directions):
        return random.choice(directions)

    def getTarget(self, targets):
        nearest = targets[0][1]
        dist = targets[0][0]
        for target in targets[1:]:
            if target[0] < dist:
                dist = target[0]
                nearest = target[1]
        return dist, nearest

    def __str__(self):
        return self.symbol + ' ' + '+'*self.hp

class Human(Mob):
    def __init__(self, symbol='H'):
        self.setAttributes(symbol, range=3, movement=2, weaponRange=1, hp=10, ap=2, local=True)

class Elf(Mob):
    def __init__(self, symbol='E'):
        self.setAttributes(symbol, range=5, movement=3, weaponRange=3, hp=8, ap=3, local=True)

class Dragon(Mob):
    def __init__(self, symbol='D'):
        self.setAttributes(symbol, range=5, movement=1, weaponRange=3, hp=20, ap=6, local=True)

class Dwarf(Mob):
    def __init__(self, symbol='d'):
        self.setAttributes(symbol, range=3, movement=1, weaponRange=1, hp=20, ap=3, local=True)

class Snake(Mob):
    def __init__(self, symbol='s'):
        self.setAttributes(symbol, range=2, movement=1, weaponRange=1, hp=2, ap=1, local=True)

class Kobold(Mob):
    def __init__(self, symbol='k'):
        self.setAttributes(symbol, range=3, movement=1, weaponRange=1, hp=2, ap=1, local=True)

class Halfling(Mob):
    def __init__(self, symbol='h'):
        self.setAttributes(symbol, range=4, movement=2, weaponRange=1, hp=8, ap=1, local=True)

class Lizard(Mob):
    def __init__(self, symbol='l'):
        self.setAttributes(symbol, range=2, movement=2, weaponRange=1, hp=1, ap=1, local=True)

class Wizard(Mob):
    def __init__(self, symbol='W'):
        self.setAttributes(symbol, range=6, movement=1, weaponRange=4, hp=6, ap=6, local=True)

class Adventurer(Mob):
    def __init__(self, level=1, symbol='@'):
        self.setAttributes(symbol, range=1, movement=1, weaponRange=1, hp=1, ap=1, local=False)
        self.levelUp(level)
        self.x = 0
        self.y = 0
        self.map = [[self.x, self.y]]

    def levelUp(self, level):
        abilities = ['range']*6
        abilities += ['movement']
        abilities += ['weaponRange']
        abilities += ['maxhp']*10
        abilities += ['ap']*3
        for lvl in range(level):
            ability = random.choice(abilities)
            exec('self.' + ability + ' += 1')
        self.hp = self.maxhp

    def __str__(self):
        return self.symbol + ' r' + str(self.range) + ' m' + str(self.movement) + ' w' + str(self.weaponRange) + ' a' + str(self.ap) + ' ' + '+'*self.hp

    def chooseDirection(self, directions):
        # translate directions
        frameDirections = [[el[0]+self.x, el[1]+self.y] for el in directions]
        unexplored = []
        for direction in frameDirections:
            if direction not in self.map:
                unexplored.append(direction)
        destination = random.choice(frameDirections + unexplored)
        if destination in unexplored:
            self.map.append(destination)
        vector = [destination[0] - self.x, destination[1] - self.y]
        self.x += vector[0]
        self.y += vector[1]
        return vector

class Game(object):
    def __init__(self, holdFolder=None):
        if holdFolder is not None:
            holdData = open(os.path.join(holdFolder, 'hold'), 'r').read()
            holdAccount = open(os.path.join(holdFolder, 'account'), 'r').read()
        level = self.getLevel(holdData, holdAccount)
        self.hold = Hold(level, holdData)
        self.running = False
        self.fps = 1

    def getLevel(self, data, account):
        accountLines = account.split('\n')
        money = int(accountLines[0])
        level = money/100
        for line in accountLines[1:]:
            lineSplit = line.split()
            if len(lineSplit) >= 3:
                symbol = lineSplit[0]
                creatureLevel = int(lineSplit[1])
                creatureQuantity = int(lineSplit[2])
                level += creatureLevel*creatureQuantity
        return level

    def play(self):
        self.running = True
        while self.running:
            print '\n'*100
            for mob in self.hold.mobs:
                print mob
            print self.hold
            self.running = self.hold.checkGameOver()
            self.hold.update()
            time.sleep(1./self.fps)

def main():
    if len(sys.argv) > 1:
        holdFolder = sys.argv[-1]
        game = Game(holdFolder)
    else:
        game = Game()
    game.play()

if __name__ == '__main__':
    main()
