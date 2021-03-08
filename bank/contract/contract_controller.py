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

    def _load_all_client_account(self):
        pass

    def _transform_from_db_to_class(self):
        pass

    def _get_currency_id_by_name(self, currency_name):
        return self.db.get_currency_id_by_name(currency_name)

    def _get_currency_name_by_id(self, currency_id):
        return self.db.get_currency_name_by_id(currency_id)

    def add_to_cash_register(self, value, currency_id):
        pass

    def sub_from_cash_register(self, value, currency_id):
        pass

    # todo: получить список всех счетов
    # todo: положить на кассу
    # todo: сохранить инфу о счете в бд
    # todo: создать депозит клиенту
    # todo: зачислить из счета на счет
    # todo: зачислить проценты
    # todo: снять с кассы
    # todo: забрать вклад
    # todo: save_account_to_db
