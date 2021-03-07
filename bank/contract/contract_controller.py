
class ContractController:
    def __init__(self, db):
        self.db = db

    def _get_currency_id_by_name(self, currency_name):
        return self.db.get_currency_id_by_name(currency_name)

    def _get_currency_name_by_id(self, currency_id):
        return self.db.get_currency_name_by_id(currency_id)
