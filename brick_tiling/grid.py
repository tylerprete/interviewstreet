import fileinput

BLOCKED = '#'
OPEN = '.'
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
piece = 0

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

    def reverse_index(self, i):
        return (i / self.m, i % self.m)

    def open_square(self):
        for (i, v) in enumerate(self.arr):
            if v == OPEN:
                return self.reverse_index(i)
        return None

    def show(self):
        lines = []
        for i in xrange(self.n):
            base = i*self.m
            lines.append( ''.join(self.arr[base:base+self.m]) )
        return "\n".join(lines)

    def free_placements(self, coords):
        for (x, y) in coords:
            self.arr[self.index(x, y)] = OPEN

    def apply_placements(self, coords, val):
        for (x, y) in coords:
            self.arr[self.index(x, y)] = val

def display(x):
    return str(x) if x < 32 else chr(x)

def counter_clockwise_rotate(coords):
    return map(lambda (x, y): (-y, x), coords)

def clockwise_rotate(coords):
    return map(lambda (x, y): (y, -x), coords)

def all_clockwise_rotations(coords):
    rotations = []
    for i in xrange(4):
        rotations.append(coords)
        coords = clockwise_rotate(coords)
    return rotations

def rotations_from_head():
    coords = [(0,0), (1,0), (2,0), (2,1)]
    flipped_coords = [(0,0), (1,0), (2,0), (2,-1)]
    rotations = all_clockwise_rotations(coords)
    rotations.extend(all_clockwise_rotations(flipped_coords))
    return rotations

def rotations_from_mid():
    coords = [(-1,0), (0,0), (1,0), (1,1)]
    flipped_coords = [(-1,0), (0,0), (1,0), (1,-1)]
    rotations = all_clockwise_rotations(coords)
    rotations.extend(all_clockwise_rotations(flipped_coords))
    return rotations

def rotations_from_corner():
    coords = [(-2,0), (-1,0), (0,0), (0,1)]
    flipped_coords = [(-2,0), (-1,0), (0,0), (0,-1)]
    rotations = all_clockwise_rotations(coords)
    rotations.extend(all_clockwise_rotations(flipped_coords))
    return rotations

def rotations_from_knob():
    coords = [(-2,-1), (-1,-1), (0,-1), (0,0)]
    flipped_coords = [(-2,1), (-1,1), (0,1), (0,0)]
    rotations = all_clockwise_rotations(coords)
    rotations.extend(all_clockwise_rotations(flipped_coords))
    return rotations

def legal_placement(thegrid, coords):
    for (x, y) in coords:
        if thegrid.get(x, y) != OPEN:
            return False
    return True

def adjust_coords(i, j, coords):
    return [(x+i, y+j) for (x,y) in coords]

def legal_placements(thegrid, x, y, rotations):
    legal_placement_list = []
    for coords in rotations:
        adj_coords = adjust_coords(x, y, coords)
        if legal_placement(thegrid, adj_coords):
            legal_placement_list.append(adj_coords)
    return legal_placement_list

# Build all_rotations const
all_rotations = []
all_rotations.extend(rotations_from_head())
all_rotations.extend(rotations_from_mid())
all_rotations.extend(rotations_from_corner())
all_rotations.extend(rotations_from_knob())
ALL_ROTATIONS = tuple(all_rotations)

def placement_gen(thegrid, i, j):
    all_placements = legal_placements(thegrid, i, j, ALL_ROTATIONS)
    return all_placements

def count_placements(thegrid):
    sq = thegrid.open_square()
    if sq:
        count = placements(thegrid, sq[0], sq[1])
        return count
    return 1

def count_placements2(thegrid):
    for i in xrange(thegrid.n):
        for j in xrange(thegrid.m):
            if thegrid.get(i, j) == OPEN:
                count = placements(thegrid, i, j)
                return count
    #print thegrid.show()
    #print
    return 1

def placements(thegrid, i, j):
    count = 0
    global piece
    all_coords = placement_gen(thegrid, i, j)
    for coords in all_coords:
        #print "Making placement from (%d, %d)" % (i, j)
        #print thegrid.show()
        #print "Changes: %s" % changes
        thegrid.apply_placements(coords, str(piece % 10))
        #print "After making placement from (%d, %d)" % (i, j)
        #print thegrid.show()
        piece += 1
        count += count_placements(thegrid)
        piece -= 1
        thegrid.free_placements(coords)
        #print "After undo placement from (%d, %d)" % (i, j)
        #print thegrid.show()
    return count

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
