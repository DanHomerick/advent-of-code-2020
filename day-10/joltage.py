"""
Advent of Coding 2020, Day 10 - Adapter Array

https://adventofcode.com/2020/day/10
"""

from typing import List

class Joltage:

    def __init__(self, adapters: List[int]):
        adapters.sort()

        # include source, rated as 0 jolts, and device, rated as 3 greater than max adapter
        self.adapters = [0] + adapters + [adapters[-1] + 3]

    def part_one(self) -> int:
        """        
        Find a chain that uses all of your adapters to connect the charging
        outlet to your device's built-in adapter and count the joltage
        differences between the charging outlet, the adapters, and your device.
        
        Return the number of 1-jolt differences multiplied by the number
        of 3-jolt differences.
        """
        # Build histogram of joltage differences
        differences = [0, 0, 0, 0]        
        for n, m in zip(self.adapters[:-1], self.adapters[1:]):
            differences[m-n] += 1

        return differences[1] * differences[3]

    def part_two(self) -> int:
        d = {0:1}
        for i in self.adapters[1:]:
            d[i] = d.get(i-1, 0) + d.get(i-2, 0) + d.get(i-3, 0)
        return d[self.adapters[-1]]
        

if __name__ == '__main__':
    with open('input', 'rt') as input_file:
        adapters = list(map(int, input_file.readlines()))

    joltage = Joltage(adapters)
    print('Part One:', joltage.part_one())
    print('Part Two:', joltage.part_two())