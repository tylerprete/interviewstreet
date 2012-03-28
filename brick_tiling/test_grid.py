import unittest
from grid import grid, count_placements
from grid import OPEN, BLOCKED
from grid import placements_from_head
from grid import clockwise_rotate, counter_clockwise_rotate

class TestGrid(unittest.TestCase):

    def test_counts(self):
        a = grid(2, 4)
        a.set(0, 0, OPEN)
        a.set(0, 1, OPEN)
        a.set(0, 2, OPEN)
        a.set(1, 0, OPEN)
        self.assertEqual(count_placements(a), 1)

        b = grid(2, 4, list(OPEN * 8))
        self.assertEqual(count_placements(b), 2)

        c = grid(3, 3, list(OPEN * 9))
        c.set(1, 1, BLOCKED)
        self.assertEqual(count_placements(c), 4)

    def test_clockwise_rotate(self):
        coords = [(0,0), (1,0), (2,0), (2,1)]
        rotated_coords = clockwise_rotate(coords)
        self.assertEqual(rotated_coords, [(0,0), (0,-1), (0,-2), (1,-2)])
        rotated_coords = clockwise_rotate(rotated_coords)
        self.assertEqual(rotated_coords, [(0,0), (-1,0), (-2,0), (-2,-1)])
        rotated_coords = clockwise_rotate(rotated_coords)
        self.assertEqual(rotated_coords, [(0,0), (0,1), (0,2), (-1,2)])

    def test_counter_clockwise_rotate(self):
        coords = [(0,0), (1,0), (2,0), (2,1)]
        rotated_coords = counter_clockwise_rotate(coords)
        self.assertEqual(rotated_coords, [(0,0), (0,1), (0,2), (-1,2)])
        rotated_coords = counter_clockwise_rotate(rotated_coords)
        self.assertEqual(rotated_coords, [(0,0), (-1,0), (-2,0), (-2,-1)])
        rotated_coords = counter_clockwise_rotate(rotated_coords)
        self.assertEqual(rotated_coords, [(0,0), (0,-1), (0,-2), (1,-2)])

    def test_placements_from_head(self):
        a = grid(4, 4, list(OPEN * 16))
        rotations = placements_from_head(a, 0, 0)
        self.assertEqual(rotations,
                [[(0, 0), (1, 0), (2, 0), (2, 1)], [(0, 0), (0, 1), (0, 2), (1, 2)]])

if __name__ == '__main__':
    unittest.main()
