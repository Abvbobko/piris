import datetime


def convert_sex_to_db_form(m, w):
    """Convert sex to the int format
    0 - man
    1 - woman
    :param m: bool - True if man
    :param w: bool - True if woman
    :return: int - sex code
    """
    if m and w:
        raise Exception("Can't be two sexes at the same time.")
    if m:
        return 0
    return 1


def convent_sex_from_db_form(sex):
    if sex == 0:
        return 'мужской'
    elif sex == 1:
        return 'женский'
    return None


def convert_date_to_the_db_form(date, date_format="%Y-%m-%d"):
    return datetime.date.strftime(date, date_format)


def get_optional_value(edit):
    return edit.text() if edit.text() else None


def sort_records_by_surname(records, surname_index):
    sort_records = list(records)
    sort_records.sort(key=lambda x: x[surname_index])
    return tuple(sort_records)


def convert_pension_from_db_form(pension):
    if pension == 0:
        return 'нет'
    elif pension == 1:
        return 'да'
    return None


def convert_record_from_db_form(record, header):
    converted_record = []
    for i in range(len(record)):
        if record[i] is None:
            converted_record.append("-")
        elif header[i] == "sex":
            converted_record.append(convent_sex_from_db_form(record[i]))
        elif header[i] == "pension":
            converted_record.append(convert_pension_from_db_form(record[i]))
        else:
            converted_record.append(record[i])

    return tuple(converted_record)


def convert_records(records, header):
    records = sort_records_by_surname(records, surname_index=header.index("surname"))
    converted_records = []
    for record in records:
        converted_records.append(convert_record_from_db_form(record, header))

    return tuple(converted_records)


