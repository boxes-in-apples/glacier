#Библиотека "движок.py"
import os
import sys

# 1. Добавляем родительскую папку (..) в sys.path
# os.path.dirname(__file__) — это текущая папка (sub_folder)
# os.path.dirname(...) — это родительская папка (parent_folder)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 2. Теперь можно импортировать!

import редактор

parent_folder = "Проекты"

def handle_noviy(arguments):
    full_path = os.path.join(parent_folder, ' '.join(arguments))
    os.makedirs(full_path, exist_ok=True)
    print(f"Проект создан {full_path}!")

def handle_otkryt(arguments):
    редактор.start()
    print(f"Открыли проект {full_path}!")

КОМАНДЫ_МОДУЛЯ = {
    "новый": "handle_noviy",
    "открыть": "handle_otkryt"
}

ИНФОРМАЦИЯ_МОДУЛЯ = {
    "название": "движок",
    "версия": "0.1"
}
