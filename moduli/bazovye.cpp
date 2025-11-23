#include <string>
#include <iostream>
#include "h/bazovye.h"
#include <vector>
#include <sstream>

int tokenize(const std::string& command) {
    std::stringstream ss(command);
    std::string token;
    std::vector<std::string> tokens;

    while (ss >> token) {
        tokens.push_back(token);
    }
    for (const std::string& element : tokens) {
        std::cout << element << "\n";
    }
    std::cout << std::endl;
    return 0;
}
