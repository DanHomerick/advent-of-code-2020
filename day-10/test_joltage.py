import unittest

from joltage import Joltage

class TestJoltage(unittest.TestCase):
    small_input = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
    
    large_input = [
        28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11,
        1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3
    ]

    def test_part_one_small(self):
        jolt = Joltage(self.small_input)
        self.assertEqual(jolt.part_one(), 7 * 5) # solution from problem text

    def test_part_one_large(self):
        jolt = Joltage(self.large_input)
        self.assertEqual(jolt.part_one(), 22 * 10) # solution from problem text

    def test_part_two_small(self):
        jolt = Joltage(self.small_input)
        self.assertEqual(jolt.part_two(), 8)

    def test_part_two_large(self):
        jolt = Joltage(self.large_input)
        self.assertEqual(jolt.part_two(), 19208)

if __name__ == '__main__':
    unittest.main()