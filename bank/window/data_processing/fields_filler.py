from PyQt5.QtCore import QDate

# todo: сюда и очиститель полей


def fill_edit(edit, column_name, value):
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
    is_man = False
    is_woman = False
    if value == 0:
        is_man = True
    elif value == 1:
        is_woman = True
    edits['man'].setChecked(is_man)
    edits['woman'].setChecked(is_woman)
