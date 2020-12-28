"""
Advent of Coding 2020, Day 6: Custom Customs

https://adventofcode.com/2020/day/6
"""

import unittest

from pathlib import Path
from typing import List

class TestCustoms(unittest.TestCase):

    forms = [
        'abc',
        'a\nb\nc\n',
        'ab\nac\n',
        'a\na\na\na\n',
        'b\n'
    ]

    sets = [
        set(['a', 'b', 'c']),
        set(['a', 'b', 'c']),
        set(['a', 'b', 'c']),
        set(['a']),
        set(['b'])
    ]

    def test_process_forms_one(self):
        result = Customs.process_forms_one(self.forms)
        self.assertEqual(result, self.sets)

    def test_sum_counts(self):
        expected = 3 + 3 + 3 + 1 + 1
        result = Customs.sum_counts(self.sets)
        self.assertEqual(result, expected)


class Customs:

    @staticmethod
    def load_inputs(file_path: Path) -> List[str]:
        with open(file_path, 'rt') as input_file:
            return input_file.read().split('\n\n')

    @staticmethod
    def process_forms_one(forms: List[str]) -> List[set]:
        sets = [set(form) for form in forms]
        for s in sets:
            if '\n' in s:
                s.remove('\n')
        return sets

    @staticmethod
    def process_forms_two(forms: List[str]) -> List[set]:
        all_sets = []
        for form in forms:
            form_sets = [set(line) for line in form.split()]
            acc = form_sets[0]
            for s in form_sets[1:]:
                acc.intersection_update(s)
            all_sets.append(acc)
            
        return all_sets

    @staticmethod
    def sum_counts(sets: List[set]):
        for s in sets:
            if '\n' in s:
                print(f's has newline: {s}')

        return sum(len(s) for s in sets)


if __name__ == '__main__':
#    unittest.main()

    print(Customs.sum_counts(Customs.process_forms_two(Customs.load_inputs('input'))))
