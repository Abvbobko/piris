import bank.constants.constants as const
import bank.db_controller as db_controller
import bank.constants.creds as creds
import bank.data_processing.fields_validator as validator
import bank.data_processing.data_converter as data_converter

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QRegExp, QDate

import sys
import os
import datetime


class MainWindow(QMainWindow):
    def __init__(self, title=""):
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
        MainWindow.set_combobox(self.residence_city_combobox, cities, "Город факт. проживания")
        MainWindow.set_combobox(self.registration_city_combobox, cities, "Город прописки")
        MainWindow.set_combobox(self.citizenship_combobox, citizenships, "Гражданство")
        MainWindow.set_combobox(self.disability_combobox, disabilities, "Инвалидность")
        MainWindow.set_combobox(self.marital_status_combobox, marital_statuses, "Семейное положение")

        # add surname, name and patronymic edit filters
        MainWindow.set_string_edit(
            self.surname_edit, field_name="Фамилия", mask_regex=const.NAME_REGEX,
            max_length=const.MAX_NAME_LENGTH, can_be_empty=False
        )

        MainWindow.set_string_edit(
            self.name_edit, field_name="Имя", mask_regex=const.NAME_REGEX,
            max_length=const.MAX_NAME_LENGTH, can_be_empty=False
        )

        MainWindow.set_string_edit(
            self.patronymic_edit, field_name="Отчество", mask_regex=const.NAME_REGEX,
            max_length=const.MAX_NAME_LENGTH, can_be_empty=False
        )

        # add dates constraints
        today = datetime.date.today()
        min_date = const.MIN_DATE
        MainWindow.set_date_edit(self.birth_date_edit, min_date, max_date=today, field_name="Дата рождения")
        MainWindow.set_date_edit(self.issue_date_edit, min_date, max_date=today, field_name="Дата выдачи")

        # add constraints for the string edits
        MainWindow.set_string_edit(
            self.passport_series_edit, field_name="Серия паспорта", mask_regex=const.PASSPORT_SERIES_MASK,
            max_length=const.MAX_PASSPORT_SERIES_LENGTH, can_be_empty=False
        )

        MainWindow.set_string_edit(
            self.issued_by_edit, field_name="Кем выдан", mask_regex=None,
            max_length=const.MAX_INFO_STRING_LENGTH, can_be_empty=False
        )

        MainWindow.set_string_edit(
            self.birth_place_edit, field_name="Место рождения", mask_regex=None,
            max_length=const.MAX_INFO_STRING_LENGTH, can_be_empty=False
        )

        MainWindow.set_string_edit(
            self.residence_address_edit, field_name="Адрес факт. проживания", mask_regex=None,
            max_length=const.MAX_INFO_STRING_LENGTH, can_be_empty=False
        )

        MainWindow.set_string_edit(
            self.email_edit, field_name="Email", mask_regex=None,
            max_length=const.MAX_INFO_STRING_LENGTH, can_be_empty=True
        )

        # phone number validators
        placeholder = const.HOME_PHONE_PLACEHOLDER
        MainWindow.set_string_edit(
            self.home_phone_edit, field_name="Телефон домашний", mask_regex=const.HOME_PHONE_MASK,
            max_length=len(placeholder), can_be_empty=True, placeholder=placeholder
        )

        placeholder = const.MOBILE_PHONE_PLACEHOLDER
        MainWindow.set_string_edit(
            self.mobile_phone_edit, field_name="Телефон мобильный", mask_regex=const.MOBILE_PHONE_MASK,
            max_length=const.MOBILE_PHONE_LENGTH, can_be_empty=True, placeholder=placeholder
        )

        # set passport number and id validators
        MainWindow.set_string_edit(
            self.passport_number_edit, field_name="Номер паспорта", mask_regex=const.PASSPORT_NUMBER_MASK,
            max_length=const.PASSPORT_NUMBER_LENGTH, can_be_empty=False
        )

        self.identification_number_regex = const.PASSPORT_ID_MASK
        self.identification_number_edit.setMaxLength(const.PASSPORT_ID_LENGTH)
        self.identification_number_edit.setValidator(QtGui.QRegExpValidator(QRegExp(self.identification_number_regex)))
        self.identification_number_edit.field_name = "Идентификационный номер"

        MainWindow.set_string_edit(
            self.monthly_income_edit, field_name="Ежемесячный доход", mask_regex=const.INCOME_MASK,
            max_length=const.INCOME_MAX_LENGTH, can_be_empty=True
        )

        self.pension_checkbox.field_name = "Пенсионер"
        self.m_radio_button.field_name = "Пол"
        self.w_radio_button.field_name = "Пол"

        # buttons functionality
        self.add_button.clicked.connect(self.add_button_click)
        self.mode_combobox.currentTextChanged.connect(self.change_mode)

    @staticmethod
    def set_string_edit(edit, field_name=None,
                        can_be_empty=False, max_length=255, mask_regex=None, placeholder=None):
        edit.mask_regex = mask_regex
        edit.setMaxLength(max_length)
        if mask_regex:
            edit.setValidator(QtGui.QRegExpValidator(QRegExp(edit.mask_regex)))
        edit.field_name = field_name
        edit.can_be_empty = can_be_empty
        if placeholder:
            edit.setPlaceholderText(placeholder)

    @staticmethod
    def set_combobox(combobox, db_values, field_name):
        db_values_names = MainWindow.get_names_from_values(db_values)
        combobox.db_values = db_values
        combobox.clear()
        combobox.addItems(db_values_names)
        combobox.field_name = field_name

    @staticmethod
    def set_date_edit(date_edit, min_date, max_date, field_name):
        min_date_qdate = QDate(min_date.year, min_date.month, min_date.day)
        max_date_qdate = QDate(max_date.year, max_date.month, max_date.day)
        date_edit.setMinimumDate(min_date_qdate)
        date_edit.setMaximumDate(max_date_qdate)
        date_edit.field_name = field_name

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

    @staticmethod
    def call_error_box(error_title="Ошибка", error_text=""):
        print("ERROR")
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Critical)
        message_box.setText(error_text)
        message_box.setWindowTitle(error_title)
        message_box.exec_()

    @staticmethod
    def validate_string_edit(edit):
        error = validator.string_validator(
            text=edit.text(),
            field_name=edit.field_name,
            mask=edit.mask_regex,
            max_length=edit.maxLength(),
            can_be_empty=edit.can_be_empty
        )
        return error

    @staticmethod
    def validate_combobox(combobox):
        error = validator.combobox_validator(
            combobox.currentText(),
            field_name=combobox.field_name
        )
        return error

    @staticmethod
    def set_text_to_edit(edit, text, transform_func=None):
        if transform_func:
            text = transform_func(text)
        edit.setText(text)

    @staticmethod
    def validate_date_edit(edit):
        date = edit.date().toPyDate()
        min_date = edit.minimumDate().toPyDate()
        max_date = edit.maximumDate().toPyDate()
        error = validator.date_validator(
            date=date, field_name=edit.field_name, min_date=min_date, max_date=max_date
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
            error = MainWindow.validate_string_edit(edit)
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
            error = MainWindow.validate_combobox(combobox)
            if error:
                return error

        # change surname, name and patronymic to the fist big letter format
        names_edit_list = [self.surname_edit, self.name_edit, self.patronymic_edit]
        for edit in names_edit_list:
            MainWindow.set_text_to_edit(edit, edit.text(), transform_func=data_converter.convert_name)

        # validate birth_date and issue_date
        date_edit_list = [self.birth_date_edit, self.issue_date_edit]
        for date_edit in date_edit_list:
            error = MainWindow.validate_date_edit(date_edit)
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
        MainWindow.set_text_to_edit(
            self.passport_series_edit, self.passport_series_edit.text(), transform_func=data_converter.to_upper
        )

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
            MainWindow.call_error_box(error_text=error)
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
    window = MainWindow(title=const.WIN_TITLE)
    window.show()
    # Start the event loop.
    app.exec_()
