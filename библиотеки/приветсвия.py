#Библиотека "приветсвия.py"

def handle_privetsvovat(arguments):
    name = arguments[0] if arguments else "Гость"
    print(f"Салам, {name}!")
    
КОМАНДЫ_МОДУЛЯ = {
    "приветсвовать": "handle_privetsvovat"
}

ИНФОРМАЦИЯ_МОДУЛЯ = {
    "Версия": "0.1"
}
