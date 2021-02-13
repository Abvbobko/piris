import bank.constants as const
import bank.db_controller as db_controller
import bank.creds as creds
import bank.fields_validator as validator

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QFrame, \
    QRadioButton, QWidget, QHBoxLayout, QDateEdit, QMessageBox
from PyQt5.QtCore import Qt, QRegExp, QDate

import sys
import os
import datetime


class MainWindow(QMainWindow):
    def __init__(self, width, height, title=""):
        super(MainWindow, self).__init__()
        # ToDo: change path from static and move ui to project folder
        # get lists from db
        self.db = db_controller.DBController(creds.HOST, creds.USER, creds.PASSWORD, creds.DATABASE)
        cities = self.db.get_cities()
        citizenships = self.db.get_citizenships()
        marital_statuses = self.db.get_marital_status()
        disabilities = self.db.get_disabilities()

        # init UI
        ui_path = os.path.abspath('../window_view/window.ui')
        uic.loadUi(ui_path, self)

        self.setWindowTitle(title)

        self.window_modes = const.MODES
        self.window_current_mode = self.window_modes[const.CURRENT_MODE]

        self.mode_combobox.clear()
        self.mode_combobox.addItems(self.window_modes)

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

        # add surname, name and patronymic edit filters
        self.surname_regex = const.NAME_REGEX
        self.surname_edit.setValidator(QtGui.QRegExpValidator(QRegExp(self.surname_regex)))
        self.surname_edit.setMaxLength(const.MAX_NAME_LENGTH)
        self.name_regex = const.NAME_REGEX
        self.name_edit.setValidator(QtGui.QRegExpValidator(QRegExp(self.name_regex)))
        self.name_edit.setMaxLength(const.MAX_NAME_LENGTH)
        self.patronymic_regex = const.NAME_REGEX
        self.patronymic_edit.setValidator(QtGui.QRegExpValidator(QRegExp(self.patronymic_regex)))
        self.patronymic_edit.setMaxLength(const.MAX_NAME_LENGTH)

        # add dates constraints
        today = datetime.date.today()
        min_date = const.MIN_DATE
        min_date_qdate = QDate(min_date.year, min_date.month, min_date.day)
        max_date_qdate = QDate(today.year, today.month, today.day)
        self.birth_date_edit.setMinimumDate(min_date_qdate)
        self.birth_date_edit.setMaximumDate(max_date_qdate)
        self.issue_date_edit.setMinimumDate(min_date_qdate)
        self.issue_date_edit.setMaximumDate(max_date_qdate)

        # buttons functionality
        self.add_button.clicked.connect(self.add_button_click)
        self.mode_combobox.currentTextChanged.connect(self.change_mode)

    def change_mode(self, value):
        self.window_current_mode = value
        if value == self.window_modes[0]:
            # add mode
            self.add_button.clicked.disconnect()
            self.add_button.clicked.connect(self.add_button_click)
        elif value == self.window_modes[1]:
            # update mode
            self.add_button.clicked.disconnect()
            self.add_button.clicked.connect(self.update_button_click)
        elif value == self.window_modes[2]:
            # delete mode
            self.add_button.clicked.disconnect()
            self.add_button.clicked.connect(self.delete_button_click)
        print(f'change on {value}')

    def call_error_box(self, error_title="Ошибка", error_text=""):
        print("ERROR")
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Critical)
        message_box.setText(error_text)
        message_box.setWindowTitle(error_title)
        message_box.exec_()

    def validate_fields(self):
        # validate surname
        error = validator.validate_name(
            name=self.surname_edit.text(), field_name="Фамилия",
            name_regex=self.surname_regex,
            max_length=self.surname_edit.maxLength()
        )
        if error:
            self.call_error_box(error_text=error)
            return False

        # validate name
        error = validator.validate_name(
            name=self.name_edit.text(), field_name="Имя",
            name_regex=self.name_regex,
            max_length=self.name_edit.maxLength()
        )
        if error:
            self.call_error_box(error_text=error)
            return False

        # validate patronymic
        error = validator.validate_name(
            name=self.patronymic_edit.text(), field_name="Отчество",
            name_regex=self.patronymic_regex,
            max_length=self.patronymic_edit.maxLength()
        )
        if error:
            self.call_error_box(error_text=error)
            return False

        # validate birth_date
        date = self.birth_date_edit.date().toPyDate()
        min_date = self.birth_date_edit.minimumDate().toPyDate()
        max_date = self.birth_date_edit.maximumDate().toPyDate()
        error = validator.date_validator(
            date=date, field_name="Дата рождения", min_date=min_date, max_date=max_date
        )
        if error:
            self.call_error_box(error_text=error)
            return False

        # validate issue_date
        date = self.issue_date_edit.date().toPyDate()
        min_date = self.issue_date_edit.minimumDate().toPyDate()
        max_date = self.issue_date_edit.maximumDate().toPyDate()
        error = validator.date_validator(
            date=date, field_name="Дата выдачи", min_date=min_date, max_date=max_date
        )
        if error:
            self.call_error_box(error_text=error)
            return False

        # validate sex
        error = validator.radio_button_validator(
            checked_list=[self.m_radio_button.isChecked(), self.w_radio_button.isChecked()],
            field_name="Пол"
        )
        if error:
            self.call_error_box(error_text=error)
            return False

        # validate residence city
        error = validator.combobox_validator(
            self.residence_city_combobox.currentText(),
            field_name="Город факт. проживания"
        )
        if error:
            self.call_error_box(error_text=error)
            return False

        # validate registration city
        error = validator.combobox_validator(
            self.registration_city_combobox.currentText(),
            field_name="Город прописки"
        )
        if error:
            self.call_error_box(error_text=error)
            return False

        # validate citizenship
        error = validator.combobox_validator(
            self.citizenship_combobox.currentText(),
            field_name="Гражданство"
        )
        if error:
            self.call_error_box(error_text=error)
            return False

        # validate marital status
        error = validator.combobox_validator(
            self.marital_status_combobox.currentText(),
            field_name="Семейное положение"
        )
        if error:
            self.call_error_box(error_text=error)
            return False

        # validate disability
        error = validator.combobox_validator(
            self.disability_combobox.currentText(),
            field_name="Инвалидность"
        )
        if error:
            self.call_error_box(error_text=error)
            return False

        # validate pension
        error = validator.checkbox_validator(
            self.pension_checkbox.isChecked(),
            field_name="Пенсионер"
        )
        if error:
            self.call_error_box(error_text=error)
            return False



        return True

    def add_button_click(self):
        print('add')
        if self.validate_fields():
            print("OK")

    def update_button_click(self):
        print('update')

    def delete_button_click(self):
        print('delete')

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
    )
    window.show()
    # Start the event loop.
    app.exec_()
