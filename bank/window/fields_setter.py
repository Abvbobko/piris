from PyQt5 import QtGui
from PyQt5.QtCore import QRegExp, QDate
import bank.window.constants.field_constants as field_const
import bank.window.data_processing.data_converter as data_converter
import datetime


def set_deposit_fields(self):
    deposits = self.db.get_deposits()
    set_combobox(self.deposit_combobox, deposits, "Депозит")
    set_string_edit(
        self.contract_number_edit, field_name="Номер договора", mask_regex=field_const.CONTRACT_NUMBER_MASK,
        max_length=field_const.CONTRACT_NUMBER_MAX_LENGTH, can_be_empty=False
    )

    set_string_edit(
        self.deposit_number_edit, field_name="Номер договора", mask_regex=field_const.CONTRACT_NUMBER_MASK,
        max_length=field_const.CONTRACT_NUMBER_MAX_LENGTH, can_be_empty=False
    )

    set_string_edit(
        self.client_id_edit, field_name="id клиента", mask_regex=field_const.ID_MASK,
        max_length=field_const.ID_MAX_LENGTH, can_be_empty=False
    )

    set_string_edit(
        self.client_id_edit, field_name="id клиента", mask_regex=field_const.ID_MASK,
        max_length=field_const.ID_MAX_LENGTH, can_be_empty=False
    )

    set_string_edit(
        self.deposit_client_id_edit, field_name="id клиента", mask_regex=field_const.ID_MASK,
        max_length=field_const.ID_MAX_LENGTH, can_be_empty=False
    )

def set_is_deposit_revocable(edit, value):
    if value:
        set_text_to_edit(edit, "да")
    else:
        set_text_to_edit(edit, "нет")


def set_all_fields(self):
    """Set all parameters to edits"""
    cities = self.db.get_cities()
    citizenships = self.db.get_citizenships()
    marital_statuses = self.db.get_marital_status()
    disabilities = self.db.get_disabilities()
    # set all comboboxes
    set_combobox(self.residence_city_combobox, cities, "Город факт. проживания")
    set_combobox(self.registration_city_combobox, cities, "Город прописки")
    set_combobox(self.citizenship_combobox, citizenships, "Гражданство")
    set_combobox(self.disability_combobox, disabilities, "Инвалидность")
    set_combobox(self.marital_status_combobox, marital_statuses, "Семейное положение")

    # add surname, name and patronymic edit filters
    set_string_edit(
        self.surname_edit, field_name="Фамилия", mask_regex=field_const.NAME_REGEX,
        max_length=field_const.MAX_NAME_LENGTH, can_be_empty=False
    )

    set_string_edit(
        self.name_edit, field_name="Имя", mask_regex=field_const.NAME_REGEX,
        max_length=field_const.MAX_NAME_LENGTH, can_be_empty=False
    )

    set_string_edit(
        self.patronymic_edit, field_name="Отчество", mask_regex=field_const.NAME_REGEX,
        max_length=field_const.MAX_NAME_LENGTH, can_be_empty=False
    )

    # add dates constraints
    today = datetime.date.today()
    min_date = field_const.MIN_DATE
    set_date_edit(self.birth_date_edit, min_date, max_date=today, field_name="Дата рождения")
    set_date_edit(self.issue_date_edit, min_date, max_date=today, field_name="Дата выдачи")

    # add constraints for the string edits
    set_string_edit(
        self.passport_series_edit, field_name="Серия паспорта", mask_regex=field_const.PASSPORT_SERIES_MASK,
        max_length=field_const.MAX_PASSPORT_SERIES_LENGTH, can_be_empty=False
    )

    set_string_edit(
        self.issued_by_edit, field_name="Кем выдан", mask_regex=None,
        max_length=field_const.MAX_INFO_STRING_LENGTH, can_be_empty=False
    )

    set_string_edit(
        self.birth_place_edit, field_name="Место рождения", mask_regex=None,
        max_length=field_const.MAX_INFO_STRING_LENGTH, can_be_empty=False
    )

    set_string_edit(
        self.residence_address_edit, field_name="Адрес факт. проживания", mask_regex=None,
        max_length=field_const.MAX_INFO_STRING_LENGTH, can_be_empty=False
    )

    set_string_edit(
        self.email_edit, field_name="Email", mask_regex=None,
        max_length=field_const.MAX_INFO_STRING_LENGTH, can_be_empty=True
    )

    # phone number validators
    placeholder = field_const.HOME_PHONE_PLACEHOLDER
    set_string_edit(
        self.home_phone_edit, field_name="Телефон домашний", mask_regex=field_const.HOME_PHONE_MASK,
        max_length=len(placeholder), can_be_empty=True, placeholder=placeholder
    )

    placeholder = field_const.MOBILE_PHONE_PLACEHOLDER
    set_string_edit(
        self.mobile_phone_edit, field_name="Телефон мобильный", mask_regex=field_const.MOBILE_PHONE_MASK,
        max_length=field_const.MOBILE_PHONE_LENGTH, can_be_empty=True, placeholder=placeholder
    )

    # set passport number and id validators
    set_string_edit(
        self.passport_number_edit, field_name="Номер паспорта", mask_regex=field_const.PASSPORT_NUMBER_MASK,
        max_length=field_const.PASSPORT_NUMBER_LENGTH, can_be_empty=False
    )

    set_string_edit(
        self.identification_number_edit, field_name="Идентификационный номер",
        mask_regex=field_const.PASSPORT_ID_MASK,
        max_length=field_const.PASSPORT_ID_LENGTH, can_be_empty=False
    )

    set_string_edit(
        self.monthly_income_edit, field_name="Ежемесячный доход", mask_regex=field_const.INCOME_MASK,
        max_length=field_const.INCOME_MAX_LENGTH, can_be_empty=True
    )

    self.pension_checkbox.field_name = "Пенсионер"
    self.m_radio_button.field_name = "Пол"
    self.w_radio_button.field_name = "Пол"


def set_text_to_edit(edit, text, transform_func=None):
    if transform_func:
        text = transform_func(text)
    edit.setText(text)


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


def set_combobox(combobox, db_values, field_name):
    db_values = data_converter.convert_list_to_str_list(db_values)
    db_values_names = data_converter.add_none_state_to_list(db_values)
    combobox.db_values = db_values
    combobox.clear()
    combobox.addItems(db_values_names)
    combobox.field_name = field_name


def set_date_edit(date_edit, min_date, max_date, field_name):
    min_date_qdate = QDate(min_date.year, min_date.month, min_date.day)
    max_date_qdate = QDate(max_date.year, max_date.month, max_date.day)
    date_edit.setMinimumDate(min_date_qdate)
    date_edit.setMaximumDate(max_date_qdate)
    date_edit.field_name = field_name
