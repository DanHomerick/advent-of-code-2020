"""
Advent of Code 2020, Day 5: Boarding Passes

https://adventofcode.com/2020/day/5
"""

from enum import Enum
from typing import List

import unittest

class Boarding:
    @staticmethod
    def load_input(path: str) -> List[str]:
        with open(path, 'rt') as input_file:
            return input_file.read().splitlines()

    @classmethod
    def calc_seat_id(cls, ticket: List[str]) -> int:
        row = cls._calc_row(ticket)
        col = cls._calc_column(ticket)
        return row * 8 + col

    @staticmethod
    def _calc_row(ticket: List[str]) -> int:
        lower = 0
        upper = 127
        inc = 64
        for c in ticket[:7]:
            if c == 'F':
                upper -= inc
            elif c == 'B':
                lower += inc
            else:
                print(f'unrecognized value: {c}')
            inc //= 2
        if lower != upper:
            print(f'Bad convergence: {lower}, {upper} for {ticket} on row')
            return -1
        
        return lower
        
    @staticmethod
    def _calc_column(ticket: List[str]) -> int:
        lower = 0
        upper = 7
        inc = 4
        for c in ticket[7:]:
            if c == 'L':
                upper -= inc
            elif c == 'R':
                lower += inc
            else:
                print(f'unrecognized value: {c}')
            inc //= 2
        if lower != upper:
            print(f'Bad convergence: {lower}, {upper} for {ticket} on column')
            return -1

        return lower

class TestBoarding(unittest.TestCase):

    def test_one(self):
        self.assertEqual(Boarding.calc_seat_id('FBFBBFFRLR'), 357)
    
    def test_two(self):
        self.assertEqual(Boarding.calc_seat_id('BFFFBBFRRR'), 567)

    def test_three(self):
        self.assertEqual(Boarding.calc_seat_id('FFFBBBFRRR'), 119)

    def test_four(self):
        self.assertEqual(Boarding.calc_seat_id('BBFFBBFRLL'), 820)


if __name__ == "__main__":
#    unittest.main()

    tickets = Boarding.load_input('input')

    # Part One:
    print("Highest id: ", max(Boarding.calc_seat_id(ticket) for ticket in tickets))

    # Part Two:
    ids = sorted([Boarding.calc_seat_id(ticket) for ticket in tickets])
    print(ids)
    expected = ids[0]
    for id in ids:
        if id != expected:
            print(f'Found it: {expected}')
            break
        expected += 1
