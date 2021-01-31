import bank.constants as const

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QLabel
from PyQt5.QtCore import Qt

import sys


class MainWindow(QMainWindow):
    def __init__(self, width, height, title=""):
        super().__init__()

        self.resize(width, height)
        self.setWindowTitle(title)
        # self.setStyleSheet("background-color: black;")

        # set projection label and parameters
        # self.projection_type_label = QLabel("o", self)
        # self.projection_type_label.setMargin(5)
        # self.projection_type_label.setAttribute(Qt.WA_TranslucentBackground)

    def init_items(self):
        pass


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
