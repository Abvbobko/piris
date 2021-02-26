import string
import random
import datetime
import calendar


def generate(sex=0, start_year=1950, end_year=datetime.date.today().year):
    # man - 0
    # woman - 1

    birth_year = random.randint(start_year, end_year)
    birth_month = random.randint(1, 12)
    month_range = calendar.monthrange(birth_year, birth_month)
    birth_day = random.randint(1, month_range[1])
    birth_date = datetime.date(birth_year, birth_month, birth_day)
    str_birth_date = birth_date.strftime("%d%m%y")

    century = 1 + birth_date.year // 100
    codes = {
        0: {19: 1, 20: 3, 21: 5},
        1: {19: 2, 20: 4, 21: 6}
    }
    first_digit = codes[sex][century]

    region_code = random.choice("ABCHKEM")

    digits = "0123456789"
    order_number = "000"
    while order_number == "000":
        order_number = random.choice(digits) + random.choice(digits) + random.choice(digits)

    citizenship = random.choice(['PB', 'BA', 'BI'])

    passport_id = f"{first_digit}{str_birth_date}{region_code}{order_number}{citizenship}"

    func = [7, 3, 1]
    control_digit = 0
    for i in range(len(passport_id)):
        if passport_id[i].isdigit():
            number = int(passport_id[i])
        else:
            number = string.ascii_uppercase.index(passport_id[i]) + 10

        control_digit += number * func[i % len(func)]

    control_digit %= 10
    passport_id += str(control_digit)

    return passport_id


print(generate(0))
