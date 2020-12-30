"""Qt оболочка для forget-me-not."""
import sys
from PyQt5 import QtWidgets
from PyQt5 import uic

from pathlib import Path

FORMS_FOLDER = "forms/"
MAIN_WINDOW_FORM = "f_main.ui"


class MainWindow(QtWidgets.QMainWindow):
    """Класс."""

    def __init__(self):
        """Конструктор класса."""
        super(MainWindow, self).__init__()
        self.application_folder = Path.cwd()
        uic.loadUi(self.application_folder / FORMS_FOLDER / MAIN_WINDOW_FORM, self)
        self.show()


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    application.exec_()
