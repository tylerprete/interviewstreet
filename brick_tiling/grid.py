import fileinput
from copy import deepcopy, copy

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

class grid(object):

    @classmethod
    def __from_list__(cls, lst):
        n = len(lst)
        m = len(lst[0])
        arr = []
        for i in xrange(n):
            arr.extend(lst[i])
        return grid(n, m, arr)

    def __init__(self, n, m, arr=None):
        self.n = n
        self.m = m
        arr_size = n * m
        self.arr = arr if arr else list(BLOCKED * arr_size)

    def index(self, x, y):
        return (x * self.m) + y

    def out_of_bounds(self, x, y):
        return (x < 0 or x >= self.n or y < 0 or y >= self.m)

    def get(self, x, y):
        if self.out_of_bounds(x, y): return BLOCKED
        i = self.index(x, y)
        return self.arr[i]

    def set(self, x, y, val):
        if self.out_of_bounds(x, y): return
        i = self.index(x, y)
        self.arr[i] = val

    def show(self):
        for i in xrange(self.n):
            base = i*self.n
            print self.arr[base:base+self.m]

    def copy(self):
        return grid(self.n, self.m, copy(self.arr))

    def apply_changes(self, changes):
        for (x, y, val) in changes:
            self.set(x, y, val)

    def apply_changes_with_undo(self, changes):
        undo = []
        for (x, y, val) in changes:
            undo.append((x, y, self.get(x, y)))
            self.set(x, y, val)
        return undo

def knob_index(thegrid, i, j, direction, flipped):
    if direction == UP or direction == DOWN:
        ix, jx = (i, j-1) if flipped else (i, j+1)
    else:
        ix, jx = (i-1, j) if flipped else (i+1, j)
    return ix, jx

def sort(a, b):
    return (a, b) if a <= b else (b, a)

def irange(x,y,z=1):
    return range(x,y+1,z)


def placement(agrid, i, j, direction, flipped):
    changes = []
    thegrid = agrid.copy()
    blocked = False
    endi, endj = i, j
    ki, kj = knob_index(thegrid, i, j, direction, flipped)
    if thegrid.get(ki, kj) in [BLOCKED, PLACEMENT]:
        return False, None
    changes.append((ki, kj, PLACEMENT))
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
            if thegrid.get(ix, jx) in [BLOCKED, PLACEMENT]:
                return False, None
            changes.append((ix, jx, PLACEMENT))
    return True, changes

def count_placements(thegrid):
    count = 0
    all_blocked = True
    for i in xrange(thegrid.n):
        for j in xrange(thegrid.m):
            if thegrid.get(i, j) in [OPEN, CHECKED]:
                all_blocked = False
                if thegrid.get(i, j) == OPEN:
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
    count = 0
    for p in placement_gen(thegrid, i, j):
        result, changes = placement(*p)
        if result:
            undo = thegrid.apply_changes_with_undo(changes)
            count += count_placements(thegrid)
            thegrid.apply_changes(undo)
    thegrid.set(i, j, CHECKED)
    return count


def check_all(thegrid, i, j):
    for p in placement_gen(thegrid, i, j):
        result, newgrid = placement(*p)
        print "placement(g, %d, %d, %d, %d) = %s" % (i, j, p[3], p[4], result)


def process_input():
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

if __name__ == '__main__':
    process_input()
