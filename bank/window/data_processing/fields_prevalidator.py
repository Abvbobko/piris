import bank.window.data_processing.fields_validator as validator


def list_validation_call(field_list, validation_func):
    for field in field_list:
        error = validation_func(field)
        if error:
            return error
    return None


def validate_date_edit(edit):
    date = edit.date().toPyDate()
    min_date = edit.minimumDate().toPyDate()
    max_date = edit.maximumDate().toPyDate()
    error = validator.date_validator(
        date=date, field_name=edit.field_name, min_date=min_date, max_date=max_date
    )
    return error


def validate_combobox(combobox):
    error = validator.combobox_validator(
        combobox.currentText(),
        field_name=combobox.field_name
    )
    return error


def validate_string_edit(edit):
    error = validator.string_validator(
        text=edit.text(),
        field_name=edit.field_name,
        mask=edit.mask_regex,
        max_length=edit.maxLength(),
        can_be_empty=edit.can_be_empty
    )
    return error


def validate_checkbox(checkbox):
    error = validator.checkbox_validator(
        checkbox.isChecked(),
        field_name=checkbox.field_name
    )
    return error



