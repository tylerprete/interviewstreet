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

    def open_squares(self):
        for (i, v) in enumerate(self.arr):
            if v == OPEN:
                yield self.reverse_index(i)

    def open_squares_count(self):
        count = 0
        for v in self.arr:
            if v == OPEN:
                count += 1
        return count

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
    #return map(lambda (x, y): (x+i, y+j), coords)
    return [(x+i, y+j) for (x,y) in coords]

def legal_placements(thegrid, x, y, rotations):
    for coords in rotations:
        adj_coords = []
        continue_outer_loop = False
        for (i, j) in coords:
            a = x+i; b = y+j
            if thegrid.get(a, b) != OPEN:
                continue_outer_loop = True
                break
            else:
                adj_coords.append((a, b))
        if continue_outer_loop:
            continue
        yield adj_coords

def nearby_squares(thegrid, coords):
    pass


def any_legal_placements(thegrid, x, y, rotations):
    for p in legal_placements(thegrid, x, y, rotations):
        return True
    else:
        return False

def check_board(thegrid, rotations):
    for (x, y) in thegrid.open_squares():
        if not any_legal_placements(thegrid, x, y, rotations):
            return False
    return True


# Build all_rotations const
all_rotations = []
all_rotations.extend(rotations_from_head())
all_rotations.extend(rotations_from_mid())
all_rotations.extend(rotations_from_corner())
all_rotations.extend(rotations_from_knob())
ALL_ROTATIONS = tuple(all_rotations)

placement_calls = 0
def placements(thegrid, i, j):
    global placement_calls
    placement_calls += 1
    count = 0
    global piece
    all_coords = legal_placements(thegrid, i, j, ALL_ROTATIONS)
    for coords in all_coords:
        #print "Making placement from (%d, %d)" % (i, j)
        #print thegrid.show()
        #print "Changes: %s" % changes
        thegrid.apply_placements(coords, str(piece % 10))
        #print "After making placement from (%d, %d)" % (i, j)
        #print thegrid.show()
        piece += 1
        sq = thegrid.open_square()
        count += placements(thegrid, *sq) if sq else 1
        piece -= 1
        thegrid.free_placements(coords)
        #print "After undo placement from (%d, %d)" % (i, j)
        #print thegrid.show()
    return count

def process_input():
    global placement_calls
    lines = []
    for line in fileinput.input():
        lines.append(line.rstrip())
    boards = int(lines[0])
    line = 1
    for board in xrange(boards):
        placement_calls = 0
        n, m = map(int, lines[line].split())
        line += 1
        theboard = lines[line:line+n]
        thegrid = grid.__from_list__(theboard)
        if thegrid.open_squares_count() % 4 == 0:
            sq = thegrid.open_square()
            print placements(thegrid, *sq) % 1000000007 if sq else 1
            #print "Placement calls: %d" % placement_calls
        else:
            print "0"

        line = line+n

if __name__ == '__main__':
    process_input()
