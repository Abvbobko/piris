import bank.constants as const
import bank.db_controller as db_controller
import bank.creds as creds

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QFrame, \
    QRadioButton, QWidget, QHBoxLayout, QDateEdit
from PyQt5.QtCore import Qt

import sys
import os


class MainWindow(QMainWindow):
    def __init__(self, width, height, modes, current_mode=0, title=""):
        super(MainWindow, self).__init__()
        # ToDo: change path from static and move ui to project folder
        self.db = db_controller.DBController(creds.HOST, creds.USER, creds.PASSWORD, creds.DATABASE)
        cities = self.db.get_cities()
        citizenships = self.db.get_citizenships()
        marital_statuses = self.db.get_marital_status()
        disabilities = self.db.get_disabilities()

        ui_path = os.path.abspath('../window_view/window.ui')
        uic.loadUi(ui_path, self)

        self.window_modes = modes
        self.window_current_mode = current_mode

        self.mode_combobox.clear()
        self.mode_combobox.addItems(self.window_modes.values())

        city_names = MainWindow.get_names_from_values(cities)
        self.cities = cities
        self.residence_city_combobox.clear()
        self.residence_city_combobox.addItems(city_names)
        self.registration_city_combobox.clear()
        self.registration_city_combobox.addItems(city_names)

        citizenships_names = MainWindow.get_names_from_values(citizenships)
        self.citizenships = citizenships
        self.citizenship_combobox.clear()
        self.citizenship_combobox.addItems(citizenships_names)

        disabilities_names = MainWindow.get_names_from_values(disabilities)
        self.disabilities = disabilities
        self.disability_combobox.clear()
        self.disability_combobox.addItems(disabilities_names)

        marital_statuses_names = MainWindow.get_names_from_values(marital_statuses)
        self.marital_statuses = marital_statuses
        self.marital_status_combobox.clear()
        self.marital_status_combobox.addItems(marital_statuses_names)

        self.setWindowTitle(title)

    def change_mode(self, value):
        pass

    def add_button_click(self):
        pass

    def update_button_click(self):
        pass

    def delete_button_click(self):
        pass

    @staticmethod
    def get_names_from_values(values):
        return [None] + [item[1] for item in values] if values else []

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
    window = MainWindow(
        width=const.WIN_WIDTH,
        height=const.WIN_HEIGHT,
        title=const.WIN_TITLE,
        modes=const.MODES,
        current_mode=const.CURRENT_MODE
    )
    window.show()
    # Start the event loop.
    app.exec_()
