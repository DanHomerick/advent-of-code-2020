"""
Advent of Code 2020, Day 9 - Encoding Error

https://adventofcode.com/2020/day/9
"""

from collections import deque
from typing import Deque, List, Set, Tuple

SetDeque = Deque[Set[int]]

class Encoding:
    @classmethod
    def part_one(cls, file_path: str, preamble_length: int = 25) -> int:
        sequence = cls._parse_input(file_path)
        set_deque = cls._preprocess(sequence[:preamble_length])
        for idx in range(preamble_length, len(sequence)):
            is_valid = cls._validate(sequence[idx], set_deque)
            if not is_valid:
                return sequence[idx]
            cls._update(idx, set_deque, sequence, preamble_length)

        raise RuntimeError

    @classmethod
    def part_two(cls, file_path: str, preamble_length: int, target: int) -> int:
        sequence = cls._parse_input(file_path)
        seq_slice = cls._sum_to_target(sequence, target)
        return min(seq_slice) + max(seq_slice)

    @staticmethod
    def _parse_input(file_path: str) -> List[int]:
        result = []
        with open(file_path, 'rt') as input_file:
            for word in input_file.read().split():
                result.append(int(word))
        return result

    @staticmethod
    def _preprocess(preamble: List[int]) -> SetDeque:
        results: SetDeque = deque(set() for _ in range(len(preamble) - 1))
        for i in range(0, len(preamble) - 1):
            for j in range(i+1, len(preamble)):
                results[i].add(preamble[i] + preamble[j])

        return results

    @staticmethod
    def _validate(x: int, set_deque: SetDeque) -> bool:
        for s in set_deque:
            if x in s:
                return True

        return False

    @staticmethod
    def _update(idx: int, set_deque: SetDeque, sequence: List[int], premable_length: int):
        """
        Modify the set_deque by discarding the oldest set, creating a new one,
        and adding new sums to all sets.
        """
        set_deque.popleft()
        set_deque.append(set())
        offset = 1
        for s in set_deque:
            seq_value = sequence[idx]
            s_value = sequence[idx - premable_length + offset]
            s.add(seq_value + s_value)
            offset += 1
    
    @staticmethod
    def _sum_to_target(sequence: List[int], target: int) -> List[int]:
        """
        Find interval in sequence that sums to target.
        
        Returns: 
            Slice of sequence containing the summation interval

        Trying to do this the simplest way that could work, with no regard for
        algorithmic effeciency.

        Each contiguous region has a starting point. We'll iterate over the
        sequence, where for each potential starting point we sum contiguous
        numbers until we either reach the target value or overshoot it. If we
        overshoot, move starting point to next element and try again.

        There's potential to reuse some calculations, but in this case we're
        just going to discard all work and start fresh.

        Raises:
            RuntimeError: if suitable range not found.
        """
        for i, x in enumerate(sequence):
            if x == target: # unlikely case where range is one element
                return sequence[i:i+1]

            sum_ = x
            for j, y in enumerate(sequence[i + 1:]):
                sum_ += y
                if sum_ == target:
                    end_idx = i + 1 + j + 1 
                    return sequence[i:end_idx]
                elif sum_ > target:
                    break
        
        raise RuntimeError

if __name__ == '__main__':
    encoding = Encoding()
    target = encoding.part_one('input')
    print('Part One:', target)

    min_max_sum = encoding.part_two('input', 25, target)
    print('Part Two:', min_max_sum)