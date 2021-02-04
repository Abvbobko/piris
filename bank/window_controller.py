import bank.constants as const

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QFrame, \
    QRadioButton, QWidget, QHBoxLayout, QDateEdit
from PyQt5.QtCore import Qt

import sys
import os


class MainWindow(QMainWindow):
    def __init__(self, width, height, title=""):
        super(MainWindow, self).__init__()
        # ToDo: change path from static and move ui to project folder
        ui_path = os.path.abspath('../window_view/window.ui')
        uic.loadUi(ui_path, self)
        # self.resize(width, height)
        # self.setWindowTitle(title)
        self.__init_items()

    def __init_items(self):
        pass
        # fields = ["Фамилия:", "Имя:", "Отчество:", "Дата рождения"]

        # surname
        # self.surname_label = QLabel("Фамилия:", self)
        # self.surname_label.move(5, 0)
        # self.surname_edit = QLineEdit(self)
        # self.surname_label.setFrameShape(QFrame.Panel)
        # width, height = self.__get_label_text_pixel_size(self.surname_label)
        # self.surname_edit.move(5 + width + 5, 0)
        # 
        # # name
        # self.name_label = QLabel("Имя:", self)
        # self.name_label.move(5, self.surname_edit.height())
        # self.name_edit = QLineEdit(self)
        # self.name_label.setFrameShape(QFrame.Panel)
        # width, height = self.__get_label_text_pixel_size(self.name_label)
        # self.name_edit.move(5 + width + 5, self.name_label.y())
        # 
        # # patronymic
        # self.patronymic_label = QLabel("Отчество:", self)
        # self.patronymic_label.move(5, self.name_edit.height() + self.name_edit.y())
        # self.patronymic_edit = QLineEdit(self)
        # self.patronymic_label.setFrameShape(QFrame.Panel)
        # width, height = self.__get_label_text_pixel_size(self.patronymic_label)
        # self.patronymic_edit.move(5 + width + 5, self.patronymic_label.y())
        # 
        # # sex
        # self.sex_label = QLabel("Пол:", self)
        # self.sex_label.move(5, self.patronymic_edit.height() + self.patronymic_label.y())
        # width, height = self.__get_label_text_pixel_size(self.sex_label)
        # 
        # layout = QHBoxLayout()
        # widget = QWidget(self)
        # widget.setLayout(layout)
        # r_m = QRadioButton("М")
        # r_m.setChecked(True)
        # r_w = QRadioButton("Ж")
        # r_m.setFixedHeight(15)
        # r_w.setFixedHeight(15)
        # layout.addWidget(r_m)
        # layout.addWidget(r_w)
        # widget.move(width+10, self.sex_label.y())
        # 
        # # birth date
        # self.birth_date_label = QLabel("Дата рождения:", self)
        # self.birth_date_label.move(5, self.sex_label.height() + self.sex_label.y())
        # width, height = self.__get_label_text_pixel_size(self.birth_date_label)
        # self.birth_date_label.setFrameShape(QFrame.Panel)
        # self.birth_date_edit = QDateEdit(self)
        # self.birth_date_edit.move(5 + width + 5, self.birth_date_label.y())


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
