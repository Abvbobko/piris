import bank.contract.client_account as accounts
import bank.contract.constants as const


class ContractController:
    def __init__(self, db):
        self.db = db
        self.bsfa = self._load_bfsas()
        self.cash_register = self._load_cash_registers()

    def _load_bfsas(self):
        pass

    def _load_cash_registers(self):
        pass

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
