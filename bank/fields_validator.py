import re
import bank.constants as const
import datetime


def is_match_pattern(pattern, string):
    matched = re.match(pattern, string)
    return bool(matched)


def validate_name(name, field_name="", name_regex=const.NAME_REGEX, min_length=1, max_length=255):
    field_name = f" '{field_name}' " if field_name else " "

    if not name:
        return f"Поле{field_name}не может быть пустым."

    if not is_match_pattern(name_regex, name):
        return f"Поле{field_name}должно состоять только из букв и начинаться с заглавной буквы."

    if len(name) < min_length:
        return f"Поле{field_name}должно быть не меньше чем {min_length} символом."

    if len(name) > max_length:
        return f"Поле{field_name}должно не должно быть длиннее чем {max_length} символов."

    return None


def date_validator(date, field_name="", min_date=None, max_date=None):
    field_name = f" '{field_name}' " if field_name else " "

    if not date:
        return f"Поле{field_name}не должно быть пустым."

    if min_date and date < min_date:
        return f"Поле{field_name}не должно быть раньше {min_date}."

    if max_date and date > max_date:
        return f"Поле{field_name}не должно быть позже {max_date}."

    return None


def radio_button_validator(checked_list, field_name="", can_be_empty=False):
    field_name = f" '{field_name}' " if field_name else " "

    if (True not in checked_list) and (not can_be_empty):
        return f"Поле{field_name}не должно быть пустым."

    return None
