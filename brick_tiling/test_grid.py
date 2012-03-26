import unittest
from grid import grid, count_placements
from grid import OPEN, BLOCKED

class TestGrid(unittest.TestCase):

    def test_counts(self):
        a = grid(2, 4)
        a.set(0, 0, OPEN)
        a.set(0, 1, OPEN)
        a.set(0, 2, OPEN)
        a.set(1, 0, OPEN)
        self.assertEqual(count_placements(a), 1)

        b = grid(2, 4)
        for i in xrange(2):
            for j in xrange(4):
                b.set(i, j, OPEN)
        self.assertEqual(count_placements(b), 2)

        c = grid(3, 3)
        for i in xrange(3):
            for j in xrange(3):
                c.set(i, j, OPEN)
        c.set(1, 1, BLOCKED)
        self.assertEqual(count_placements(c), 4)

if __name__ == '__main__':
    unittest.main()
