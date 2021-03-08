from enum import Enum


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

    # todo: проработать спец методы для кассы и СФРБ
    # todo: проверять, чтобы номер депозита не было в бд


class Deposit:
    def __init__(self, client_id, deposit_id, contract_number, currency_id, rate, term, start_date):
        self.client_id = client_id
        self.contract_number = contract_number
        self.deposit_id = deposit_id
        self.current_account_id = Deposit.create_account(
            AccountType.PASSIVE, 3014, currency_id, contract_number
        )
        self.credit_account_id = Deposit.create_account(
            AccountType.PASSIVE, 2400, currency_id, contract_number
        )
        self.currency_id = currency_id
        self.rate = rate
        self.term = term
        self.start_date = start_date
        # todo: generate end_date using term

    @staticmethod
    def create_account(account_type, chart_of_accounts_code, currency_id, deposit_number):
        return ClientAccount(account_type, chart_of_accounts_code, currency_id, deposit_number=deposit_number)

    def get_currency_id(self):
        return self.currency_id

    # todo: get accounts info?
        # todo: current
        # todo: credit
        # todo: controller gets info and saves to db

