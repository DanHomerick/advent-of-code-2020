"""
Advent of Code, Day 12: Rain Risk

https://adventofcode.com/2020/day/12

I've been limiting myself to stuff found in the standard library, but in this
case using numpy would sure have made some basic math stuff a bit easier.

I'm somewhat curious if the ship 'draws' something during its travels in either
part one or part two, but not quite curious enough to code up a visualization
of it.
"""

import enum

from abc import ABC, abstractmethod
from typing import List, NamedTuple, Tuple

class Position(NamedTuple):
    x: int
    y: int

class Dir(enum.IntEnum):
    N = 270
    E = 0
    S = 90
    W = 180


class BaseShip(ABC):
    def __init__(self):
        self.pos: Position = Position(0, 0)
        self.heading: Dir = Dir.E

    def run(self, commands: List[str]) -> int:
        """
        Follow commands and return manhatten distance
        """
        for cmd in commands:
            self.command(cmd)

        return self.manhatten_distance()

    @abstractmethod
    def command(self, command: str):
        """Parse the command string, and follow the command."""
        pass

    def manhatten_distance(self) -> int:
        """
        Distance from starting position
        """
        return abs(self.pos.x) + abs(self.pos.y)

    def _parse(self, command: str) -> Tuple[str, int]:
        return (command[0], int(command[1:]))

    def _move(self, pos: Position, direction: Dir, distance: int) -> Position:
        """Move pos in a cardinal direction. Return new position."""
        if direction == Dir.N:
            return Position(pos.x, pos.y + distance)
        elif direction == Dir.E:
            return Position(pos.x + distance, pos.y)
        elif direction == Dir.S:
            return Position(pos.x, pos.y - distance)
        elif direction == Dir.W:
            return Position(pos.x - distance, pos.y)
        else:
            raise ValueError


class PartOneShip(BaseShip):
    def command(self, command: str):
        """Parse the command string, and follow the command."""
        cmd, value = self._parse(command)

        if cmd == 'F':
            self.pos = self._move(self.pos, self.heading, value)
        elif cmd == 'L':
            self.turn(-value)
        elif cmd == 'R':
            self.turn(value)
        else: # N, S, E, W
            self.pos = self._move(self.pos, Dir[cmd], value)

    def turn(self, deg: int):
        """
        Change heading without altering position. Positive values are
        clockwise. Only 90 degree increments are accepted.
        """
        self.heading = Dir((self.heading.value + deg) % 360)


class PartTwoShip(BaseShip):
    # Rotation matrices. Positive is counter-clockwise.
    rotations = {
        0: [[1, 0], [0, 1]],
        90: [[0, -1], [1, 0]],
        180: [[-1, 0], [0, -1]],
        270: [[0, 1], [-1, 0]]
    }

    def __init__(self):
        super().__init__()
        self.waypoint = Position(10, 1) # 10 units east and 1 unit north of ship

    def command(self, command: str):
        cmd, value = self._parse(command)

        if cmd == 'F':
            self.move_ship(value)
        elif cmd == 'R':
            self.rotate_waypoint(360 - value)
        elif cmd == 'L':
            self.rotate_waypoint(value)
        else: # N, S, E, W
            self.move_waypoint(Dir[cmd], value)

    def move_ship(self, value: int):
        self.pos = Position(self.pos.x + self.waypoint.x * value,
                            self.pos.y + self.waypoint.y * value)

    def move_waypoint(self, direction: Dir, distance: int):
        self.waypoint = self._move(self.waypoint, direction, distance)

    def rotate_waypoint(self, deg: int):    
        """Positive deg will do a counterclockwise (Left) rotation"""
        w0 = self.waypoint.x
        w1 = self.waypoint.y
        matrix = self.rotations[deg]
        self.waypoint = Position(w0 * matrix[0][0] + w1 * matrix[0][1],
                                 w0 * matrix[1][0] + w1 * matrix[1][1])


if __name__ == '__main__':
    with open('input', 'rt') as commands_file:
        commands = commands_file.readlines()

    p1ship = PartOneShip()
    print("Part One:", p1ship.run(commands))

    p2ship = PartTwoShip()
    print("Part Two:", p2ship.run(commands))
