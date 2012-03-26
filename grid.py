from copy import deepcopy
import logging
#from pydbgr.api import debug

logging.basicConfig(level = logging.DEBUG)

BLOCKED = '#'
OPEN = '.'
CHECKED = '*'
PLACEMENT = '@'
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
NORMAL = False
FLIPPED = True

"""
UP and not FLIPPED:
    *
    *
    **
"""

class gridrow(list):

    def __getitem__(self, i):
        if i < 0: return BLOCKED
        try:
            return super(gridrow, self).__getitem__(i)
        except IndexError:
            return BLOCKED


class grid(gridrow):

    @classmethod
    def __from_list__(cls, lst):
        n = len(lst)
        m = len(lst[0])
        g = grid(n, m)
        for i in xrange(n):
            g[i] = gridrow(lst[i])
        return g

    def __init__(self, n, m):
        self.n = n
        self.m = m
        for i in range(n):
            row = BLOCKED * m
            self.append(gridrow(row))

    def __getitem__(self, i):
        if i < 0: return gridrow(BLOCKED * self.m)
        try:
            return super(gridrow, self).__getitem__(i)
        except IndexError:
            return gridrow(BLOCKED * self.m)

    def show(self):
        for line in self:
            print line

def knob_index(thegrid, i, j, direction, flipped):
    if direction == UP or direction == DOWN:
        ix, jx = (i, j-1) if flipped else (i, j+1)
    else:
        ix, jx = (i-1, j) if flipped else (i+1, j)
    return ix, jx

def get_knob(thegrid, i, j, direction, flipped):
    if direction == UP or direction == DOWN:
        knob = thegrid[i][j-1] if flipped else thegrid[i][j+1]
    else:
        knob = thegrid[i-1][j] if flipped else thegrid[i+1][j]
    return knob

def sort(a, b):
    return (a, b) if a <= b else (b, a)

def irange(x,y,z=1):
    return range(x,y+1,z)

def placement(agrid, i, j, direction, flipped):
    #logging.debug("Call to placement: %d %d %d %d", i, j, direction, flipped)
    thegrid = deepcopy(agrid)
    blocked = False
    endi, endj = i, j
    ki, kj = knob_index(thegrid, i, j, direction, flipped)
    if thegrid[ki][kj] in [BLOCKED, PLACEMENT]:
        return False, None
    thegrid[ki][kj] = PLACEMENT
    if direction == UP:
        endi = i - 2
    elif direction == RIGHT:
        endj = j + 2
    elif direction == DOWN:
        endi = i + 2
    elif direction == LEFT:
        endj = j - 2
    for ix in irange(*sort(i, endi)):
        for jx in irange(*sort(j, endj)):
            if thegrid[ix][jx] in [BLOCKED, PLACEMENT]:
                return False, None
            thegrid[ix][jx] = PLACEMENT
    return True, thegrid

# This needs work...
# We need to count/make placements,
# but we also need to avoid counting duplicate boards...
def count_placements(thegrid):
    #thegrid.show()
    #print
    count = 0
    all_blocked = True
    for i in xrange(len(thegrid)):
        for j in xrange(len(thegrid[0])):
            if thegrid[i][j] in [OPEN, CHECKED]:
                all_blocked = False
                if thegrid[i][j] == OPEN:
                    count += placements(thegrid, i, j)
    return 1 if all_blocked else count

def placement_gen(thegrid, i, j):
    directions = [UP, DOWN, LEFT, RIGHT]
    flipped = [NORMAL, FLIPPED]
    count = 0
    for d in directions:
        for f in flipped:
            yield (thegrid, i, j, d, f)

def placements(thegrid, i, j):
    #print "Call to placements: %d %d" % (i, j)
    count = 0
    for p in placement_gen(thegrid, i, j):
        result, newgrid = placement(*p)
        if result:
            #print "Placement made: Calling count_placements from (%d, %d)" % (i, j)
            #print "Old board"
            #thegrid.show()
            #print "New board"
            #newgrid.show()
            #print
            count += count_placements(newgrid)
    thegrid[i][j] = CHECKED
    return count


def check_all(thegrid, i, j):
    for p in placement_gen(thegrid, i, j):
        result, newgrid = placement(*p)
        print "placement(g, %d, %d, %d, %d) = %s" % (i, j, p[3], p[4], result)


def test_cases():
    a = grid(2, 4)
    #a.show()
    a[0][0] = OPEN
    a[0][1] = OPEN
    a[0][2] = OPEN
    a[1][0] = OPEN
    a.show()
    #check_all(a, 0, 0)
    print "Placements: %d" % count_placements(a)
    b = grid(2, 4)
    #b.show()
    for i in xrange(2):
        for j in xrange(4):
            b[i][j] = OPEN
    b.show()
    #check_all(b, 0, 0)
    print "Placements: %d" % count_placements(b)
    c = grid(3, 3)
    for i in xrange(3):
        for j in xrange(3):
            c[i][j] = OPEN
    c[1][1] = BLOCKED
    c.show()
    print "Placements: %d" % count_placements(c)

import fileinput

def read_board():
    pass

if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.rstrip())
    boards = int(lines[0])
    line = 1
    for board in xrange(boards):
        n, m = map(int, lines[line].split())
        line += 1
        theboard = lines[line:line+n]
        thegrid = grid.__from_list__(theboard)
        print count_placements(thegrid) % 1000000007
        line = line+n
