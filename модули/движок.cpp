//движок.cpp
#include <iostream> //Это чтобы выходы работали библиотека
#include <string> //А это чтобы строку вводить можно было


std::string menu() { //функция меню

    std::cout << "GLACIER 0.1.1\nДобро пожаловать!\n" << std::endl; //Первая линия в меню

    std::cout << "Glacier>"; //Ввод сюда будет

    std::string command; //создаем строку-переменную для команды ну это понятно
    std::getline(std::cin, command); //получаем целую линию в переменную команда

    return command; //возвращаем команду

}
