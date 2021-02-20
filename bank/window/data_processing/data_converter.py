def convert_name(name):
    if not name:
        return name

    return name[0].upper() + name[1:].lower()


def to_upper(string):
    if not string:
        return string

    return string.upper()


def get_names_from_values(values):
    return [None] + [item[1] for item in values] if values else []
