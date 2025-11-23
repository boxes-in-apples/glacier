#include <iostream>
#include <string>

int tokenize(const std::string & string);

int main() {
    std::cout << "Welcome to Glacier 0.1.1 C++ version.\nGlacier>>>";
    std::string command;
    std::getline(std::cin, command);

    tokenize(command);
    return 0;
}
