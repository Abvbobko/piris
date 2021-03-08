import bank.contract.client_account as accounts
import bank.contract.constants as const
from bank.db.db_controller import DBController


class ContractController:
    def __init__(self, db: DBController):
        self.db = db
        self.bdfa = self._load_bdfas()
        self.cash_register = self._load_cash_registers()

    @staticmethod
    def _convert_account_to_dict(record, header):
        result = {}
        for i in range(len(header)):
            result[header[i]] = record[i]
        return result

    @staticmethod
    def _load_unique_currency_accounts(load_db_func, account_type, chart_of_accounts_number):
        """:return: {
                    currency_id: entity,
                    ...
                }
        """
        raw_accounts_with_header = load_db_func()
        header = raw_accounts_with_header["columns"]
        raw_accounts = raw_accounts_with_header["records"]

        result_dict = {}

        for account_record in raw_accounts:
            account_record_dict = ContractController._convert_account_to_dict(account_record, header)
            currency_id = account_record_dict["currency_id"]
            result_dict[currency_id] = accounts.ClientAccount(
                account_type, chart_of_accounts_number, currency_id,
                start_debit=account_record_dict["debit"], start_credit=account_record_dict["credit"],
                account_number=account_record_dict["number"]
            )
        return result_dict

    def _load_bdfas(self):
        return ContractController._load_unique_currency_accounts(
            accounts.AccountType.PASSIVE, const.BFSA_NUMBER, self.db.get_bdfas
        )

    def _load_cash_registers(self):
        return ContractController._load_unique_currency_accounts(
            accounts.AccountType.ACTIVE, const.CASH_REGISTER_NUMBER, self.db.get_cash_registers
        )

    def _transform_from_db_to_class(self):
        pass

    def _get_currency_id_by_name(self, currency_name):
        return self.db.get_currency_id_by_name(currency_name)

    def _get_currency_name_by_id(self, currency_id):
        return self.db.get_currency_name_by_id(currency_id)

    def _add_to_cash_register(self, value, currency_id):
        self.cash_register[currency_id].add_amount(value)

    def _sub_from_cash_register(self, value, currency_id):
        self.cash_register[currency_id].sub_amount(value)

    @staticmethod
    def transfer_between_accounts(account_a: accounts.ClientAccount, account_b: accounts.ClientAccount, amount):
        """Передать сумму от a к b"""
        account_a.sub_amount(amount)
        account_b.add_amount(amount)

    @staticmethod
    def _convert_account_to_db_form(account: accounts.ClientAccount, is_bdfa=False, is_cash_register=False):
        return {
            "is_bdfa": is_bdfa,
            "is_cash_register": is_cash_register,
            "debit": account.get_debit(),
            "credit": account.get_credit(),
            "type": account.get_type(),
            "currency_id": account.get_currency_id(),
            "chart_of_accounts": account.get_chart_of_accounts_number(),
            "account_number": account.get_account_number()
        }

    def save_deposit_to_db(self, deposit):
        current_account = deposit.get_current_account()
        credit_account = deposit.get_credit_account()
        current_account_dict = ContractController._convert_account_to_db_form(current_account)
        credit_account_dict = ContractController._convert_account_to_db_form(credit_account)
        error = self.db.insert_account(**current_account_dict)
        if error:
            return error
        current_account_id = self.db.get_last_inserted_id()

        error = self.db.insert_account(**credit_account_dict)
        if error:
            return error
        credit_account_id = self.db.get_last_inserted_id()
        # todo: method to save|update deposit in db controller



    def create_deposit(self, client_id, contract_number, currency_id,
                       amount, term, deposit_program_id, rate, start_date):
        deposit = accounts.Deposit(
            client_id=client_id,
            deposit_id=deposit_program_id,
            contract_number=contract_number,
            currency_id=currency_id,
            rate=rate,
            term=term,
            start_date=start_date
        )

        # todo: сделать метод по сохранению депозита
            # todo: метод по созранению счета
        pass

    # todo: создать депозит клиенту
    # todo: зачислить проценты
    # todo: забрать вклад
    # todo: save_account_to_db

