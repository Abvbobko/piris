import bank.contract.client_account as accounts
import bank.contract.constants as const
from bank.db.db_controller import DBController
from calendar import monthrange
import datetime


class ContractController:
    def __init__(self, db: DBController):
        self.db = db
        self.bdfa = self._load_bdfas()
        self.cash_register = self._load_cash_registers()
        self.log_file = const.LOG_FILE_PATH

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
                account_number=account_record_dict["number"], account_id=account_record_dict["id"]
            )
        return result_dict

    def _load_bdfas(self):
        return ContractController._load_unique_currency_accounts(
            self.db.get_bdfas, accounts.AccountType.PASSIVE, const.BFSA_NUMBER
        )

    def _load_cash_registers(self):
        return ContractController._load_unique_currency_accounts(
            self.db.get_cash_registers, accounts.AccountType.ACTIVE, const.CASH_REGISTER_NUMBER
        )

    def _transform_from_db_to_class(self):
        pass

    def _get_currency_id_by_name(self, currency_name):
        return self.db.get_currency_id_by_name(currency_name)

    def _get_currency_name_by_id(self, currency_id):
        return self.db.get_currency_name_by_id(currency_id)

    def _log_cash_register_transact(self, log_file, date, currency_id, amount, way="to"):
        with open(log_file, 'a') as f:
            f.write(f"date: {date}, {way}: {self.cash_register[currency_id].get_account_number()}, " +
                    f"amount: {amount}\n")

    def _add_to_cash_register(self, value, currency_id, log_file, current_date):
        self._log_cash_register_transact(self.log_file, current_date, currency_id, value, "to")
        self.cash_register[currency_id].add_amount(value)

    def _sub_from_cash_register(self, value, currency_id, log_file, current_date):
        self._log_cash_register_transact(self.log_file, current_date, currency_id, value, "from")
        self.cash_register[currency_id].sub_amount(value)

    @staticmethod
    def _log_transfer(log_file, date, account_from_number, account_to_number, amount):
        with open(log_file, 'a') as f:
            f.write(f"date: {date}, from: {account_from_number}," +
                    f" to: {account_to_number}, amount: {amount}\n")

    @staticmethod
    def transfer_between_accounts(account_a: accounts.ClientAccount, account_b: accounts.ClientAccount,
                                  amount, log_file, date):
        """Передать сумму от a к b"""
        ContractController._log_transfer(log_file, date,
                                         account_a.get_account_number(), account_b.get_account_number(),
                                         amount)
        account_a.sub_amount(amount)
        account_b.add_amount(amount)

    @staticmethod
    def _convert_account_to_db_form(account: accounts.ClientAccount, is_bdfa=False, is_cash_register=False):
        return {
            "is_bdfa": is_bdfa,
            "is_cash_register": is_cash_register,
            "debit": account.get_debit(),
            "credit": account.get_credit(),
            "account_type": account.get_type(),
            "currency_id": account.get_currency_id(),
            "chart_of_accounts_number": account.get_chart_of_accounts_number(),
            "account_number": account.get_account_number()
        }

    @staticmethod
    def _convert_deposit_to_db_form(deposit: accounts.Deposit, current_id, credit_id):
        return {
            "client_id": deposit.get_client_id(),
            "current_account": current_id,
            "credit_account": credit_id,
            "contract_number": deposit.get_contract_number(),
            "deposit_program_id": deposit.get_deposit_id(),
            "deposit_start_date": deposit.get_start_date(),
            "deposit_end_date": deposit.get_end_date()
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
        current_account.set_account_id(current_account_id)
        error = self.db.insert_account(**credit_account_dict)
        if error:
            return error
        credit_account_id = self.db.get_last_inserted_id()
        credit_account.set_account_id(credit_account_id)

        deposit_dict = ContractController._convert_deposit_to_db_form(deposit, current_account_id, credit_account_id)
        error = self.db.insert_deposit(**deposit_dict)
        if error:
            return error
        return None

    def update_account_in_db(self, account: accounts.ClientAccount, is_bdfa=False, is_cash_register=False):
        account_id = account.get_account_id()
        if account_id:
            account_params = ContractController._convert_account_to_db_form(account, is_bdfa, is_cash_register)
            self.db.insert_account(update_mode=True, account_id=account.get_account_id(), **account_params)
        else:
            print("This account doesn't have account_id")

    def create_deposit(self, client_id, contract_number, currency_id,
                       amount, term, deposit_program_id, rate, start_date, is_revocable, deposit_name):
        deposit = accounts.Deposit(
            client_id=client_id,
            deposit_id=deposit_program_id,
            contract_number=contract_number,
            currency_id=currency_id,
            rate=rate,
            term=term,
            start_date=start_date,
            deposit_name=deposit_name,
            is_revocable=is_revocable
        )
        error = self.save_deposit_to_db(deposit)
        if error:
            return error
        self._add_to_cash_register(amount, currency_id, self.log_file, deposit.start_date)
        current_account = deposit.get_current_account()
        self.transfer_between_accounts(self.cash_register[currency_id], current_account, amount,
                                       self.log_file, start_date)
        self.transfer_between_accounts(current_account, self.bdfa[currency_id], amount,
                                       self.log_file, start_date)
        self.update_account_in_db(self.bdfa[currency_id], is_bdfa=True)
        self.update_account_in_db(self.cash_register[currency_id], is_cash_register=True)
        self.update_account_in_db(current_account)

    def create_credit(self, client_id, contract_number, currency_id,
                      amount, term, deposit_program_id, rate, start_date, is_revocable, deposit_name):
        credit = accounts.Deposit(
            client_id=client_id,
            deposit_id=deposit_program_id,
            contract_number=contract_number,
            currency_id=currency_id,
            rate=rate,
            term=term,
            start_date=start_date,
            deposit_name=deposit_name,
            is_revocable=is_revocable,
            is_credit=True
        )
        error = self.save_deposit_to_db(credit)
        if error:
            return error

        current_account = credit.get_current_account()
        self.transfer_between_accounts(self.bdfa[currency_id], current_account, amount,
                                       self.log_file, start_date)
        self.transfer_between_accounts(current_account, self.cash_register[currency_id],amount,
                                       self.log_file, start_date)

        self._sub_from_cash_register(amount, currency_id, self.log_file, credit.start_date)

        self.update_account_in_db(self.bdfa[currency_id], is_bdfa=True)
        self.update_account_in_db(self.cash_register[currency_id], is_cash_register=True)
        self.update_account_in_db(current_account)

    @staticmethod
    def _convert_number_to_account_type(number):
        return accounts.AccountType(number)

    @staticmethod
    def get_account_instance(account_type, chart_of_accounts, currency_id, start_debit=0, start_credit=0,
                             account_number=None, deposit_number=None, account_id=None):
        account_type = ContractController._convert_number_to_account_type(account_type)
        return accounts.ClientAccount(
            account_type=account_type, chart_of_accounts=chart_of_accounts, currency_id=currency_id,
            start_debit=start_debit, start_credit=start_credit, account_number=account_number,
            deposit_number=deposit_number, account_id=account_id)

    @staticmethod
    def get_deposit_instance(client_id, deposit_id, contract_number, currency_id, rate, term, start_date,
                             is_revocable, deposit_name,
                             current_account, credit_account, end_date=None):
        return accounts.Deposit(
            client_id=client_id, deposit_id=deposit_id, contract_number=contract_number, currency_id=currency_id,
            rate=rate, term=term, start_date=start_date, is_revocable=is_revocable, deposit_name=deposit_name,
            current_account=current_account, credit_account=credit_account, end_date=end_date
        )

    @staticmethod
    def get_deposit_table_header():
        return accounts.Deposit.get_table_header()

    def get_accounts_in_table_form(self, deposits_list):
        result_list = []
        for deposit in deposits_list:
            currency = self._get_currency_name_by_id(deposit.get_currency_id())
            deposit_accounts = deposit.get_table_form(currency)
            for account in deposit_accounts:
                result_list.append(account)
        return result_list

    def _get_spec_account_in_table_form(self, spec_table_dict, name):
        result_list = []
        for currency_id in spec_table_dict.keys():
            currency = self._get_currency_name_by_id(currency_id)
            spec_table = [
                spec_table_dict[currency_id].get_account_number(),
                name,
                spec_table_dict[currency_id].get_type_readable(),
                spec_table_dict[currency_id].get_debit(),
                spec_table_dict[currency_id].get_credit(),
                spec_table_dict[currency_id].get_saldo(),
                currency
            ]
            result_list.append(spec_table)
        return result_list

    def get_cash_registers_in_table_form(self):
        return self._get_spec_account_in_table_form(self.cash_register, "Касса")

    def get_bdfas_in_table_form(self):
        return self._get_spec_account_in_table_form(self.bdfa, "СФРБ")

    def get_spec_accounts_in_table_form(self):
        """Return all bdfa and cash register in table form"""
        cash_registers = self.get_cash_registers_in_table_form()
        bdfas = self.get_bdfas_in_table_form()
        return cash_registers + bdfas

    @staticmethod
    def get_bdfa_header():
        return [
            "Номер счета", "Название", "Тип", "Дебит", "Кредит", "Сальдо", "Валюта"
        ]

    @staticmethod
    def _is_give_persent(date: datetime.date, current_date: datetime.date):
        if date.day == current_date.day and date != current_date:
            return True
        return ContractController._check_day_and_month_length(date, current_date)

    @staticmethod
    def _check_day_and_month_length(date: datetime.date, current_date: datetime.date):
        if date == current_date:
            return False
        day = date.day
        if day == 31 and monthrange(date.year, date.month)[1] < 31:
            return True
        if day == 30 and monthrange(date.year, date.month)[1] < 30:
            return True
        return False

    def _update_deposit_end_date(self, deposit: accounts.Deposit, new_end_date):
        print("update", deposit.get_end_date())
        return self.db.update_deposit_end_date(
            deposit.current_account.get_account_id(),
            deposit.credit_account.get_account_id(),
            new_end_date
        )

    def _give_all_amount(self, deposit: accounts.Deposit, current_date):
        deposit.set_end_date(current_date)
        currency_id = deposit.get_currency_id()
        current_account = deposit.get_current_account()

        # снять все с текущего
        self.transfer_between_accounts(self.bdfa[currency_id], current_account, current_account.get_debit(),
                                       self.log_file, current_date)
        amount = current_account.get_saldo()
        self.transfer_between_accounts(current_account, self.cash_register[currency_id], amount,
                                       self.log_file, current_date)
        self._sub_from_cash_register(currency_id=currency_id, value=amount, log_file=self.log_file,
                                     current_date=current_date)

        # снять все с процентного
        credit_account = deposit.get_credit_account()
        amount = credit_account.get_saldo()
        self.transfer_between_accounts(credit_account, self.cash_register[currency_id], amount,
                                       self.log_file, current_date)
        self._sub_from_cash_register(value=amount, currency_id=currency_id, log_file=self.log_file,
                                     current_date=current_date)

        # update accounts
        self.update_account_in_db(current_account)
        self.update_account_in_db(credit_account)
        self._update_deposit_end_date(deposit, current_date)
        self.update_account_in_db(self.bdfa[currency_id], is_bdfa=True)
        self.update_account_in_db(self.cash_register[currency_id], is_cash_register=True)

    def _give_percent(self, deposit: accounts.Deposit, current_date):
        currency_id = deposit.get_currency_id()
        current_account = deposit.get_current_account()
        amount = current_account.get_debit()
        credit_account = deposit.get_credit_account()
        # amount + year percent / num of month
        percent_amount = round((amount * deposit.get_term() + amount) / 12, 2)
        self.transfer_between_accounts(self.bdfa[currency_id], credit_account, percent_amount,
                                       self.log_file, current_date)
        self.transfer_between_accounts(credit_account, self.cash_register[currency_id], percent_amount,
                                       self.log_file, current_date)
        self._sub_from_cash_register(value=percent_amount, currency_id=currency_id, log_file=self.log_file,
                                     current_date=current_date)
        # update accounts
        self.update_account_in_db(credit_account)
        self.update_account_in_db(self.bdfa[currency_id], is_bdfa=True)
        self.update_account_in_db(self.cash_register[currency_id], is_cash_register=True)

    def close_day(self, current_date, deposits):
        for deposit in deposits:
            deposit_end_date = deposit.get_end_date()
            if current_date == deposit_end_date or \
                    ContractController._check_day_and_month_length(deposit_end_date, current_date):

                self._give_all_amount(deposit, current_date)
            elif current_date > deposit_end_date:
                # депозит кончился, ничего не делать
                pass
            elif ContractController._is_give_persent(deposit_end_date, current_date):
                self._give_percent(deposit, current_date)

    @staticmethod
    def calculate_annuity_amount(start_amount, num_of_month, rate):
        i = rate / (num_of_month*100)
        k = (i*(1+i)**num_of_month)/((1+i)**num_of_month - 1)
        return round(start_amount/num_of_month, 2), round(k * start_amount - start_amount/num_of_month, 2)

    @staticmethod
    def calculate_differentiated_amount(start_amount, rate, paid_amount, term):
        """

        :param start_amount:
        :param rate:
        :param paid_amount:
        :return: основной, процентный
        """
        # paid - выплаченная часть кредита
        outstanding_balance = start_amount - paid_amount  # остаток задолженности
        # remaining_months = remaining_month if remaining_month else (end_date - current_date).days // 30
        month_rate = rate / (12*100)
        return round(outstanding_balance/term, 2), round(outstanding_balance*month_rate, 2)

    def _close_credit(self, credit):
        pass

    def _paid_percent(self, credit: accounts.Deposit, current_date):
        currency_id = credit.get_currency_id()
        if credit.get_is_revocable() == 0:
            # diff
            main, percent = ContractController.calculate_differentiated_amount(
                credit.get_current_account().get_debit(),
                credit.get_rate(),
                credit.get_credit_account().get_debit(),
                credit.get_term()
            )
        else:
            # ann
            main, percent = ContractController.calculate_annuity_amount(credit.get_current_account().get_debit(),
                                                                        credit.get_term(),
                                                                        credit.get_rate())
            # проценты
            credit_account = credit.get_credit_account()
            self.transfer_between_accounts(credit_account, self.bdfa[currency_id], percent,
                                           self.log_file, current_date)
            self._add_to_cash_register(value=percent, currency_id=currency_id, log_file=self.log_file,
                                       current_date=current_date)
            self.transfer_between_accounts(self.cash_register[currency_id], credit_account, percent,
                                           self.log_file, current_date)
            # основной
            self._add_to_cash_register(value=main, currency_id=currency_id, log_file=self.log_file,
                                       current_date=current_date)
            current_account = credit.get_current_account()
            self.transfer_between_accounts(self.cash_register[currency_id], current_account, main,
                                           self.log_file, current_date)
            self.transfer_between_accounts(current_account, self.bdfa[currency_id], main,
                                           self.log_file, current_date)
            # update accounts
            self.update_account_in_db(current_account)
            self.update_account_in_db(credit_account)
            self.update_account_in_db(self.bdfa[currency_id], is_bdfa=True)
            self.update_account_in_db(self.cash_register[currency_id], is_cash_register=True)

    def close_credit_day(self, current_date, credit_list):
        for credit in credit_list:
            deposit_end_date = credit.get_end_date()
            if current_date == deposit_end_date or \
                    ContractController._check_day_and_month_length(deposit_end_date, current_date):
                pass
                # СНЯТЬ ВСЕ СУММУ (ВЕРНУТЬ КРЕДИТ)
                # не надо, все возвращаем каждый месяц
                # self._give_all_amount(credit, current_date)
            elif current_date > deposit_end_date:
                # кредит кончился, ничего не делать
                pass
            elif ContractController._is_give_persent(deposit_end_date, current_date):
                self._paid_percent(credit, current_date)
                # снять процент

    def close_deposit(self, deposit, current_date):
        if deposit.get_is_revocable():
            if deposit.get_end_date() <= current_date:
                return f"Депозит {deposit.get_contract_number()} уже закрыт."
            self._give_all_amount(deposit, current_date)
            return None
        return f"Депозит {deposit.get_contract_number()} не является отзывным."

    @staticmethod
    def get_calculated_credit_header():
        return ["Месяц", "Основная сумма", "Проценты"]
