#include <iostream>
#include <string>

std::string menu() {
    std::cout << "GLACIER 0.1.1\nДобро пожаловать!\n" << std::endl;
    while (true) {
        std::cout << "Glacier>";
        std::string command;
        std::getline(std::cin, command);
        return command;
    }
}
