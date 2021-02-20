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


def convert_date_to_the_db_form(date, date_format="%Y-%m-%d"):
    return datetime.date.strftime(date, date_format)


def get_optional_value(edit):
    return edit.text() if edit.text() else None





