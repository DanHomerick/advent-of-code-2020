"""
Advent of Coding 2020, Day 7: Handy Haversacks

https://adventofcode.com/2020/day/7
"""

from __future__ import annotations

import unittest

from pathlib import Path
from typing import Dict, Optional, Union
from warnings import warn

class TestHandyHaversacks(unittest.TestCase):

    # === TEST INPUT ===
    # light red bags contain 1 bright white bag, 2 muted yellow bags.
    # dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    # bright white bags contain 1 shiny gold bag.
    # muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    # shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    # dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    # vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    # faded blue bags contain no other bags.
    # dotted black bags contain no other bags.

    def test_parse_line(self):
        line = 'light red bags contain 1 bright white bag, 2 muted yellow bags.'
        handy = HandyHaversacks()
        handy._parse_line(line)

        self.assertTrue('light red' in handy.bags)
        self.assertTrue('bright white' in handy.bags)
        self.assertTrue('muted yellow' in handy.bags)

        light_red = handy.bags['light red']
        bright_white = handy.bags['bright white']
        muted_yellow = handy.bags['muted yellow']
        self.assertEqual(light_red._children, {bright_white: 1, muted_yellow: 2})

    def test_parse_lines(self):
        handy = HandyHaversacks()
        handy._parse_input('test_input_one')

        self.assertTrue('light red' in handy.bags)
        self.assertTrue('dotted black' in handy.bags)

        bright_white = handy.bags['bright white']
        shiny_gold = handy.bags['shiny gold']
        self.assertTrue(shiny_gold in bright_white._children)
        self.assertEqual(bright_white._children[shiny_gold], 1)

    def test_part_one(self):
        handy = HandyHaversacks()
        result = handy.part_one(Path('test_input_one'))
        self.assertEqual(result, 4)

    def test_part_two(self):
        handy = HandyHaversacks()
        result = handy.part_two('test_input_two')
        self.assertEqual(result, 126)


class TestBag(unittest.TestCase):
    def test_finalize(self):
        bags = [Bag('0'), Bag('1'), Bag('2')]
        bags[0].add(bags[1], 5)
        bags[1].add(bags[2], 3)

        self.assertFalse(bags[0].is_final)
        self.assertFalse(bags[1].is_final)
        self.assertFalse(bags[2].is_final)
        bags[0].finalize()
        self.assertTrue(bags[0].is_final)
        self.assertTrue(bags[1].is_final)
        self.assertTrue(bags[2].is_final)

        self.assertEqual(bags[0]._deep_children[bags[1]], 5)
        self.assertEqual(bags[0]._deep_children[bags[2]], 15) # 5 * 3


class Bag:

    def __init__(self, name: str):
        self.name: str = name
        self._children: Dict[Bag, int] = dict()

        self._deep_children: Dict[Bag, int] = dict()
        self._is_final: bool = False

    def __hash__(self):
        return hash(self.name)

    @property
    def is_final(self):
        return self._is_final

    def add(self, bag: Bag, count: int):
        if bag in self._children:
            warn(f'bag "{bag}" is already a child in {self.name}')

        self._children[bag] = count

    def finalize(self):
        if self._is_final:
            return

        for bag, count in self._children.items():
            self._deep_children[bag] = count

            if not bag.is_final:
                bag.finalize()

            for b, c in bag._deep_children.items():
                if b not in self._deep_children:
                    self._deep_children[b] = count * c
                else:
                    self._deep_children[b] += count * c

        self._is_final = True

    def deep_count(self, bag: Bag) -> Optional[int]:
        if not self._is_final:
            return None

        return self._deep_children[bag]

    def deep_count_all(self) -> Optional[int]:
        if not self._is_final:
            return None

        return sum(self._deep_children.values())

    def deep_contains(self, bag: Bag) -> Optional[int]:
        if not self._is_final:
            return None

        return bag in self._deep_children
    
    def count_children(self) -> int:
        if len(self._children) == 0:
            return 0
        
        return sum([(bag.count_children() + 1) * count for bag, count in self._children.items()])

class HandyHaversacks:

    def __init__(self):
        self.bags: Dict[str, Bag] = dict()

    def part_one(self, input_file: Union[Path, str]) -> int:
        if isinstance(input_file, str):
            input_file = Path(input_file)

        self._parse_input(input_file)
        self._finalize_all()

        shiny_gold = self.bags['shiny gold']
        return sum([bag.deep_contains(shiny_gold) for bag in self.bags.values()])

    def part_two(self, input_file: Union[Path, str]) -> int:
        if isinstance(input_file, str):
            input_file = Path(input_file)

        self._parse_input(input_file)
        self._finalize_all()

        shiny_gold = self.bags['shiny gold']
        return shiny_gold.count_children()
        
    def _parse_input(self, file_path: Path):
        with open(file_path) as input_file:
            lines = input_file.readlines()

        for line in lines:
            self._parse_line(line)

    def _parse_line(self, line: str):
        name = line[:line.find('bags')].strip()
        if name in self.bags:
            bag = self.bags[name]
        else:
            bag = Bag(name)
            self.bags[name] = bag

        contents_index = line.find('contain') + len('contain') + 1
        contents_list = line[contents_index:].split(',')
        # ex: contents_list = ['5 striped magenta bags', '3 plaid salmon bags.']
        # ex2: contents_list = ['no other bags.']

        for content_str in contents_list:
            parts = content_str.split()
            # ex: parts = ['5', 'striped', 'magenta', 'bags']
            # ex2: ['no', 'other', 'bags.']

            if parts[0] == 'no':
                break

            content_name = ' '.join(parts[1:3]) # ex: 'striped magenta'
            if content_name in self.bags:
                content_bag = self.bags[content_name]
            else:
                content_bag = Bag(content_name)
                self.bags[content_name] = content_bag

            bag.add(content_bag, int(parts[0]))

    def _finalize_all(self):
        for bag in self.bags.values():
            bag.finalize()


if __name__ == '__main__':
#    unittest.main()

    handy = HandyHaversacks()
#    print('Part One: ', handy.part_one('input'))
    print('Part Two: ', handy.part_two('input'))