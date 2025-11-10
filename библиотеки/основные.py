#Библиотека "основные.py"

def handle_vyvesti(arguments):
    output = " ".join(arguments)
    print(output)
    
КОМАНДЫ_МОДУЛЯ = {
    "вывести": "handle_vyvesti"
}

ИНФОРМАЦИЯ_МОДУЛЯ = {
    "название": "основные",
    "версия": "0.1"
}
