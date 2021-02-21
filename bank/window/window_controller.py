import bank.window.constants.field_constants as field_const
import bank.window.constants.window_constants as win_const

import bank.db.db_controller as db_controller
import bank.db.constants.creds as creds
import bank.window.data_processing.fields_validator as validator
import bank.window.data_processing.fields_prevalidator as prevalidator
import bank.window.data_processing.data_converter as data_converter
import bank.window.fields_setter as fields_setter
import bank.window.data_processing.db_data_converter as db_data_converter

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import QRegExp

import sys
import os
import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # get lists from db
        self.db = db_controller.DBController(creds.HOST, creds.USER, creds.PASSWORD, creds.DATABASE)
        cities = self.db.get_cities()
        citizenships = self.db.get_citizenships()
        marital_statuses = self.db.get_marital_status()
        disabilities = self.db.get_disabilities()

        # init UI
        ui_path = os.path.abspath(win_const.UI_PATH)
        uic.loadUi(ui_path, self)

        self.setWindowTitle(win_const.WIN_TITLE)

        self.window_modes = win_const.MODES
        self.window_current_mode = self.window_modes[win_const.CURRENT_MODE]

        self.mode_combobox.clear()
        self.mode_combobox.addItems(self.window_modes)

        # set all comboboxes
        fields_setter.set_combobox(self.residence_city_combobox, cities, "Город факт. проживания")
        fields_setter.set_combobox(self.registration_city_combobox, cities, "Город прописки")
        fields_setter.set_combobox(self.citizenship_combobox, citizenships, "Гражданство")
        fields_setter.set_combobox(self.disability_combobox, disabilities, "Инвалидность")
        fields_setter.set_combobox(self.marital_status_combobox, marital_statuses, "Семейное положение")

        # add surname, name and patronymic edit filters
        fields_setter.set_string_edit(
            self.surname_edit, field_name="Фамилия", mask_regex=field_const.NAME_REGEX,
            max_length=field_const.MAX_NAME_LENGTH, can_be_empty=False
        )

        fields_setter.set_string_edit(
            self.name_edit, field_name="Имя", mask_regex=field_const.NAME_REGEX,
            max_length=field_const.MAX_NAME_LENGTH, can_be_empty=False
        )

        fields_setter.set_string_edit(
            self.patronymic_edit, field_name="Отчество", mask_regex=field_const.NAME_REGEX,
            max_length=field_const.MAX_NAME_LENGTH, can_be_empty=False
        )

        # add dates constraints
        today = datetime.date.today()
        min_date = field_const.MIN_DATE
        fields_setter.set_date_edit(self.birth_date_edit, min_date, max_date=today, field_name="Дата рождения")
        fields_setter.set_date_edit(self.issue_date_edit, min_date, max_date=today, field_name="Дата выдачи")

        # add constraints for the string edits
        fields_setter.set_string_edit(
            self.passport_series_edit, field_name="Серия паспорта", mask_regex=field_const.PASSPORT_SERIES_MASK,
            max_length=field_const.MAX_PASSPORT_SERIES_LENGTH, can_be_empty=False
        )

        fields_setter.set_string_edit(
            self.issued_by_edit, field_name="Кем выдан", mask_regex=None,
            max_length=field_const.MAX_INFO_STRING_LENGTH, can_be_empty=False
        )

        fields_setter.set_string_edit(
            self.birth_place_edit, field_name="Место рождения", mask_regex=None,
            max_length=field_const.MAX_INFO_STRING_LENGTH, can_be_empty=False
        )

        fields_setter.set_string_edit(
            self.residence_address_edit, field_name="Адрес факт. проживания", mask_regex=None,
            max_length=field_const.MAX_INFO_STRING_LENGTH, can_be_empty=False
        )

        fields_setter.set_string_edit(
            self.email_edit, field_name="Email", mask_regex=None,
            max_length=field_const.MAX_INFO_STRING_LENGTH, can_be_empty=True
        )

        # phone number validators
        placeholder = field_const.HOME_PHONE_PLACEHOLDER
        fields_setter.set_string_edit(
            self.home_phone_edit, field_name="Телефон домашний", mask_regex=field_const.HOME_PHONE_MASK,
            max_length=len(placeholder), can_be_empty=True, placeholder=placeholder
        )

        placeholder = field_const.MOBILE_PHONE_PLACEHOLDER
        fields_setter.set_string_edit(
            self.mobile_phone_edit, field_name="Телефон мобильный", mask_regex=field_const.MOBILE_PHONE_MASK,
            max_length=field_const.MOBILE_PHONE_LENGTH, can_be_empty=True, placeholder=placeholder
        )

        # set passport number and id validators
        fields_setter.set_string_edit(
            self.passport_number_edit, field_name="Номер паспорта", mask_regex=field_const.PASSPORT_NUMBER_MASK,
            max_length=field_const.PASSPORT_NUMBER_LENGTH, can_be_empty=False
        )

        self.identification_number_regex = field_const.PASSPORT_ID_MASK
        self.identification_number_edit.setMaxLength(field_const.PASSPORT_ID_LENGTH)
        self.identification_number_edit.setValidator(QtGui.QRegExpValidator(QRegExp(self.identification_number_regex)))
        self.identification_number_edit.field_name = "Идентификационный номер"

        fields_setter.set_string_edit(
            self.monthly_income_edit, field_name="Ежемесячный доход", mask_regex=field_const.INCOME_MASK,
            max_length=field_const.INCOME_MAX_LENGTH, can_be_empty=True
        )

        self.pension_checkbox.field_name = "Пенсионер"
        self.m_radio_button.field_name = "Пол"
        self.w_radio_button.field_name = "Пол"

        # buttons functionality
        self.add_button.clicked.connect(self.add_button_click)
        self.mode_combobox.currentTextChanged.connect(self.change_mode)

        self.tabs.currentChanged.connect(self.change_tab)

        # disable table editing by user
        self.clients_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

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
    def call_message_box(title="", text="", icon=QMessageBox.NoIcon):
        message_box = QMessageBox()
        message_box.setIcon(icon)
        message_box.setText(text)
        message_box.setWindowTitle(title)
        message_box.exec_()

    @staticmethod
    def call_error_box(error_title="Ошибка", error_text=""):
        print("ERROR")
        MainWindow.call_message_box(error_title, error_text, QMessageBox.Critical)

    @staticmethod
    def call_ok_box(ok_title="ОK", ok_text=""):
        print("OK")
        MainWindow.call_message_box(ok_title, ok_text, QMessageBox.Information)

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

        error = prevalidator.list_validation_call(string_data_edits, prevalidator.validate_string_edit)
        if error:
            return error

        comboboxes = [
            self.residence_city_combobox,
            self.registration_city_combobox,
            self.citizenship_combobox,
            self.marital_status_combobox,
            self.disability_combobox
        ]

        error = prevalidator.list_validation_call(comboboxes, prevalidator.validate_combobox)
        if error:
            return error

        # change surname, name and patronymic to the fist big letter format
        names_edit_list = [self.surname_edit, self.name_edit, self.patronymic_edit]
        for edit in names_edit_list:
            fields_setter.set_text_to_edit(edit, edit.text(), transform_func=data_converter.convert_name)

        # validate birth_date and issue_date
        date_edit_list = [self.birth_date_edit, self.issue_date_edit]
        error = prevalidator.list_validation_call(date_edit_list, prevalidator.validate_date_edit)
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
        checkbox_list = [self.pension_checkbox]
        error = prevalidator.list_validation_call(checkbox_list, prevalidator.validate_checkbox)
        if error:
            return error

        # fix passport series
        fields_setter.set_text_to_edit(
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

    def validate_fields_with_db(self):
        passport_series = self.passport_series_edit.text()
        passport_number = int(self.passport_number_edit.text())
        if self.db.is_passport_number_exists(passport_series=passport_series, passport_number=passport_number):
            return "Паспорт с таким номером и серией уже существует."
        passport_id = self.identification_number_edit.text()
        if self.db.is_passport_id_exists(passport_id=passport_id):
            return "Паспорт с таким идентификационным номером уже существует."
        return None

    def add_person(self):
        sex = db_data_converter.convert_sex_to_db_form(
            self.m_radio_button.isChecked(),
            self.w_radio_button.isChecked()
        )
        birth_date = db_data_converter.convert_date_to_the_db_form(self.birth_date_edit.date().toPyDate())
        issue_date = db_data_converter.convert_date_to_the_db_form(self.issue_date_edit.date().toPyDate())
        passport_number = int(self.passport_number_edit.text())
        home_phone = db_data_converter.get_optional_value(self.home_phone_edit)
        mobile_phone = db_data_converter.get_optional_value(self.mobile_phone_edit)
        email = db_data_converter.get_optional_value(self.email_edit)
        monthly_income = db_data_converter.get_optional_value(self.monthly_income_edit)
        monthly_income = float(monthly_income) if monthly_income else None
        pension = int(self.pension_checkbox.isChecked())
        return self.db.insert_person(
            first_name=self.name_edit.text(),
            surname=self.surname_edit.text(),
            patronymic=self.patronymic_edit.text(),
            birth_date=birth_date,
            sex=sex,
            passport_series=self.passport_series_edit.text(),
            passport_number=passport_number,
            issued_by=self.issued_by_edit.text(),
            issue_date=issue_date,
            identification_number=self.identification_number_edit.text(),
            birth_place=self.birth_place_edit.text(),
            residence_address=self.residence_address_edit.text(),
            home_phone=home_phone,
            mobile_phone=mobile_phone,
            email=email,
            pension=pension,
            monthly_income=monthly_income,
            marital_status=self.marital_status_combobox.currentText(),
            disability=self.disability_combobox.currentText(),
            citizenship=self.citizenship_combobox.currentText(),
            residence_city=self.residence_city_combobox.currentText(),
            registration_city=self.registration_city_combobox.currentText()
        )

    def add_button_click(self):
        print('add')
        error = self.validate_fields() # todo: раскомментить
        # error = '' ########################### todo: delete this row
        if error:
            MainWindow.call_error_box(error_text=error)
            return
        error = self.validate_fields_with_db() # todo: раскомментить
        if error:
            MainWindow.call_error_box(error_text=error)
            return
        error = self.add_person() # todo: раскомментить
        if error:
            MainWindow.call_error_box(error_text=error)
            return
        MainWindow.call_ok_box(ok_text="Клиент успешно добавлен.") # todo: раскомментить
        # print(self.db.get_clients())

    def update_button_click(self):
        print('update')

    def delete_button_click(self):
        print('delete')

    def fill_clients_table(self):
        table_values = self.db.get_clients()
        headers = table_values["columns"]
        records = table_values["records"]

        # remove column idPerson (#todo: подумать, мб оставить и по ней сделать удаление просто)
        #  todo: (можно даже внутри вкладки)

        self.clients_table.setColumnCount(len(headers) - 1)
        self.clients_table.setRowCount(len(records))
        self.clients_table.setHorizontalHeaderLabels(headers[1:])

        if len(records) == 0:
            return
        records = db_data_converter.convert_records(records, headers)
        for i in range(len(records)):
            for j in range(1, len(records[i])):
                self.clients_table.setItem(i, j-1, QTableWidgetItem(str(records[i][j])))

    def change_tab(self, index):
        if index == win_const.CLIENT_LIST_TAB_INDEX:
            self.fill_clients_table()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    # enable error messages
    sys.excepthook = except_hook

    app = QApplication([])
    window = MainWindow()
    window.show()
    # Start the event loop.
    app.exec_()
