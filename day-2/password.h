/*
Advent of Code 2020, Day 2 - Password Philosophy

https://adventofcode.com/2020/day/2
*/

#pragma once

#include <string>
#include <utility>
#include <vector>

namespace advent {

enum Method {
    PART_ONE,
    PART_TWO
};

struct Rule {
    char value;
    int low;
    int high;
};

struct Entry {
    Rule rule;
    std::string password;

    Entry(Rule rule, const std::string& password)
        : rule(rule)
        , password(password)
    {}
};

class PasswordVerifier {
public:
    std::vector<Entry> loadInputs(const std::string& path);
    int countValid(const std::vector<Entry>& entries, Method method);

private:
    bool isValidMethodOne(const Entry& entry);
    bool isValidMethodTwo(const Entry& entry);
};

}