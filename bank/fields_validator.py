import re
import bank.constants as const


def is_match_pattern(pattern, string):
    matched = re.match(pattern, string)
    return bool(matched)


def validate_name(name, field_name="", name_regex=const.NAME_REGEX, min_length=1, max_length=255, can_be_empty=False):

    if field_name:
        field_name = f" '{field_name}' "

    if not name and not can_be_empty:
        return False, f"Поле{field_name}не может быть пустым."

    if not is_match_pattern(name_regex, name):
        return False, f"Поле{field_name}должно состоять только из букв и начинаться с заглавной буквы."

    if len(name) < min_length:
        return False, f"Поле{field_name}должно быть не меньше чем {min_length} символом."

    if len(name) > max_length:
        return False, f"Поле{field_name}должно не должно быть длиннее чем {max_length} символов."

    return True, None


