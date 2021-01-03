import unittest

from seating import Values as V
from seating import Board
from seating import Part

class TestSeating(unittest.TestCase):

    def test_from_file(self):
        board = Board.from_file('small_test_input_0')
        expected = [
            [V.floor, V.floor, V.floor, V.floor, V.floor],
            [V.floor, V.floor, V.full , V.floor, V.floor],
            [V.floor, V.floor, V.empty, V.empty, V.floor],
            [V.floor, V.full , V.floor, V.empty, V.floor],
            [V.floor, V.floor, V.floor, V.floor, V.floor]
        ]
        self.assertEqual(len(board.matrix), 5)
        self.assertEqual(len(board.matrix[0]), 5)
        self.assertListEqual(board.matrix, expected)

    def test_convolve_all_floor(self):
        m = [[V.floor, V.floor, V.floor]] * 3
        self.assertEqual(Board._convolve(1, 1, m), V.floor)

    def test_convolve_all_empty(self):
        m = [[V.empty, V.empty, V.empty]] * 3
        self.assertEqual(Board._convolve(1, 1, m), V.full)

    def test_convolve_all_full(self):
        m = [[V.full, V.full, V.full]] * 3
        self.assertEqual(Board._convolve(1, 1, m), V.empty)

    def test_convolve_input_2(self):
        b1 = Board.from_file('small_test_input_1')
        self.assertEqual(Board._convolve(2, 2, b1.matrix), V.empty)
        self.assertEqual(Board._convolve(2, 3, b1.matrix), V.empty)

    def test_step_part_one(self):
        b0 = Board.from_file('small_test_input_0')
        b1 = Board.from_file('small_test_input_1')
        b2 = Board.from_file('small_test_input_2')
        
        t1 = b0._step(Part.one)
        self.assertListEqual(t1.matrix, b1.matrix)

        t2 = t1._step(Part.one)
        self.assertListEqual(t2.matrix, b2.matrix)

    def test_dimensions(self):
        b = Board.from_file('input')
        self.assertEqual(b.width, 97 + 2)
        self.assertEqual(b.height, 93 + 2)

    def test_equality(self):
        a = Board.from_file('small_test_input_0')
        b = Board.from_file('small_test_input_0')
        self.assertTrue(a == b)

    def test_raycast(self):
        m = [
            [V.floor, V.floor, V.floor],
            [V.full,  V.full,  V.floor],
            [V.full,  V.full,  V.floor]
        ]
        self.assertEqual(Board._raycast(1, 1, m), V.full)


if __name__ == '__main__':
    unittest.main()