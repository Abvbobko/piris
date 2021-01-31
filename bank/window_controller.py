import bank.constants as const

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QFrame
from PyQt5.QtCore import Qt

import sys


class MainWindow(QMainWindow):
    def __init__(self, width, height, title=""):
        super().__init__()

        self.resize(width, height)
        self.setWindowTitle(title)
        self.__init_items()
        # self.setStyleSheet("background-color: black;")

        # set projection label and parameters
        # self.projection_type_label = QLabel("o", self)
        # self.projection_type_label.setMargin(5)
        # self.projection_type_label.setAttribute(Qt.WA_TranslucentBackground)

    def __init_items(self):
        # fields = ["Фамилия:", "Имя:", "Отчество:", "Дата рождения"]
        self.surname_label = QLabel("Фамилия:", self)
        self.surname_label.move(5, 0)
        self.surname_edit = QLineEdit(self)
        self.surname_label.setFrameShape(QFrame.Panel)
        width, height = self.__get_label_text_pixel_size(self.surname_label)
        self.surname_edit.move(5 + width + 5, 0)

        self.name_label = QLabel("Имя:", self)
        self.name_label.move(5, self.surname_edit.height())
        self.name_edit = QLineEdit(self)
        self.name_label.setFrameShape(QFrame.Panel)
        width, height = self.__get_label_text_pixel_size(self.name_label)
        self.name_edit.move(5 + width + 5, self.surname_edit.height())

        self.patronymic_label = QLabel("Отчество:", self)
        self.patronymic_label.move(5, self.name_edit.height()*2)
        self.patronymic_edit = QLineEdit(self)
        self.patronymic_label.setFrameShape(QFrame.Panel)
        width, height = self.__get_label_text_pixel_size(self.patronymic_label)
        self.patronymic_edit.move(5 + width + 5, self.name_edit.height()*2)


    @staticmethod
    def __get_label_text_pixel_size(label):
        size_object = label.fontMetrics().boundingRect(label.text())
        return size_object.width(), size_object.height()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    # enable error messages
    sys.excepthook = except_hook

    app = QApplication([])
    window = MainWindow(const.WIN_WIDTH, const.WIN_HEIGHT, const.WIN_TITLE)
    window.show()
    # Start the event loop.
    app.exec_()
