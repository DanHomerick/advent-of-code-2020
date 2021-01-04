import unittest
from unittest.mock import patch

from rain import PartOneShip, PartTwoShip, Position, Dir

class TestPartOne(unittest.TestCase):
    def test_command_forward(self):
        s = PartOneShip()
        self.assertEqual(s.pos, Position(0, 0))
        s.command('F10')
        self.assertEqual(s.pos, Position(10, 0))

        s.heading = Dir.N
        s.command('F20')
        self.assertEqual(s.pos, Position(10, 20))

    def test_command_turn(self):
        s = PartOneShip()
        self.assertEqual(s.heading, Dir.E)
        s.turn(-90)
        self.assertEqual(s.heading, Dir.N)
        s.turn(-270)
        self.assertEqual(s.heading, Dir.E)
        s.turn(270)
        self.assertEqual(s.heading, Dir.N)
        s.turn(270)
        self.assertEqual(s.heading, Dir.W)

class TestPartTwo(unittest.TestCase):
    def test_command_forward(self):
        s = PartTwoShip()
        self.assertEqual(s.pos, Position(0, 0))
        s.command('F10')
        self.assertEqual(s.pos, Position(100, 10))

    def test_command_rotate(self):
        s = PartTwoShip()
        self.assertEqual(s.waypoint, Position(10, 1))
        s.command('R90')
        self.assertEqual(s.waypoint, Position(1, -10))
        s.command('L180')
        self.assertEqual(s.waypoint, Position(-1, 10))
        s.command('R270')
        self.assertEqual(s.waypoint, Position(-10, -1))

    def test_command_move_waypoint(self):
        s = PartTwoShip()
        self.assertEqual(s.waypoint, Position(10, 1))
        s.command('N50')
        self.assertEqual(s.waypoint, Position(10, 51))
        s.command('E25')
        self.assertEqual(s.waypoint, Position(35, 51))

    def test_example(self):
        s = PartTwoShip()
        s.command('F10')
        self.assertEqual(s.pos, Position(100, 10))
        s.command('N3')
        self.assertEqual(s.waypoint, Position(10, 4))
        self.assertEqual(s.pos, Position(100, 10))
        s.command('F7')
        self.assertEqual(s.pos, Position(170, 38))
        self.assertEqual(s.waypoint, Position(10, 4))
        s.command('R90')
        self.assertEqual(s.waypoint, Position(4, -10))
        self.assertEqual(s.pos, Position(170, 38))
        s.command('F11')
        self.assertEqual(s.pos, Position(214, -72))
        self.assertEqual(s.waypoint, Position(4, -10))
        
        self.assertEqual(s.manhatten_distance(), 286)


if __name__ == '__main__':
    unittest.main()