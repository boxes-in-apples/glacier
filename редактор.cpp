#include <QApplication>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    window.setWindowTitle("Редактор");
    window.resize(800, 600);
    window.show();

    return app.exec();
}

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
