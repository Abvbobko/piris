def convert_name(name):
    if not name:
        return name

    return name[0].upper() + name[1:].lower()


def to_upper(string):
    if not string:
        return string

    return string.upper()


def add_none_state_to_list(values):
    if None not in values:
        return [None] + values
    return values

