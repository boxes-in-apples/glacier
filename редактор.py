import tkinter as tk
from tkinter import filedialog, messagebox
from модули.базовые import tokenize
from исполнитель import initialize_engine, process_matrix_commands

# Глобальная переменная для отслеживания текущего открытого файла
current_file_path = None

def new_file():
    """Создает новый, пустой файл."""
    global current_file_path
    text_area.delete("1.0", tk.END)  # Очищаем текстовую область
    current_file_path = None
    root.title("Простой Редактор - Новый файл")

def open_file():
    """Открывает существующий файл."""
    global current_file_path
    
    # Открываем диалоговое окно для выбора файла
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
    )
    
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            text_area.delete("1.0", tk.END)  # Очищаем и вставляем содержимое
            text_area.insert("1.0", content)
            current_file_path = file_path
            root.title(f"Простой Редактор - {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка открытия", f"Не удалось открыть файл:\n{e}")

def save_file():
    """Сохраняет содержимое в текущий файл или вызывает save_as."""
    global current_file_path
    
    if current_file_path:
        # Сохранение в уже открытый файл
        try:
            with open(current_file_path, 'w', encoding='utf-8') as file:
                content = text_area.get("1.0", tk.END + "-1c") # Берем весь текст кроме последнего символа новой строки
                file.write(content)
            root.title(f"Простой Редактор - {current_file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить файл:\n{e}")
    else:
        # Если файл новый, вызываем функцию "Сохранить как..."
        save_file_as()

def save_file_as():
    """Сохраняет содержимое в новый файл."""
    global current_file_path
    
    # Открываем диалоговое окно для выбора пути сохранения
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
    )
    
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                content = text_area.get("1.0", tk.END + "-1c")
                file.write(content)
            current_file_path = file_path
            root.title(f"Простой Редактор - {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить файл:\n{e}")

def run_file():
    # Мы добавляем полный блок try-except
    try:
        # 'r' означает режим чтения (read)
        with open(current_file_path, 'r', encoding='utf-8') as file:
            # Метод .read() считывает ВСЁ содержимое файла в одну строку
            содержимое_файла = file.read()

        # --- 1. Чтение и Инициализация ---
        # ВЕСЬ ЭТОТ КОД ТЕПЕРЬ С ПРАВИЛЬНЫМ ОТСТУПОМ ВНУТРИ run_file() и try
        initialize_engine()
        # Теперь команды из этих модулей (например, 'приветсвовать' и 'вывести')
        # уже зарегистрированы и готовы к работе.

        # --- 2. Получение и Выполнение Команд ---
        command = содержимое_файла
        tokens = tokenize(command)

        print("\n--- Выполнение команд ---")
        results = process_matrix_commands(tokens)

        print("\n--- Выполнение завершено ---")
        print(f"Результат: {results}")

    except FileNotFoundError:
        print("🛑 Ошибка: Файл 'основа.py' не найден. Проверьте путь и имя.")
    except Exception as e:
        print(f"❌ Произошла непредвиденная ошибка: {e}")


# --- Создание основного окна ---
def start():
    global root, text_area
    root = tk.Tk()
    text_area = tk.Text(root, wrap="word", font=("Consolas", 12))

    root.title("Простой Редактор - Новый файл")
    root.geometry("800x600")

    # --- Создание текстовой области ---
    text_area = tk.Text(root, wrap="word", font=("Consolas", 12))
    text_area.pack(expand=True, fill="both")

    # --- Создание главного меню ---
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Создание меню "Файл"
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Файл", menu=file_menu)

    # Добавление команд в меню "Файл"
    file_menu.add_command(label="Новый", command=new_file)
    file_menu.add_command(label="Открыть...", command=open_file)
    file_menu.add_separator()
    file_menu.add_command(label="Запустить", command=run_file)
    file_menu.add_separator()
    file_menu.add_command(label="Сохранить", command=save_file)
    file_menu.add_command(label="Сохранить как...", command=save_file_as)
    file_menu.add_separator()
    file_menu.add_command(label="Выход", command=root.quit)

    # Запуск основного цикла Tkinter
    root.mainloop()

