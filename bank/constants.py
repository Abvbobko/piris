import datetime

WIN_WIDTH = 600
WIN_HEIGHT = 400
WIN_TITLE = "BANK"

MODES = ["Добавление", "Редактирование", "Удаление"]
CURRENT_MODE = 0

NAME_REGEX = "[А-Яа-яA-Za-z]+"
MAX_NAME_LENGTH = 255

MIN_DATE = datetime.date(1900, 1, 1)

MAX_PASSPORT_SERIES_LENGTH = 2
PASSPORT_SERIES_MASK = "[A-Za-z]+"

MAX_INFO_STRING_LENGTH = 255


