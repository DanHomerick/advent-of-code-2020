import unittest

from collections import deque

from encoding import Encoding


class TestEncoding(unittest.TestCase):

    test_sequence = [
        35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219,
        299, 277, 309, 576
    ]

    test_sets = [
        set([35 + 20, 35 + 15, 35 + 25, 35 + 47]),
        set([20 + 15, 20 + 25, 20 + 47]),
        set([15 + 25, 15 + 47]),
        set([25 + 47])
    ]

    def test_parse_input(self):
        self.assertEqual(Encoding._parse_input('test_input'), self.test_sequence)

    def test_preprocess(self):
        result = Encoding._preprocess([35, 20, 15, 25, 47])
        self.assertEqual(len(result), 4)
        self.assertEqual(len(result[0]), 4)
        self.assertEqual(len(result[3]), 1)
        self.assertEqual(result[0], self.test_sets[0])

    def test_validate(self):
        test_deque = deque(self.test_sets)
        self.assertTrue(Encoding._validate(55, test_deque))
        self.assertFalse(Encoding._validate(1000, test_deque))
        self.assertTrue(Encoding._validate(25 + 47, test_deque))

    def test_update(self):
        test_deque = deque([set(s) for s in self.test_sets]) # copy to prevent modification
        Encoding._update(5, test_deque, self.test_sequence, 5)
        
        expected_0 = set([20 + 15, 20 + 25, 20 + 47, 20 + 40])
        expected_1 = set([15 + 25, 15 + 47, 15 + 40])
        expected_2 = set([25 + 47, 25 + 40])
        expected_3 = set([47 + 40])

        self.assertEqual(len(test_deque), 4)
        self.assertEqual(test_deque[0], expected_0)
        self.assertEqual(test_deque[1], expected_1)
        self.assertEqual(test_deque[2], expected_2)
        self.assertEqual(test_deque[3], expected_3)

    def test_sum_to_target(self):
        enc = Encoding()
        result = enc._sum_to_target(self.test_sequence, 127)
        expect = self.test_sequence[2:6]
        self.assertEqual(result, expect)

    def test_part_one(self):
        self.assertEqual(Encoding.part_one('test_input', 5), 127)

    def test_part_two(self):
        self.assertEqual(Encoding.part_two('test_input', 5, 127), 62)

if __name__ == '__main__':
    unittest.main()