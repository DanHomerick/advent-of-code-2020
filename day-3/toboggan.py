"""
Advent of Code 2020, Day 3 - Toboggan Trajectory

https://adventofcode.com/2020/day/3
"""

from functools import reduce
from pathlib import Path
from typing import List

import operator

class Toboggan:
    """
    Solves the advent of code, day 3 challenge
    """

    @staticmethod
    def load_input(filename: Path) -> List[str]:
        """
        Reads input file and returns list of lines.
        """
        with open(filename, 'rt') as input_file:
            return input_file.read().splitlines()

    @staticmethod
    def count_trees(rows: List[str], slope_x: int, slope_y: int) -> int:
        """
        Counts the number of trees encountered with given slope.
        """
        x = 0
        y = 0
        trees = 0
        row_length = len(rows[0])
        while y < len(rows):
            if rows[y][x % row_length] == '#':
                trees += 1

            x += slope_x
            y += slope_y

        return trees


if __name__ == "__main__":
    t = Toboggan()
    rows = t.load_input(Path('input'))

    tree_counts = [t.count_trees(rows, x, y) for x, y in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]]

    print(tree_counts)
    print(reduce(operator.mul, tree_counts))
