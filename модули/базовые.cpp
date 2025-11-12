#include <string>
#include <vector>
#include <sstream>
#include <algorithm>

std::vector<std::vector<std::string>> tokenize(const std::string& multiline_text, const std::string& delimiter = " ") {
    /*
    Преобразует многострочный текст в матрицу (вектор векторов строк),
    которая может быть использована как команды.
    */
    std::vector<std::vector<std::string>> matrix;
    std::istringstream stream(multiline_text);
    std::string line;

    while (std::getline(stream, line)) {
        // Пропускаем пустые строки
        std::string trimmed_line = line;
        trimmed_line.erase(trimmed_line.begin(), std::find_if(trimmed_line.begin(), trimmed_line.end(), [](unsigned char ch) {
            return !std::isspace(ch);
        }));
        trimmed_line.erase(std::find_if(trimmed_line.rbegin(), trimmed_line.rend(), [](unsigned char ch) {
            return !std::isspace(ch);
        }).base(), trimmed_line.end());

        if (trimmed_line.empty()) {
            continue;
        }

        std::vector<std::string> elements;
        if (delimiter == " ") {
            std::istringstream line_stream(trimmed_line);
            std::string word;
            while (line_stream >> word) {
                elements.push_back(word);
            }
        } else {
            size_t start = 0;
            size_t end = trimmed_line.find(delimiter);
            while (end != std::string::npos) {
                elements.push_back(trimmed_line.substr(start, end - start));
                start = end + delimiter.length();
                end = trimmed_line.find(delimiter, start);
            }
            elements.push_back(trimmed_line.substr(start));
        }

        if (!elements.empty()) {
            matrix.push_back(elements);
        }
    }

    return matrix;
}
