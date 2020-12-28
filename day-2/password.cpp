#include "password.h"
#include "boost/algorithm/string.hpp"

#include <fstream>
#include <iostream>


using namespace std;
using namespace advent;

vector<Entry> PasswordVerifier::loadInputs(const string& path) {
    vector<Entry> entries;
    ifstream inputs(path);
    if (!inputs.is_open()) {
        cerr << "Failed to open file: " << path << endl;
        exit(1);
    }

    string line;
    Rule rule;
    while (getline(inputs, line)) {
        vector<string> parts;
        boost::split(parts, line, boost::is_any_of("- "));
        rule.value = parts[2][0];
        rule.low = stoi(parts[0]);
        rule.high = stoi(parts[1]);
        entries.emplace_back(rule, parts[3]);
    }
    return entries;

}

int PasswordVerifier::countValid(const vector<Entry>& entries, Method method) {
    int count = 0;
    if (method == PART_ONE) {
        for (const Entry& entry : entries) {
            if (isValidMethodOne(entry)) {
                ++count;
            }
        }
    } else if (method == PART_TWO) {
        for (const Entry& entry : entries) {
            if (isValidMethodTwo(entry)) {
                ++count;
            }
        }
    }
    return count;
}

bool PasswordVerifier::isValidMethodOne(const Entry& entry) {
    int count = 0;
    char value = entry.rule.value;
    for (auto iter = entry.password.begin(); iter != entry.password.end(); ++iter) {
        if (*iter == value) {
            ++count;
        }
    }
    return count >= entry.rule.low && count <= entry.rule.high;
}

bool PasswordVerifier::isValidMethodTwo(const Entry& entry) {
    int count = 0;
    char value = entry.rule.value;
    if (entry.rule.high > entry.password.size()) {
        cerr << "out of index: " << entry.password;
        return false;
    }

    bool matchLow = entry.password[entry.rule.low - 1] == value; // -1 since they're using 1-based indexing
    bool matchHigh = entry.password[entry.rule.high - 1] == value;
    return matchLow ^ matchHigh;
}

int main() {
    PasswordVerifier verifier;
    vector<Entry> entries = verifier.loadInputs("input");
    cout << verifier.countValid(entries, PART_TWO) << endl;
}