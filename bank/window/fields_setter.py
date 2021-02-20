from PyQt5 import QtGui
from PyQt5.QtCore import QRegExp, QDate

import bank.window.data_processing.data_converter as data_converter


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




