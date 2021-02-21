# todo: сюда и очиститель полей


def fill_edit(edit, column_name, value):
    if column_name == "sex":
        # fill radiobutton
        pass
    elif column_name in ["birth_date", "issue_date"]:
        # fill date edit
        pass
    elif column_name in ["passport_number", "monthly_income"]:
        fill_number_edit(edit, value)
    elif column_name == "pension":
        fill_checkbox_edit(edit, value)
    elif column_name in ["marital_status", "disability", "citizenship", "residence_city", "registration_city"]:
        # fill combobox
        pass
    else:
        fill_string_edit(edit, value)


def fill_combobox_edit(edit, value):
    pass


def fill_date_edit(edit, value):
    # todo: узнать, какой тип возвращает бд: datetime или стринг
    pass


def fill_checkbox_edit(edit, value):
    edit.setChecked(value)


def fill_number_edit(edit, value):
    if value is not None:
        edit.setText(str(value))
        return
    edit.setText('')


def fill_string_edit(edit, value):
    edit.setText(value)


def fill_radio_button(edit, value):
    pass
