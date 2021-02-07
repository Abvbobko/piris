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
        # self.setWindowTitle(title)

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
