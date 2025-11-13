#include <iostream>
#include <string>


std::string menu() { // Изменить тип возвращаемого значения, так как теперь функция управляет циклом

    std::cout << "GLACIER 0.1.1\nДобро пожаловать!\n" << std::endl;

    std::cout << "Glacier>";

    std::string command;
    std::getline(std::cin, command);

    return command;

}
