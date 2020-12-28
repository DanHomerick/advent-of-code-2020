"""
Advent of Code 2020, Day 4 - Passport Processing

https://adventofcode.com/2020/day/4


A valid passport contains the following fields:
    byr (Birth Year)
    iyr (Issue Year)
    eyr (Expiration Year)
    hgt (Height)
    hcl (Hair Color)
    ecl (Eye Color)
    pid (Passport ID)
    cid (Country ID)

For Part 1, we want to count passports that are missing the cid field as valid.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

import re

class Passport:
    """
    Holds passport values (as strings), and does validity check.
    """

    valid_hair_colors = set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])

    def __init__(self):
        self.byr = None
        self.iyr = None
        self.eyr = None
        self.hgt = None
        self.hcl = None
        self.ecl = None
        self.pid = None
        self.cid = None

    def deserialize(self, data: str) -> Passport:
        for pair in data.split():
            k, v = pair.split(":")
            self.__dict__[k] = v

        return self

    def is_valid(self, verbose: bool = False) -> bool:
        all_present = self.byr is not None \
            and self.iyr is not None \
            and self.eyr is not None \
            and self.hgt is not None \
            and self.hcl is not None \
            and self.ecl is not None \
            and self.pid is not None
            # cid is allowed to be None in first part of challenge

        if not all_present:
            if verbose:
                print("Missing field")
            return False

        # validate individual fields
        try:
            # birth year
            byr = int(self.byr)
            if not 1920 <= byr <= 2002:
                if verbose:
                    print('invalid byr: ', byr)
                return False

            # issue year
            iyr = int(self.iyr)
            if not 2010 <= iyr <= 2020:
                if verbose:
                    print('invalid iyr: ', iyr)
                return False

            # expiration year
            eyr = int(self.eyr)
            if not 2020 <= eyr <= 2030:
                if verbose:
                    print('invalid eyr: ', eyr)
                return False

            # height
            hgt_unit = self.hgt[-2:]
            hgt_value = int(self.hgt[0:-2])
            if hgt_unit == "cm":
                if not 150 <= hgt_value <= 193:
                    if verbose:
                        print('out of range cm height: ', hgt_value)
                    return False
            elif hgt_unit == "in":
                if not 59 <= hgt_value <= 76:
                    if verbose:
                        print('out of range inch height: ', hgt_value)
                    return False
            else:
                if verbose:
                    print('invalid hgt unit: ', hgt_unit)
                return False

            # hair color
            if re.fullmatch('#[0-9|a-f]{6}', self.hcl) is None:
                if verbose:
                    print('invalid hair color: ', self.hcl)
                return False

            # eye color
            if self.ecl not in Passport.valid_hair_colors:
                if verbose:
                    print('invalid eye color: ', self.ecl)
                return False

            # passport id
            if re.fullmatch('[0-9]{9}', self.pid) is None:
                if verbose:
                    print('invalid passport id: ', self.pid)
                return False

        except:
            if verbose:
                print('uncategorized fail')
            return False

        return True


class PassportLoader:
    """
    Loads passports from file, and deserializes into Passport objects
    """

    @staticmethod
    def load_input(path: Path) -> List[Passport]:
        """
        Splits input file into strings containing passport info, one passport per string.
        """

        passports = []
        with open(path, 'rt') as input_file:
            for data in input_file.read().split('\n\n'):
                passports.append(Passport().deserialize(data))

        return passports



if __name__ == '__main__':
    loader = PassportLoader()
    passports = loader.load_input(Path('input'))

    print("# Valid: ", sum(p.is_valid() for p in passports))
