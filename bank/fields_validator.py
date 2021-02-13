import re
import bank.constants as const
import datetime


def is_match_pattern(pattern, string):
    matched = re.match(pattern, string)
    return bool(matched)


def change_field_name(field_name):
    return f' "{field_name}" ' if field_name else " "


def validate_name(name, field_name=None, name_regex=const.NAME_REGEX, min_length=1, max_length=255):
    field_name = change_field_name(field_name)

    if not name:
        return f"Поле{field_name}не может быть пустым."

    if not is_match_pattern(name_regex, name):
        return f"Поле{field_name}должно состоять только из букв и начинаться с заглавной буквы."

    if len(name) < min_length:
        return f"Поле{field_name}должно быть не меньше чем {min_length} символом."

    if len(name) > max_length:
        return f"Поле{field_name}должно не должно быть длиннее чем {max_length} символов."

    return None


def date_validator(date, field_name=None, min_date=None, max_date=None):
    field_name = change_field_name(field_name)

    if not date:
        return f"Поле{field_name}не должно быть пустым."

    if min_date and date < min_date:
        return f"Поле{field_name}не должно быть раньше {min_date}."

    if max_date and date > max_date:
        return f"Поле{field_name}не должно быть позже {max_date}."

    return None


def radio_button_validator(checked_list, field_name=None, can_be_empty=False):
    field_name = change_field_name(field_name)

    if (True not in checked_list) and (not can_be_empty):
        return f"Поле{field_name}не должно быть пустым."

    return None


def combobox_validator(value, field_name=None, can_be_empty=False):
    field_name = change_field_name(field_name)

    if not value and not can_be_empty:
        return f"Поле{field_name}не должно быть пустым."

    return None


def checkbox_validator(state, field_name=None, is_tristate=False):
    field_name = change_field_name(field_name)

    if is_tristate and state not in [0, 1, 2]:
        return f"У поля{field_name}некорректное значение."
    elif state not in [True, False]:
        return f"У поля{field_name}некорректное значение."

    return None
