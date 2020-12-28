#include "code.h"
#include <iostream>
#include <fstream>

using namespace std;

unordered_set<int> Sum2020Solver::loadInput(const std::string& path) {
    unordered_set<int> values;
    ifstream s;
    s.open(path);
    if (!s.is_open()) {
        cout << "Failed to open file: " << path << endl;
        exit(1);
    }
    
    string line;
    while (getline(s, line)) {
        int value = stoi(line);
        values.insert(value);
    }

    return values;
}

int Sum2020Solver::solve1(const std::unordered_set<int>& values) {
    for (auto value : values) {
        int match = 2020 - value;
        if (values.find(match) != values.end()) {
            cout << "Solved: " << value << ", " << match << endl;
            return value * match;
        }
    }
    return -1;
}

int Sum2020Solver::solve2(const std::unordered_set<int>& values) {
    for (auto value1 : values) {
        for (auto value2 : values) {
            if (value1 == value2) {
                continue;
            }
            int remainder = 2020 - value1 - value2;
            if (remainder > 0) {
                if (values.find(remainder) != values.end()) {
                    cout << "Solved: " << value1 << ", " << value2 << ", " << remainder << endl;
                    return value1 * value2 * remainder;
                }
            }
        }
    }
    return -1;
}

int main(int argc, char** argv) {
    string filename;
    string problemNum("1");
    if (argc < 2) {
        filename = "input";
    } else {
        filename = argv[1];
    }

    if (argc < 3) {
        problemNum = "1";
    } else {
        problemNum = argv[2];
    }

    Sum2020Solver solver;
    unordered_set<int> inputs = solver.loadInput(filename);

    if (problemNum == "1") {
        cout << "Solver1: " << solver.solve1(inputs) << endl;
    } else if (problemNum == "2") {
        cout << "Solver2: " << solver.solve2(inputs) << endl;
    }
}

