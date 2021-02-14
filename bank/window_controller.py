import bank.constants as const
import bank.db_controller as db_controller
import bank.creds as creds
import bank.fields_validator as validator
import bank.data_converter as data_converter

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

        # set all comboboxes
        self.set_combobox(self.residence_city_combobox, cities, "Город факт. проживания")
        self.set_combobox(self.registration_city_combobox, cities, "Город прописки")
        self.set_combobox(self.citizenship_combobox, citizenships, "Гражданство")
        self.set_combobox(self.disability_combobox, disabilities, "Инвалидность")
        self.set_combobox(self.marital_status_combobox, marital_statuses, "Семейное положение")

        # add surname, name and patronymic edit filters
        self.set_string_edit(
            self.surname_edit, field_name="Фамилия", mask_regex=const.NAME_REGEX,
            max_length=const.MAX_NAME_LENGTH, can_be_empty=False
        )

        self.set_string_edit(
            self.name_edit, field_name="Имя", mask_regex=const.NAME_REGEX,
            max_length=const.MAX_NAME_LENGTH, can_be_empty=False
        )

        self.set_string_edit(
            self.patronymic_edit, field_name="Отчество", mask_regex=const.NAME_REGEX,
            max_length=const.MAX_NAME_LENGTH, can_be_empty=False
        )

        # add dates constraints
        today = datetime.date.today()
        min_date = const.MIN_DATE
        min_date_qdate = QDate(min_date.year, min_date.month, min_date.day)
        max_date_qdate = QDate(today.year, today.month, today.day)
        self.birth_date_edit.setMinimumDate(min_date_qdate)
        self.birth_date_edit.setMaximumDate(max_date_qdate)
        self.birth_date_edit.field_name = "Дата рождения"

        self.issue_date_edit.setMinimumDate(min_date_qdate)
        self.issue_date_edit.setMaximumDate(max_date_qdate)
        self.issue_date_edit.field_name = "Дата выдачи"

        # add constraints for the string edits
        self.set_string_edit(
            self.passport_series_edit, field_name="Серия паспорта", mask_regex=const.PASSPORT_SERIES_MASK,
            max_length=const.MAX_PASSPORT_SERIES_LENGTH, can_be_empty=False
        )

        self.set_string_edit(
            self.issued_by_edit, field_name="Кем выдан", mask_regex=None,
            max_length=const.MAX_INFO_STRING_LENGTH, can_be_empty=False
        )

        self.set_string_edit(
            self.birth_place_edit, field_name="Место рождения", mask_regex=None,
            max_length=const.MAX_INFO_STRING_LENGTH, can_be_empty=False
        )

        self.set_string_edit(
            self.residence_address_edit, field_name="Адрес факт. проживания", mask_regex=None,
            max_length=const.MAX_INFO_STRING_LENGTH, can_be_empty=False
        )

        self.set_string_edit(
            self.email_edit, field_name="Email", mask_regex=None,
            max_length=const.MAX_INFO_STRING_LENGTH, can_be_empty=True
        )

        # phone number validators
        placeholder = const.HOME_PHONE_PLACEHOLDER
        self.set_string_edit(
            self.home_phone_edit, field_name="Телефон домашний", mask_regex=const.HOME_PHONE_MASK,
            max_length=len(placeholder), can_be_empty=True, placeholder=placeholder
        )

        placeholder = const.MOBILE_PHONE_PLACEHOLDER
        self.set_string_edit(
            self.mobile_phone_edit, field_name="Телефон мобильный", mask_regex=const.MOBILE_PHONE_MASK,
            max_length=const.MOBILE_PHONE_LENGTH, can_be_empty=True, placeholder=placeholder
        )

        # set passport number and id validators
        self.set_string_edit(
            self.passport_number_edit, field_name="Номер паспорта", mask_regex=const.PASSPORT_NUMBER_MASK,
            max_length=const.PASSPORT_NUMBER_LENGTH, can_be_empty=False
        )

        self.identification_number_regex = const.PASSPORT_ID_MASK
        self.identification_number_edit.setMaxLength(const.PASSPORT_ID_LENGTH)
        self.identification_number_edit.setValidator(QtGui.QRegExpValidator(QRegExp(self.identification_number_regex)))
        self.identification_number_edit.field_name = "Идентификационный номер"

        self.set_string_edit(
            self.monthly_income_edit, field_name="Ежемесячный доход", mask_regex=const.INCOME_MASK,
            max_length=const.INCOME_MAX_LENGTH, can_be_empty=True
        )

        self.pension_checkbox.field_name = "Пенсионер"
        self.m_radio_button.field_name = "Пол"
        self.w_radio_button.field_name = "Пол"

        # buttons functionality
        self.add_button.clicked.connect(self.add_button_click)
        self.mode_combobox.currentTextChanged.connect(self.change_mode)

    def set_string_edit(self, edit, field_name=None,
                        can_be_empty=False, max_length=255, mask_regex=None, placeholder=None):
        edit.mask_regex = mask_regex
        edit.setMaxLength(max_length)
        if mask_regex:
            edit.setValidator(QtGui.QRegExpValidator(QRegExp(edit.mask_regex)))
        edit.field_name = field_name
        edit.can_be_empty = can_be_empty
        if placeholder:
            edit.setPlaceholderText(placeholder)

    def set_combobox(self, combobox, db_values, field_name):
        db_values_names = MainWindow.get_names_from_values(db_values)
        combobox.db_values = db_values
        combobox.clear()
        combobox.addItems(db_values_names)
        combobox.field_name = field_name

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

    def validate_string_edit(self, edit):
        error = validator.string_validator(
            string=edit.text(),
            field_name=edit.field_name,
            mask=edit.mask_regex,
            max_length=edit.maxLength(),
            can_be_empty=edit.can_be_empty
        )
        return error

    def validate_combobox(self, combobox):
        error = validator.combobox_validator(
            combobox.currentText(),
            field_name=combobox.field_name
        )
        return error

    def validate_fields(self):

        # validate string data edits
        string_data_edits = [
            self.surname_edit,
            self.name_edit,
            self.patronymic_edit,
            self.passport_series_edit,
            self.issued_by_edit,
            self.birth_place_edit,
            self.residence_address_edit,
            self.email_edit,
            self.home_phone_edit,
            self.mobile_phone_edit,
            self.passport_number_edit,
            self.monthly_income_edit
        ]
        for edit in string_data_edits:
            error = self.validate_string_edit(edit)
            if error:
                return error

        comboboxes = [
            self.residence_city_combobox,
            self.registration_city_combobox,
            self.citizenship_combobox,
            self.marital_status_combobox,
            self.disability_combobox
        ]

        for combobox in comboboxes:
            error = self.validate_combobox(combobox)
            if error:
                return error

        # fix surname
        surname = data_converter.convert_name(self.surname_edit.text())
        self.surname_edit.setText(surname)

        # fix name
        name = data_converter.convert_name(self.name_edit.text())
        self.name_edit.setText(name)

        # fix patronymic
        patronymic = data_converter.convert_name(self.patronymic_edit.text())
        self.patronymic_edit.setText(patronymic)

        # validate birth_date
        date = self.birth_date_edit.date().toPyDate()
        min_date = self.birth_date_edit.minimumDate().toPyDate()
        max_date = self.birth_date_edit.maximumDate().toPyDate()
        error = validator.date_validator(
            date=date, field_name=self.birth_date_edit.field_name, min_date=min_date, max_date=max_date
        )
        if error:
            return error

        # validate issue_date
        date = self.issue_date_edit.date().toPyDate()
        min_date = self.issue_date_edit.minimumDate().toPyDate()
        max_date = self.issue_date_edit.maximumDate().toPyDate()
        error = validator.date_validator(
            date=date, field_name=self.issue_date_edit.field_name, min_date=min_date, max_date=max_date
        )
        if error:
            return error

        # validate sex
        error = validator.radio_button_validator(
            checked_list=[self.m_radio_button.isChecked(), self.w_radio_button.isChecked()],
            field_name=self.m_radio_button.field_name
        )
        if error:
            return error

        # validate pension
        error = validator.checkbox_validator(
            self.pension_checkbox.isChecked(),
            field_name=self.pension_checkbox.field_name
        )
        if error:
            return error

        # fix passport series
        passport_series = data_converter.to_upper(self.passport_series_edit.text())
        self.passport_series_edit.setText(passport_series)

        # validate passport_id
        birth_date = self.birth_date_edit.date().toPyDate()
        sex = 0 if self.m_radio_button.isChecked() else 1
        error = validator.passport_id_validator(
            passport_id=self.identification_number_edit.text(),
            birth_date=birth_date,
            sex=sex,
            field_name=self.identification_number_edit.field_name,
            length=self.identification_number_edit.maxLength(),
            mask=self.identification_number_regex
        )
        if error:
            return error

        return None

    def add_button_click(self):
        print('add')
        error = self.validate_fields()
        if error:
            self.call_error_box(error_text=error)
        else:
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
