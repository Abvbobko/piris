from enum import Enum
import datetime
import dateutil.relativedelta as relativedelta


class AccountType(Enum):
    ACTIVE = 0
    PASSIVE = 1
    ACTIVE_PASSIVE = 2


class ClientAccount:
    def __init__(self, account_type, chart_of_accounts, currency_id, start_debit=0, start_credit=0,
                 account_number=None, deposit_number=None):
        self.debit = start_debit
        self.credit = start_credit
        self.type = account_type
        self.currency_id = currency_id
        self.chart_of_accounts = chart_of_accounts
        self.number = account_number if account_number \
            else ClientAccount.generate_number(chart_of_accounts, deposit_number)

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

    def get_chart_of_accounts_number(self):
        return self.chart_of_accounts

    def get_account_number(self):
        return self.number


class Deposit:
    def __init__(self, client_id, deposit_id, contract_number, currency_id, rate, term, start_date,
                 current_account=None, credit_account=None):
        """Класс депозита
        :param client_id: id клиента (надо для таблицы)
        :param deposit_id: id тарифа (со своим планом)
        :param contract_number: номер договора (вводится в ui)
        :param currency_id: id валюты
        :param rate: ставка
        :param term: срок (в месяцах)
        :param start_date: дата заключения договора (с каких пор начинает капать вклад)
        :param current_account: текущий счет (если есть)
        :param credit_account: процентный счет (если есть)
        """
        self.client_id = client_id
        self.contract_number = contract_number
        self.deposit_id = deposit_id
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
        self.end_date = Deposit.calculate_end_date(start_date, term)

    @staticmethod
    def calculate_end_date(start_date, term):
        return start_date + relativedelta.relativedelta(month=term)

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
