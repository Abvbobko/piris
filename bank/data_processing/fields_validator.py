import re
import string


def is_match_pattern(pattern, text):
    matched = re.match(pattern, text)
    return bool(matched)


def change_field_name(field_name):
    return f' "{field_name}" ' if field_name else " "


def string_validator(text, field_name=None, mask=None, min_length=None, max_length=None, can_be_empty=False):
    field_name = change_field_name(field_name)

    if not text and not can_be_empty:
        return f"Поле{field_name}не может быть пустым."

    if can_be_empty and len(text) == 0:
        return None

    if mask and not is_match_pattern(mask, text):
        return f"Поле{field_name}заполнено некорректно."

    if min_length and len(text) < min_length:
        return f"Поле{field_name}должно быть не меньше чем {min_length} символом."

    if max_length and len(text) > max_length:
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


def passport_id_validator(passport_id, birth_date, sex, field_name=None, length=None, mask=None):
    # man - 0
    # woman - 1
    # field_name = change_field_name(field_name)
    error = string_validator(
        passport_id, field_name=field_name, min_length=length, max_length=length, mask=mask
    )
    if error:
        return error

    field_name = change_field_name(field_name)

    # validate first digit
    century = 1 + birth_date.year//100
    codes = {
        0: {19: 1, 20: 3, 21: 5},
        1: {19: 2, 20: 4, 21: 6}
    }
    digit = codes[sex][century]

    # validate 1 digit
    if int(passport_id[0]) != digit:
        return f"Первая цифра поля {field_name} некорректна."

    # validate birth date digits (2-8)
    str_birth_date = birth_date.strftime("%d%m%y")
    if str_birth_date != passport_id[1:7]:
        return f"Перепроверьте цифры номер 2-7 поля {field_name}."

    # validate control digit

    func = [7, 3, 1]
    control_digit = 0
    for i in range(len(passport_id) - 1):
        if passport_id[i].isdigit():
            number = int(passport_id[i])
        else:
            number = string.ascii_uppercase.index(passport_id[i]) + 10
        control_digit += number * func[i % len(func)]

    control_digit %= 10

    if control_digit != int(passport_id[-1]):
        return f"Контрольная цифра поля {field_name} некорректна."

    return None
