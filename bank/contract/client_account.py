from enum import Enum
import datetime
import dateutil.relativedelta as relativedelta
import calendar


class AccountType(Enum):
    ACTIVE = 0
    PASSIVE = 1
    ACTIVE_PASSIVE = 2


class ClientAccount:
    def __init__(self, account_type, chart_of_accounts, currency_id, start_debit=0, start_credit=0,
                 account_number=None, deposit_number=None, account_id=None):
        self.debit = start_debit
        self.credit = start_credit
        self.type = account_type
        self.currency_id = currency_id
        self.chart_of_accounts = chart_of_accounts
        self.number = account_number if account_number \
            else ClientAccount.generate_number(chart_of_accounts, deposit_number)

        self.account_id = account_id

    @staticmethod
    def generate_number(chart_of_accounts_number, deposit_number):
        deposit_number = "0"*(8 - len(str(deposit_number))) + str(deposit_number)
        account_number = f"{chart_of_accounts_number}{deposit_number}"
        control_digit = sum([int(digit) for digit in account_number]) % 10
        account_number += str(control_digit)
        if len(account_number) != 13:
            raise Exception("Error. Something went wrong in account number generation")

        return account_number

    def add_amount(self, amount):
        if self.type == AccountType.ACTIVE:
            self.debit += amount
        elif self.type == AccountType.PASSIVE:
            self.credit += amount
        print(f'Зачислено на {self.number}')

    def sub_amount(self, amount):
        if self.type == AccountType.ACTIVE:
            self.credit += amount
        elif self.type == AccountType.PASSIVE:
            self.debit += amount
        print(f'Вычтено с {self.number}')

    def get_currency_id(self):
        return self.currency_id

    def get_debit(self):
        return self.debit

    def get_credit(self):
        return self.credit

    def get_saldo(self):
        if self.type == AccountType.ACTIVE:
            return self.debit - self.credit
        elif self.type == AccountType.PASSIVE:
            return self.credit - self.debit

    def get_type(self):
        return self.type.value

    def get_type_readable(self):
        if self.type == AccountType.ACTIVE:
            return "Активный"
        elif self.type == AccountType.PASSIVE:
            return "Пассивный"
        return "Активно-Пассивный"

    def get_chart_of_accounts_number(self):
        return self.chart_of_accounts

    def get_account_number(self):
        return self.number

    def get_account_id(self):
        return self.account_id

    def set_account_id(self, value):
        self.account_id = value


class Deposit:
    def __init__(self, client_id, deposit_id, contract_number, currency_id, rate, term, start_date, is_revocable,
                 deposit_name, current_account=None, credit_account=None, end_date=None):
        """Класс депозита
        :param client_id: id клиента (надо для таблицы)
        :param deposit_id: id тарифа (со своим планом)
        :param contract_number: номер договора (вводится в ui)
        :param currency_id: id валюты
        :param rate: ставка
        :param deposit_name: название депозита (пример "Семейный")
        :param term: срок (в месяцах)
        :param start_date: дата заключения договора (с каких пор начинает капать вклад)
        :param current_account: текущий счет (если есть)
        :param credit_account: процентный счет (если есть)
        """
        self.client_id = client_id
        self.contract_number = contract_number
        self.deposit_id = deposit_id
        self.is_revocable = is_revocable
        self.deposit_name = deposit_name
        self.current_account = current_account if current_account else Deposit.create_account(
            AccountType.PASSIVE, 3014, currency_id, contract_number
        )
        self.credit_account = credit_account if credit_account else Deposit.create_account(
            AccountType.PASSIVE, 2400, currency_id, contract_number
        )
        self.currency_id = currency_id
        self.rate = rate
        self.term = term
        self.start_date = start_date
        self.end_date = end_date if end_date else Deposit.calculate_end_date(start_date, term)

    @staticmethod
    def add_months(source_date, months):
        month = source_date.month - 1 + months
        year = source_date.year + month // 12
        month = month % 12 + 1
        day = min(source_date.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

    @staticmethod
    def calculate_end_date(start_date, term):
        return Deposit.add_months(start_date, term)

    @staticmethod
    def create_account(account_type, chart_of_accounts_code, currency_id, deposit_number):
        return ClientAccount(account_type, chart_of_accounts_code, currency_id, deposit_number=deposit_number)

    def get_currency_id(self):
        return self.currency_id

    def get_current_account(self):
        return self.current_account

    def get_credit_account(self):
        return self.credit_account

    def get_client_id(self):
        return self.client_id

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_deposit_id(self):
        return self.deposit_id

    def get_contract_number(self):
        return self.contract_number

    def _is_revocable_readable_form(self):
        return "Да" if self.is_revocable else "Нет"

    def get_term(self):
        return self.term

    def _account_to_table_form(self, account, account_name, currency):
        return [
            self.contract_number,
            account_name,
            account.get_account_number(),
            self._is_revocable_readable_form(),
            account.get_type_readable(),
            account.get_debit(),
            account.get_credit(),
            account.get_saldo(),
            self.get_start_date(),
            self.get_end_date(),
            self.get_term(),
            currency,
            self.deposit_name
        ]

    def get_table_form(self, currency):
        return [
            self._account_to_table_form(self.current_account, "текущий", currency),
            self._account_to_table_form(self.credit_account, "кредитный", currency)
        ]

    @staticmethod
    def get_table_header():
        return ["Номер договора", "Счет", "Номер счета", "Отзывной", "Тип", "Дебит", "Кредит", "Сальдо",
                "Дата начала", "Дата окончания", "Ставка %", "Валюта", "Название тарифа"]

    def set_end_date(self, new_end_date):
        self.end_date = new_end_date

    def get_is_revocable(self):
        return self.is_revocable

