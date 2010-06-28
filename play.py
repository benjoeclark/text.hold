#!/usr/bin/env python

import sys
import time
import random


class Mob(object):
    def __init__(self, symbol):
        self.symbol = symbol

    def is_mob(self):
        return True

class Static(object):
    def is_mob(self):
        return False


class Wall(Static):
    def __init__(self):
        self.symbol = '#'


class Empty(Static):
    def __init__(self):
        self.symbol = ' '


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

    def __repr__(self):
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


class Game(object):
    def __init__(self, data, delay=1.):
        self.hold = Hold(data)
        self.delay = delay
        self.finished = False
        self.run()

    def run(self):
        while not self.finished:
            self.turn()
            print '\n'*100
            print self.hold
            time.sleep(self.delay)

    def turn(self):
        mobs = self.hold.get_mobs()
        for mob in mobs:
            possible_pos = self.hold.get_possible_pos(mob[1], mob[2])
            if len(possible_pos) > 0:
                self.hold.move(mob, random.choice(possible_pos))


def main():
    hold_name = sys.argv[-1]
    hold_file = open(hold_name, 'r')
    hold_data = hold_file.read()
    hold_file.close()
    game = Game(hold_data)

if __name__=='__main__':
    main()
