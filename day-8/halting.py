"""
Advent of Code 2020, Day 8: Handheld Halting

https://adventofcode.com/2020/day/8
"""

import enum

from typing import List, NamedTuple, Tuple

class Ops(enum.Enum):
    acc = enum.auto()
    jmp = enum.auto()
    nop = enum.auto()


class Instruction:
    def __init__(self, op: Ops, value: int):
        self.op = op
        self.value = value
        self.executed = False


class State(NamedTuple):
    line: int
    accum: int


class Outcome(enum.Enum):
    terminated = enum.auto()
    looped = enum.auto()


class Halting:
    def __init__(self):
        pass

    def part_one(self, input_path: str) -> int:
        instructions = self._parse_input(input_path)

        state = State(line=0, accum=0)
        while True:
            instruction = instructions[state.line]
            new_state = self._step(state, instruction)

            if instructions[new_state.line].executed:
                print(f'Looped back to line {new_state.line}.')
                return state.accum
            else:
                state = new_state

    def part_two(self, input_path: str) -> int:
        instructions = self._parse_input(input_path)

        for idx, inst in enumerate(instructions):
            original_op = inst.op
            if inst.op == Ops.jmp:
                inst.op = Ops.nop
            elif inst.op == Ops.nop:
                inst.op = Ops.jmp
            else:
                continue

            # Try running with modified instruction
            (outcome, state) = self._run(instructions)
            if outcome == Outcome.terminated and state.line == len(instructions):
                print(f'Changed instruction on line {idx + 1}')
                return state.accum # We've fixed it!
            else:
                inst.op = original_op # Didn't work, change it back
        
        raise RuntimeError


    def _parse_input(self, input_path: str) -> List[Instruction]:
        with open(input_path, 'rt') as input_file:
            lines = input_file.readlines()

        instructions = []
        for line in lines:
            parts = line.split()
            op = Ops[parts[0]]
            value = int(parts[1])
            instructions.append(Instruction(op, value))

        return instructions

    def _step(self, state: State, instruction: Instruction) -> State:
        """Executes a single instruction and returns new machine state"""
        instruction.executed = True

        if instruction.op == Ops.acc:
            return State(line=state.line + 1, accum=state.accum + instruction.value)
        elif instruction.op == Ops.jmp:
            return State(line=state.line + instruction.value, accum=state.accum)
        elif instruction.op == Ops.nop:
            return State(line=state.line + 1, accum=state.accum)
        else:
            raise ValueError

    def _run(self, instructions: List[Instruction]) -> Tuple[Outcome, State]:
        for inst in instructions:
            inst.executed = False
        
        state = State(line=0, accum=0)
        program_length = len(instructions)
        outcome = Outcome.terminated
        while state.line < program_length:
            instruction = instructions[state.line]
            new_state = self._step(state, instruction)

            if new_state.line < program_length and instructions[new_state.line].executed:
                outcome = Outcome.looped
                break
            else:
                state = new_state

        return (outcome, state)


if __name__ == '__main__':
    halting = Halting()
    print("Part One:", halting.part_one('input'))
    print("Part Two:", halting.part_two('input'))
