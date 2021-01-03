"""
Advent of Code, Day 11: Seating System

https://adventofcode.com/2020/day/11
"""
from __future__ import annotations

from typing import List
import enum
import operator

class Values(enum.IntEnum):
    floor = 0
    empty = 1
    full = 2

    def __repr__(self):
        if self.value == Values.floor:
            return '.'
        if self.value == Values.empty:
            return 'L'
        if self.value == Values.full:
            return '#'

    @staticmethod
    def from_str(s: str):
        if s == '.':
            return Values.floor
        if s == 'L':
            return Values.empty
        if s == '#':
            return Values.full

class Part(enum.Enum):
    one = enum.auto()
    two = enum.auto()

Matrix = List[List[Values]]

class Board:

    _directions = [
        (1, 0), # East
        (1, 1), # Southeast
        (0, 1), # South
        (-1, 1), # Southwest
        (-1, 0), # West
        (-1, -1), # Northwest
        (0, -1), # North
        (1, -1) # NorthEast
    ]

    @classmethod
    def from_file(cls, input_path: str) -> Board:
        with open(input_path, 'rt') as f:
            return cls.from_str(f.read())

    @classmethod
    def from_str(cls, state: str) -> Board:
        """
        Create instance from string representation of board.
        Pads outline of board with floor values.
        """
        lines = [l for l in state.split('\n') if len(l) > 0]
        matrix = []
        width = len(lines[0]) + 2 # +2 for left/right padding
        matrix.append([Values.floor] * width)
        for line in lines:
            matrix.append([Values.floor] + [Values.from_str(s) for s in line] + [Values.floor])

        matrix.append([Values.floor] * width)

        return cls(matrix)

    def __init__(self, matrix: Matrix):
        self.matrix = matrix
        self.height = len(matrix)
        self.width = len(matrix[0])

    def __repr__(self):
        return '\n'.join([''.join(map(repr, line)) for line in self.matrix])

    def __eq__(self, other: Board) -> bool:
        return self.matrix == other.matrix

    @property
    def occupied(self) -> int:
        counter = 0
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                counter += self.matrix[row][col] == Values.full
        return counter

    def part_one(self) -> int:
        for _ in range(250): # timeout after 250 steps
            n = self._step(Part.one)
            if n == self:
                return n.occupied
            else:
                self = n
        raise RuntimeError('time out')

    def part_two(self, verbose: bool = False) -> int:
        if verbose:
            print(self)

        for _ in range(250): # timeout after 250 steps
            n = self._step(Part.two)
            if verbose:
                print('-----')
                print(n)

            if n == self:
                return n.occupied
            else:
                self = n
        raise RuntimeError('time out')


    def _step(self, part: Part) -> Board:
        new_matrix = []
        for h in range(self.height):
            new_matrix.append([Values.floor] * self.width)

        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if part == Part.one:
                    new_matrix[row][col] = self._convolve(row, col, self.matrix)
                elif part == Part.two:
                    new_matrix[row][col] = self._raycast(row, col, self.matrix)
                else:
                    raise ValueError

        return Board(new_matrix)

    @staticmethod
    def _convolve(row: int, col: int, m: Matrix) -> Values:
        """For part one"""
        if m[row][col] == Values.floor:
            return Values.floor

        sum_ = 0
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i == row and j == col:
                    continue
                if m[i][j] == Values.full:
                    sum_ += 1

        if sum_ >= 4:
            return Values.empty
        elif sum_ == 0:
            return Values.full
        else:
            return m[row][col]

    @classmethod
    def _raycast(cls, row: int, col: int, m: Matrix) -> Values:
        """For part two"""
        if m[row][col] == Values.floor:
            return Values.floor

        w = len(m[0])
        h = len(m)

        sum_ = 0
        for dx, dy in cls._directions:
            c = col + dx
            r = row + dy
            while True:
                if c < 0 or c >= w:
                    break
                if r < 0 or r >= h:
                    break

                v = m[r][c]
                if v == Values.full:
                    sum_ += 1
                    break
                elif v == Values.empty:
                    break
                else: # v == Values.floor:
                    c += dx
                    r += dy

        if sum_ >= 5:
            return Values.empty
        elif sum_ == 0:
            return Values.full
        else:
            return m[row][col]




if __name__ == '__main__':
    b_1 = Board.from_file('input')
    print('Part One:', b_1.part_one())
    b_2 = Board.from_file('input')
    print('Part Two:', b_2.part_two())
