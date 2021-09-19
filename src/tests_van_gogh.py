from unittest import TestCase

from van_gogh import VanGogh


class VanGoghTestCase(TestCase):
    def test_hex_grid_returns_hexagonal_grid(self):
        """
            __
         __/  \__
        /  \__/  \
        \__/  \__/
        /  \__/  \
        \__/  \__/
           \__/
        """

        vincent = VanGogh(grid_size=1)
        grid = vincent._hex_grid()
        expected_grid = [(-3.00, -1.73), (-2.50, -0.87), (-2.00, 0.00), (-1.50, 0.87), (-1.00, 1.73), (-2.00, -1.73),
                         (-1.50, -0.87), (-1.00, 0.00), (-0.50, 0.87), (0.00, 1.73), (-1.00, -1.73), (-0.50, -0.87),
                         (0.00, 0.00), (0.50, 0.87), (1.00, 1.73), (0.00, -1.73), (0.50, -0.87), (1.00, 0.00),
                         (1.50, 0.87), (2.00, 1.73), (1.00, -1.73), (1.50, -0.87), (2.00, 0.00), (2.50, 0.87)]
        for expected_point, point in zip(expected_grid, grid):
            self.assertAlmostEqual(expected_point[0], point[0], places=2)
            self.assertAlmostEqual(expected_point[1], point[1], places=2)

    def test_square_grid_returns_overlapping_square_grid(self):
        vincent = VanGogh(grid_size=1)
        grid = vincent._square_grid()
        grid.sort()  # The original grid is randomized, but we want to check the exact values, and hence sort it first
        expected_grid = [(-1.00, -1.00), (-1.00, -0.50), (-1.00, 0.00), (-1.00, 0.50), (-1.00, 1.00), (-0.50, -1.00),
                         (-0.50, -0.50), (-0.50, 0.00), (-0.50, 0.50), (-0.50, 1.00), (0.00, -1.00), (0.00, -0.50),
                         (0.00, 0.00), (0.00, 0.50), (0.00, 1.00), (0.50, -1.00), (0.50, -0.50), (0.50, 0.00),
                         (0.50, 0.50), (0.50, 1.00), (1.00, -1.00), (1.00, -0.50), (1.00, 0.00), (1.00, 0.50),
                         (1.00, 1.00)]
        for expected_point, point in zip(expected_grid, grid):
            self.assertAlmostEqual(expected_point[0], point[0], places=2)
            self.assertAlmostEqual(expected_point[1], point[1], places=2)
