import bank.window.constants.field_constants as field_const
import bank.window.constants.window_constants as win_const

import bank.db.db_controller as db_controller
import bank.db.constants.creds as creds
import bank.window.data_processing.fields_validator as validator
import bank.window.data_processing.fields_prevalidator as prevalidator
import bank.window.data_processing.data_converter as data_converter
import bank.window.fields_setter as fields_setter
import bank.window.data_processing.db_data_converter as db_data_converter
import bank.window.data_processing.edit_manipulator as edit_manipulator

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QAbstractItemView

import sys
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # get lists from db
        self.db = db_controller.DBController(creds.HOST, creds.USER, creds.PASSWORD, creds.DATABASE)
        # init UI
        ui_path = os.path.abspath(win_const.UI_PATH)
        uic.loadUi(ui_path, self)

        self.setWindowTitle(win_const.WIN_TITLE)

        self.window_modes = win_const.MODES
        self.window_current_mode = self.window_modes[win_const.CURRENT_MODE]

        self.mode_combobox.clear()
        self.mode_combobox.addItems(self.window_modes)

        fields_setter.set_all_fields(self)
        # buttons functionality
        self.add_button.clicked.connect(self._add_button_click)
        self.mode_combobox.currentTextChanged.connect(self._change_mode)

        # disable table editing by user
        self.clients_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        fields_setter.set_string_edit(
            self.id_edit, field_name="id", mask_regex=field_const.ID_MASK,
            max_length=field_const.ID_MAX_LENGTH, can_be_empty=False
        )

        self.find_button.clicked.connect(self._find_button_click)
        # id of person that is updating now
        self.updating_person_id = None

        self.tabs.currentChanged.connect(self._change_tab)

    @staticmethod
    def _enable_field(label, edit, enable):
        label.setEnabled(enable)
        edit.setEnabled(enable)

    def _enable_id_field(self, enable):
        MainWindow._enable_field(self.id_label, self.id_edit, enable)

    def _set_mode(self, enable_id_field, find_button_enable, add_button_func, add_button_text):
        self._enable_id_field(enable_id_field)
        self.find_button.setEnabled(find_button_enable)
        self.add_button.clicked.disconnect()
        self.add_button.clicked.connect(add_button_func)
        self.add_button.setText(add_button_text)

    def _change_mode(self, value):
        self.window_current_mode = value
        self.updating_person_id = None
        if value == self.window_modes[0]:
            # add mode
            self.id_edit.clear()
            self._set_mode(
                enable_id_field=False,
                find_button_enable=False,
                add_button_func=self._add_button_click,
                add_button_text="Добавить"
            )
        elif value == self.window_modes[1]:
            # update mode
            self._set_mode(
                enable_id_field=True,
                find_button_enable=True,
                add_button_func=self._update_button_click,
                add_button_text="Редактировать"
            )
        elif value == self.window_modes[2]:
            # delete mode
            self._set_mode(
                enable_id_field=True,
                find_button_enable=False,
                add_button_func=self._delete_button_click,
                add_button_text="Удалить"
            )
        print(f'change on {value}')

    def _find_button_click(self):
        edit_list = [self.id_edit]
        error = prevalidator.list_validation_call(edit_list, prevalidator.validate_string_edit)
        if error:
            MainWindow.call_error_box(error_text=error)
            return
        person_id = int(self.id_edit.text())
        person_record = self.db.get_person(person_id)
        record = person_record["records"]
        header = person_record["columns"]
        if not record:
            error = "Запись не найдена."
            MainWindow.call_error_box(error_text=error)
            self._clear_data_edits()
            return
        self._fill_data_edits(record[0], header)
        self.updating_person_id = person_id

    def _get_mapper(self):
        """Maps column name and edit"""
        return edit_manipulator.get_mapper(self)

    def _map_column_name_to_edit(self, column_name):
        mapper = self._get_mapper()
        if column_name not in mapper.keys():
            return None
        return mapper[column_name]

    def _fill_data_edits(self, record, header):
        for i in range(len(record)):
            edit = self._map_column_name_to_edit(header[i])
            if edit:
                edit_manipulator.fill_edit(edit, header[i], record[i])

    def _clear_data_edits(self):
        mapper = self._get_mapper()
        for edit in mapper.values():
            edit_manipulator.clear_edit(edit)

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

    def _validate_fields(self):
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
            mask=self.identification_number_edit.mask_regex
        )
        if error:
            return error

        return None

    def _validate_fields_with_db(self, updating_mode=False):
        passport_series = self.passport_series_edit.text()
        passport_number = int(self.passport_number_edit.text())
        if self.db.is_passport_number_exists(passport_series=passport_series, passport_number=passport_number,
                                             updating_mode=updating_mode, person_id=self.updating_person_id):
            return "Паспорт с таким номером и серией уже существует."
        passport_id = self.identification_number_edit.text()
        if self.db.is_passport_id_exists(passport_id=passport_id,
                                         updating_mode=updating_mode, person_id=self.updating_person_id):
            return "Паспорт с таким идентификационным номером уже существует."
        return None

    def _add_person(self, updating_mode=False):
        person_id = None
        if updating_mode:
            person_id = self.updating_person_id

        mapper = self._get_mapper()
        params_dict = {}
        for column_name, edit in mapper.items():
            params_dict[column_name] = edit_manipulator.get_current_value(edit, column_name)

        return self.db.insert_person(
            update_mode=updating_mode,
            person_id=person_id,
            **params_dict
        )

    def _add_button_click(self):
        print('add')
        pipeline = [
            self._validate_fields,
            self._validate_fields_with_db,
            self._add_person
        ]
        for pipeline_func in pipeline:
            error = pipeline_func()
            if error:
                MainWindow.call_error_box(error_text=error)
                return

        MainWindow.call_ok_box(ok_text="Клиент успешно добавлен.")
        self._clear_data_edits()

    def _update_button_click(self):
        print('update')

        error = self._validate_fields()
        if error:
            MainWindow.call_error_box(error_text=error)
            return
        error = self._validate_fields_with_db(updating_mode=True)
        if error:
            MainWindow.call_error_box(error_text=error)
            return
        error = self._add_person(updating_mode=True)
        if error:
            MainWindow.call_error_box(error_text=error)
            return
        MainWindow.call_ok_box(ok_text="Клиент успешно обновлен.")
        self._clear_data_edits()

    def _delete_button_click(self):
        print('delete')
        edit_list = [self.id_edit]
        error = prevalidator.list_validation_call(edit_list, prevalidator.validate_string_edit)
        if error:
            MainWindow.call_error_box(error_text=error)
            return
        error = self.db.delete_person_by_id(int(self.id_edit.text()))
        if error:
            MainWindow.call_error_box(error_text=error)
            return
        MainWindow.call_ok_box(ok_text="Клиент успешно удален.")
        self.id_edit.clear()

    def _fill_clients_table(self):
        table_values = self.db.get_clients()
        headers = table_values["columns"]
        records = table_values["records"]

        self.clients_table.setColumnCount(len(headers))
        self.clients_table.setRowCount(len(records))
        self.clients_table.setHorizontalHeaderLabels(headers)

        if len(records) == 0:
            return
        records = db_data_converter.convert_records(records, headers)
        for i in range(len(records)):
            for j in range(len(records[i])):
                self.clients_table.setItem(i, j, QTableWidgetItem(str(records[i][j])))

    def _change_tab(self, index):
        if index == win_const.CLIENT_LIST_TAB_INDEX:
            self._fill_clients_table()


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
