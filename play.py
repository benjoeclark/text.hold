#!/usr/bin/env python

import sys
import time
import random


class Entity(object):
    def is_mob(self):
        return False


class Mob(Entity):
    def __init__(self, symbol):
        self.symbol = symbol

    def is_mob(self):
        return True

    def get_action(self, view):
        return Move(random.choice(view.poi))

class Adventurer(Mob):
    def __init__(self, symbol):
        self.symbol = symbol

    def get_action(self, view):
        for poi in view.poi:
            if 'mob' in dir(poi):
                return Attack(poi)
        return Move(random.choice(view.poi))


class Wall(Entity):
    def __init__(self):
        self.symbol = '#'


class Empty(Entity):
    def __init__(self):
        self.symbol = ' '


class Poi(object):
    pass


class Direction(Poi):
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def __str__(self):
        return str(self.dx) + ' ' + str(self.dy)


class View(object):
    def __init__(self):
        self.poi = []

    def append(self, poi):
        self.poi.append(poi)

    def __str__(self):
        output = ''
        for poi in self.poi:
            output += str(poi)
        return output


class Action(object):
    pass


class Move(Action):
    def __init__(self, direction):
        self.dx = direction.dx
        self.dy = direction.dy

    def __str__(self):
        return 'move ' + str(self.dx) + ' ' + str(self.dy)


class Attack(Action):
    def __init__(self, target):
        self.mob = target.mob

    def __str__(self):
        return 'attack ' + str(self.mob)


class Hold(object):
    def __init__(self, initial_data):
        self.height = initial_data.count('\n')
        self.width = len(initial_data.split('\n')[0])
        self.data = self.parse(initial_data)

    def parse(self, data_in):
        data = []
        for c in data_in:
            if c == '#':
                data.append(Wall())
            elif c == ' ':
                data.append(Empty())
            elif c == '1':
                data.append(Mob('1'))
            elif c == 'm':
                data.append(Mob('m'))
        return data

    def __str__(self):
        lines = []
        for y in xrange(self.height):
            lines.append('')
            for x in xrange(self.width):
                lines[-1] += self.data[self.idx(x, y)].symbol
        return '\n'.join(lines)

    def idx(self, x, y):
        if 0 > x or 0 > y or x >= self.width or y >= self.height:
            return None
        return x + y * self.width

    def get_mobs(self):
        mobs = []
        y = 0
        x = 0
        for element in self.data:
            if x >= self.width:
                x = 0
                y += 1
            if element.is_mob():
                mobs.append((element, x, y))
            x += 1
        return mobs

    def move(self, mob, new_pos):
        self.data[self.idx(mob[1], mob[2])] = Empty()
        self.data[self.idx(new_pos[0], new_pos[1])] = mob[0]

    def handle_action(self, mob_tuple, action):
        mob, x, y = mob_tuple
        if 'dx' in dir(action):
            self.move(mob_tuple, (x+action.dx, y+action.dy))

    def get_possible_pos(self, x, y):
        possible_pos = []
        idx = self.idx(x+1, y)
        if idx is not None and self.data[idx].symbol == ' ':
            possible_pos.append((x+1, y))
        idx = self.idx(x, y+1)
        if idx is not None and self.data[idx].symbol == ' ':
            possible_pos.append((x, y+1))
        idx = self.idx(x-1, y)
        if idx is not None and self.data[idx].symbol == ' ':
            possible_pos.append((x-1, y))
        idx = self.idx(x, y-1)
        if idx is not None and self.data[idx].symbol == ' ':
            possible_pos.append((x, y-1))
        return possible_pos

    def get_surroundings(self, x, y):
        pass

    def get_view(self, mob_tuple):
        mob, x, y = mob_tuple
        view = View()
        possible_pos = self.get_possible_pos(x, y)
        for pos in possible_pos:
            view.append(Direction(pos[0] - x, pos[1] - y))
        return view


class Game(object):
    def __init__(self, data, delay=1.):
        self.hold = Hold(data)
        self.delay = delay
        self.finished = False
        self.run()

    def run(self):
        while not self.finished:
            self.turn()
            print '\n'*1
            print self.hold
            time.sleep(self.delay)

    def turn(self):
        mobs = self.hold.get_mobs()
        for mob in mobs:
            view = self.hold.get_view(mob)
            action = mob[0].get_action(view)
            self.hold.handle_action(mob, action)
            #possible_pos = self.hold.get_possible_pos(mob[1], mob[2])
            #if len(possible_pos) > 0:
            #    self.hold.move(mob, random.choice(possible_pos))


def main():
    hold_name = sys.argv[-1]
    hold_file = open(hold_name, 'r')
    hold_data = hold_file.read()
    hold_file.close()
    game = Game(hold_data)

if __name__=='__main__':
    main()
