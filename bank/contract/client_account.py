
class ClientAccount:
    def __init__(self, db, account_type, chart_of_accounts, currency_id, deposit_number,
                 is_bdfa=False, is_cash_register=False):
        self.db = db
        self.is_bdfa = is_bdfa
        self.is_cash_register = is_cash_register
        self.debit = 0
        self.credit = 0
        # 0 - active
        # 1 - passive
        # 2 - active-passive
        self.type = account_type
        self.currency_id = currency_id
        self.chart_of_accounts = chart_of_accounts
        self.number = ClientAccount.generate_number(chart_of_accounts, deposit_number)

    @staticmethod
    def generate_number(chart_of_accounts_number, deposit_number):
        deposit_number = "0"*(8 - len(str(deposit_number))) + str(deposit_number)
        account_number = f"{chart_of_accounts_number}{deposit_number}"
        control_digit = sum([int(digit) for digit in account_number]) % 10
        account_number += str(control_digit)
        if len(account_number) != 13:
            raise Exception("Error. Something went wrong in account number generation")

        return account_number

    # todo: функция по увеличению дебита/кредита в зависимости от type
    # todo: геттеры ко всем функциям
    # todo: начислить проценты
    # todo: проработать спец методы для кассы и СФРБ


class Deposit:
    def __init__(self, client_id, deposit_id, contract_number):
        self.client_id = client_id
        self.contract_number = contract_number
        self.deposit_id = deposit_id
        # current_account_id
        # credit_account_id

    def create_account(self):
        pass

    # todo: метод по генерации друх счетов
    # todo: начислить проценты
    # todo: взаимоействие с бд
