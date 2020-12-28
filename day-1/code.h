/*
Advent of Code 2020, Day 1: Report Repair

https://adventofcode.com/2020/day/1
*/

#include <unordered_set>

class Sum2020Solver {
public:
    std::unordered_set<int> loadInput(const std::string& filepath);
    int solve1(const std::unordered_set<int>& values);
    int solve2(const std::unordered_set<int>& values);
private:

};