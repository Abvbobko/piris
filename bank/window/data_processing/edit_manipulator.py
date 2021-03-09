from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDateEdit, QComboBox, QCheckBox, QRadioButton
from bank.window.constants.field_constants import DEFAULT_DATE
from bank.window.data_processing import db_data_converter


def uncheck_edit(edit):
    edit.setChecked(False)


def clear_combobox(edit):
    edit.setCurrentIndex(0)


def clear_date(edit, default_date=DEFAULT_DATE):
    fill_date_edit(edit, default_date)


def clear_edit(edit):
    """Clear edit according to the edit type"""
    edit_type = type(edit)
    if edit_type == list:
        for one_edit in edit:
            clear_edit(one_edit)
    elif edit_type == dict:
        for one_edit in edit.values():
            clear_edit(one_edit)
    elif edit_type == QRadioButton or edit_type == QCheckBox:
        uncheck_edit(edit)
    elif edit_type == QComboBox:
        clear_combobox(edit)
    elif edit_type == QDateEdit:
        clear_date(edit)
    else:
        edit.clear()


def fill_edit(edit, column_name, value):
    """Fill edit according to the column name"""
    if column_name == "sex":
        fill_radio_button(edit, value)
    elif column_name in ["birth_date", "issue_date"]:
        fill_date_edit(edit, value)
    elif column_name in ["passport_number", "monthly_income"]:
        fill_number_edit(edit, value)
    elif column_name == "pension":
        fill_checkbox_edit(edit, value)
    elif column_name in ["marital_status", "disability", "citizenship", "residence_city", "registration_city"]:
        fill_combobox_edit(edit, value)
    else:
        fill_string_edit(edit, value)


def fill_combobox_edit(combobox, value):
    for i in range(combobox.count()):
        if combobox.itemText(i) == value:
            combobox.setCurrentIndex(i)
            break


def fill_date_edit(edit, value):
    date = QDate(value.year, value.month, value.day)
    edit.setDate(date)


def fill_checkbox_edit(edit, value):
    edit.setChecked(value)


def fill_number_edit(edit, value):
    if value is not None:
        edit.setText(str(value))
        return
    edit.setText('')


def fill_string_edit(edit, value):
    edit.setText(value)


def fill_radio_button(edits, value):
    """Convert 0/1 value to radio button format"""
    is_man = False
    is_woman = False
    if value == 0:
        is_man = True
    elif value == 1:
        is_woman = True
    edits['man'].setChecked(is_man)
    edits['woman'].setChecked(is_woman)


def get_current_value(edit, column_name):
    """Get value from edit according to the column name"""
    if column_name == "sex":
        value = get_sex_value(edit)
    elif column_name in ["birth_date", "issue_date"]:
        value = get_date_value(edit)
    elif column_name == "passport_number":
        value = get_int_value(edit)
    elif column_name in ["home_phone", "mobile_phone", "email"]:
        value = get_optional_value(edit)
    elif column_name == "monthly_income":
        value = get_optional_float_value(edit)
    elif column_name == "pension":
        value = get_checkbox_int_value(edit)
    elif column_name in ["marital_status", "disability", "citizenship", "residence_city", "registration_city"]:
        value = get_combobox_value(edit)
    else:
        value = get_str_value(edit)
    return value


def get_value_from_radio_button_list(radio_buttons):
    """Get isChecked for all radio buttons in list"""
    return [radio_button.isChecked() for radio_button in radio_buttons]


def get_sex_value(sex_dict):
    """Get values from list of radio buttons and convert to int"""
    sex_values = get_value_from_radio_button_list(sex_dict.values())
    return db_data_converter.convert_sex_to_db_form(sex_values[0], sex_values[1])


def get_date_value(date_edit):
    """Convert date (for date edit)"""
    return db_data_converter.convert_date_to_the_db_form(date_edit.date().toPyDate())


def get_int_value(edit):
    """Convert str value to int (for line edit)"""
    return int(edit.text())


def get_optional_value(edit):
    return db_data_converter.get_optional_value(edit)


def get_optional_float_value(edit):
    """Get optional value and if it's set -> return floated value"""
    value = db_data_converter.get_optional_value(edit)
    return float(value) if value else None


def get_checkbox_int_value(edit):
    """Convert checkbox bool value to int"""
    return int(edit.isChecked())


def get_combobox_value(edit):
    """Get current text from combobox"""
    return edit.currentText()


def get_str_value(edit):
    """Get text from simple line edit"""
    return edit.text()


def get_mapper(self):
    return {
        "surname": self.surname_edit,
        "first_name": self.name_edit,
        "patronymic": self.patronymic_edit,
        "birth_date": self.birth_date_edit,
        "sex": {'man': self.m_radio_button, 'woman': self.w_radio_button},
        "passport_series": self.passport_series_edit,
        "passport_number": self.passport_number_edit,
        "issued_by": self.issued_by_edit,
        "issue_date": self.issue_date_edit,
        "identification_number": self.identification_number_edit,
        "birth_place": self.birth_place_edit,
        "residence_address": self.residence_address_edit,
        "home_phone": self.home_phone_edit,
        "mobile_phone": self.mobile_phone_edit,
        "email": self.email_edit,
        "pension": self.pension_checkbox,
        "monthly_income": self.monthly_income_edit,
        "marital_status": self.marital_status_combobox,
        "disability": self.disability_combobox,
        "citizenship": self.citizenship_combobox,
        "residence_city": self.residence_city_combobox,
        "registration_city": self.registration_city_combobox
    }


def get_deposit_mapper(self):
    return {
        "contract_number": self.contract_number_edit,
        "deposit": self.deposit_combobox,
        "client_id": self.client_id_edit,
        "is_revocable": self.is_revocable_edit,
        "currency": self.currency_combobox,
        "rate": self.rate_edit,
        "term": self.term_combobox,
        "deposit_program_start": self.deposit_program_period_from_edit,
        "deposit_program_end": self.deposit_program_period_to_edit,
        "min_amount": self.min_amount_edit,
        "max_amount": self.max_amount_edit,
        "amount": self.amount_edit
    }