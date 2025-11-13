#include <QApplication>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    window.setWindowTitle("Моё первое окно на Qt");
    window.resize(400, 300);
    window.show();

    return app.exec();
}
