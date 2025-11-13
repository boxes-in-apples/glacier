// базовые.cpp
#include <iostream>
#include <string>

void tokenize(const std::string& command) {
    // Теперь внутри функции 'command' нельзя изменить
    std::cout << command << " - но это заглушка вообще-то." << std::endl;
}
