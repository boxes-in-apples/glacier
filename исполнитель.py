import importlib
import os
import sys

# --- 0. ПРЕДВАРИТЕЛЬНАЯ НАСТРОЙКА ПУТЕЙ ---
# Это позволяет импортировать модули из папок 'библиотеки' и 'модули'

script_dir = os.path.dirname(os.path.abspath(__file__))

LIBRARY_PATH = "библиотеки"
MODULE_PATH = "модули"

# Добавляем пути к системным путям (если еще не добавлены)
if script_dir not in sys.path:
    sys.path.append(script_dir)
if os.path.join(script_dir, LIBRARY_PATH) not in sys.path:
    sys.path.append(os.path.join(script_dir, LIBRARY_PATH))
if os.path.join(script_dir, MODULE_PATH) not in sys.path:
    sys.path.append(os.path.join(script_dir, MODULE_PATH))

# --- ИМПОРТ: Загружаем tokenize из отдельного модуля ---
try:
    from модули.базовые import tokenize 
except ImportError:
    print("КРИТИЧЕСКАЯ ОШИБКА: Не удалось импортировать 'tokenize' из 'модули.базовые'.")
    sys.exit(1)


# ======================================================================
# 1. ГЛОБАЛЬНЫЕ ДАННЫЕ
# ======================================================================

DEBUG_MODE = False
FILE_DEBUG_CONFIG = "file0"

COMMAND_MODULE_MAP = {}
LOADED_MODULES = {}
IMPORTED_FUNCTIONS = {}


# ======================================================================
# 2. ФУНКЦИИ ЯДРА
# ======================================================================

def initialize_debug_mode():
    """ 
    Читает 'file0' и устанавливает DEBUG_MODE. 
    """
    global DEBUG_MODE
    try:
        with open(FILE_DEBUG_CONFIG, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line == '1':
                DEBUG_MODE = True
                print(f"[{FILE_DEBUG_CONFIG}] Режим отладки (DEBUG MODE) включен.")
            elif first_line == '0':
                DEBUG_MODE = False
                print(f"[{FILE_DEBUG_CONFIG}] Режим отладки выключен (Тихий режим).")
            else:
                DEBUG_MODE = False
                print(f"[{FILE_DEBUG_CONFIG}] Неизвестное значение. Режим отладки выключен.")
    except (FileNotFoundError, Exception) as e:
        DEBUG_MODE = False
        print(f"[{FILE_DEBUG_CONFIG}] Ошибка: {e}. Режим отладки выключен.")

def load_commands_from_module(module_name):
    """ Сканирует и загружает команды из указанного модуля. """
    if module_name in LOADED_MODULES:
        if DEBUG_MODE:
            print(f"Модуль '{module_name}' уже загружен.")
        return True

    try:
        module = importlib.import_module(module_name)
        LOADED_MODULES[module_name] = module
        
        if DEBUG_MODE:
            print(f"Модуль '{module_name}' успешно загружен.")
        
        if hasattr(module, 'КОМАНДЫ_МОДУЛЯ'):
            commands = getattr(module, 'КОМАНДЫ_МОДУЛЯ')
            
            for command_key, func_name in commands.items():
                COMMAND_MODULE_MAP[command_key] = (module_name, func_name)
                if DEBUG_MODE:
                    print(f"  - Зарегистрирована команда: '{command_key}' ({func_name})")
            return True
            
        else:
            if DEBUG_MODE:
                 print(f"В модуле '{module_name}' не найден словарь КОМАНДЫ_МОДУЛЯ.")
            return False

    except ImportError as e:
        if DEBUG_MODE:
            print(f"ОШИБКА ИМПОРТА: Не удалось загрузить {module_name}. {e}")
        return False
    except Exception as e:
        if DEBUG_MODE:
            print(f"НЕИЗВЕСТНАЯ ОШИБКА при загрузке {module_name}: {e}")
        return False

def handle_import(args):
    """ Обработчик встроенной команды 'импорт module_name'. """
    global LIBRARY_PATH
    
    if not args:
        print("Ошибка: Команда 'импорт' требует имя модуля в качестве аргумента.")
        return
        
    short_module_name = args[0]
    full_module_name = f"{LIBRARY_PATH}.{short_module_name}" 
    
    if DEBUG_MODE:
        print(f"\n--- Выполняется динамическая загрузка модуля: {full_module_name} ---")
    
    if load_commands_from_module(full_module_name):
        if DEBUG_MODE:
            print("✅ Загрузка завершена успешно.")
    else:
        if DEBUG_MODE:
            print("❌ Загрузка завершилась с ошибкой.")

def get_function(command_name):
    """ Находит функцию по имени команды. """
    if command_name in IMPORTED_FUNCTIONS:
        return IMPORTED_FUNCTIONS[command_name]
    # ... (пропуск части кода для краткости, она остается прежней) ...
    if command_name not in COMMAND_MODULE_MAP:
        if DEBUG_MODE:
            print(f"Ошибка: Команда '{command_name}' не найдена в системе.")
        return None
        
    module_name, func_name = COMMAND_MODULE_MAP[command_name]    

    if module_name not in LOADED_MODULES:
        if DEBUG_MODE:
            print(f"Критическая ошибка: Модуль '{module_name}' для команды '{command_name}' не найден в кеше LOADED_MODULES.")
        return None
        
    module = LOADED_MODULES[module_name]

    try:
        func_object = getattr(module, func_name)
        if callable(func_object):
            IMPORTED_FUNCTIONS[command_name] = func_object
            return func_object
        else:
            if DEBUG_MODE:
                print(f"Ошибка: '{func_name}' не является функцией.")
            return None
    except AttributeError:
        if DEBUG_MODE:
            print(f"Ошибка: Функция '{func_name}' не найдена в модуле '{module_name}'.")
        return None

def execute_command(command_name, *args):
    """ Вызывает функцию по имени команды с заданными аргументами. """
    func = get_function(command_name)
    if func:
        if DEBUG_MODE:
            print(f"\n--- Выполняем команду: {command_name} ---")
        return func(args)    
    return None


# ======================================================================
# 3. ОБРАБОТЧИК МАТРИЦЫ КОМАНД
# ======================================================================

def process_matrix_commands(command_matrix):
    """
    Основная функция для выполнения последовательности команд из матрицы.
    """
    if not isinstance(command_matrix, list) or not command_matrix:
        if DEBUG_MODE:
            print("Ошибка: Матрица команд пуста или имеет неверный формат.")
        return

    results = []
    
    for command_list in command_matrix:
        if not command_list:
            continue

        command_name = command_list[0] 
        args = command_list[1:]   
        
        if DEBUG_MODE:
            print(f"\n[Обработчик Матрицы] Попытка выполнить: '{command_name}' с аргументами: {args}")

        result = execute_command(command_name, *args)
        results.append(result)
        
    return results


# ======================================================================
# 4. ФУНКЦИЯ ВХОДА (EXTERNAL API) И ЗАПУСК
# ======================================================================

def initialize_engine(preload_modules=None):
    """
    ⭐ ГЛАВНАЯ ФУНКЦИЯ ВХОДА. Инициализирует систему: 
    читает DEBUG_MODE, регистрирует встроенные команды и выполняет предварительную загрузку.
    """
    initialize_debug_mode() 

    # Регистрируем встроенную команду "импорт"
    # Это обязательно должно быть до предварительной загрузки!
    IMPORTED_FUNCTIONS["импорт"] = handle_import
    COMMAND_MODULE_MAP["импорт"] = ("Встроенный", "handle_import") 
    
    # --- НОВАЯ ЛОГИКА ПРЕДВАРИТЕЛЬНОЙ ЗАГРУЗКИ ---
    if preload_modules:
        if DEBUG_MODE:
            print(f"\n[ИНИЦИАЛИЗАЦИЯ] Начинается предварительная загрузка модулей: {preload_modules}")
        
        # Перебираем список модулей, которые нужно загрузить
        for module_name in preload_modules:
            # Вызываем handle_import. Она ожидает кортеж аргументов, 
            # поэтому передаем (module_name,)
            handle_import((module_name,)) 
        
        if DEBUG_MODE:
             print("[ИНИЦИАЛИЗАЦИЯ] Предварительная загрузка завершена.")
    # ---------------------------------------------

    if DEBUG_MODE:
        print("Система команд готова к работе.")
        print(f"Доступные команды: {list(COMMAND_MODULE_MAP.keys())}\n")
        

def run_demo():
    """ Запускает демонстрационный сценарий (используется только для прямого запуска). """
    raw_input_text = """
    импорт приветсвия
    приветсвовать Клиент
    импорт основные
    вывести Система готова к работе.
    """
    print("\n--- Демонстрация: Выполнение Матрицы Команд ---")
    
    # 1. Используем импортированный tokenize
    command_matrix = tokenize(raw_input_text, delimiter=' ')
    
    # 2. Вызываем главную функцию обработки
    process_matrix_commands(command_matrix)
    
    print("\n--- Выполнение Матрицы Команд Завершено ---")


if __name__ == "__main__":
    # Если файл запускается напрямую:
    initialize_engine()
    run_demo()
