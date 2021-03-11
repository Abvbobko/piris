import mysql.connector as mysql
import bank.db.constants.creds as creds
import bank.db.constants.db_names as db_names


class DBController:
    def __init__(self, host, user, password, database):
        self.db = self.__get_connection(host, user, password, database)
        self.cursor = self.db.cursor()

    def connect(self, host, user, password, database):
        self.db = self.__get_connection(host, user, password, database)

    @staticmethod
    def __get_connection(host, user, password, database):
        return mysql.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )

    def close_connection(self):
        self.db.close()

    """--- Client part ---"""

    def is_passport_number_exists(self, passport_series, passport_number, updating_mode=False, person_id=None):
        params = [
            DBController._create_param_dict("passport_series", passport_series, True),
            DBController._create_param_dict("passport_number", passport_number, False)
        ]
        found_records = self._select_records_by_parameters(db_names.PERSON_TABLE, params)
        if updating_mode:
            for record in found_records:
                if record[0] != person_id:
                    return True
        elif found_records:
            return True
        return False

    def is_passport_id_exists(self, passport_id, updating_mode=False, person_id=None):
        params = [
            DBController._create_param_dict("identification_number", passport_id, True)
        ]
        found_records = self._select_records_by_parameters(db_names.PERSON_TABLE, params)

        if updating_mode:
            for record in found_records:
                if record[0] != person_id:
                    return True

        elif found_records:
            return True
        return False

    def insert_person(self, update_mode=False, person_id=None, **kwargs):

        person_data = [
            DBController._create_param_dict("first_name", kwargs["first_name"], True),
            DBController._create_param_dict("surname", kwargs["surname"], True),
            DBController._create_param_dict("patronymic", kwargs["patronymic"], True),
            DBController._create_param_dict("birth_date", kwargs["birth_date"], True),
            DBController._create_param_dict("sex", kwargs["sex"], False),
            DBController._create_param_dict("passport_series", kwargs["passport_series"], True),
            DBController._create_param_dict("passport_number", kwargs["passport_number"], False),
            DBController._create_param_dict("issued_by", kwargs["issued_by"], True),
            DBController._create_param_dict("issue_date", kwargs["issue_date"], True),
            DBController._create_param_dict("identification_number", kwargs["identification_number"], True),
            DBController._create_param_dict("birth_place", kwargs["birth_place"], True),
            DBController._create_param_dict("residence_address", kwargs["residence_address"], True),
            DBController._create_param_dict("home_phone", kwargs["home_phone"], True),
            DBController._create_param_dict("mobile_phone", kwargs["mobile_phone"], True),
            DBController._create_param_dict("email", kwargs["email"], True),
            DBController._create_param_dict("pension", kwargs["pension"], False),
            DBController._create_param_dict("monthly_income", kwargs["monthly_income"], False),
            DBController._create_param_dict(
                "marital_status", self._get_id_by_name(kwargs["marital_status"], db_names.MARITAL_STATUS_TABLE), False
            ),
            DBController._create_param_dict(
                "disability", self._get_id_by_name(kwargs["disability"], db_names.DISABILITY_TABLE), False
            ),
            DBController._create_param_dict(
                "citizenship", self._get_id_by_name(kwargs["citizenship"], db_names.CITIZENSHIP_TABLE), False
            ),
            DBController._create_param_dict(
                "residence_city", self._get_id_by_name(kwargs["residence_city"], db_names.CITY_TABLE), False
            ),
            DBController._create_param_dict(
                "registration_city", self._get_id_by_name(kwargs["registration_city"], db_names.CITY_TABLE), False
            )
        ]

        if update_mode and person_id is not None:
            list_of_id_params = [DBController._create_param_dict("idPerson", person_id, False)]
            return self._update_record(db_names.PERSON_TABLE, person_data, list_of_id_params)

        return self._write_to_db(db_names.PERSON_TABLE, person_data)

    def get_person(self, person_id):
        params = [{
            "field_name": "idPerson",
            "field_value": person_id,
            "quote_char": False
        }]
        person = self._select_records_by_parameters(db_names.PERSON_TABLE, params)
        header = self.cursor.column_names
        converted_records = self._convert_person_records(person, header)

        return {
            "columns": header,
            "records": converted_records
        }

    def get_cities(self):
        return self._get_name_list(db_names.CITY_TABLE)

    def get_citizenships(self):
        return self._get_name_list(db_names.CITIZENSHIP_TABLE)

    def get_marital_status(self):
        return self._get_name_list(db_names.MARITAL_STATUS_TABLE)

    def get_disabilities(self):
        return self._get_name_list(db_names.DISABILITY_TABLE)

    def get_citizenship_by_id(self, citizenship_id):
        return self._get_name_by_id(citizenship_id, db_names.CITIZENSHIP_TABLE)

    def get_marital_status_by_id(self, marital_status_id):
        return self._get_name_by_id(marital_status_id, db_names.MARITAL_STATUS_TABLE)

    def get_disability_by_id(self, disability_id):
        return self._get_name_by_id(disability_id, db_names.DISABILITY_TABLE)

    def _convert_person_record(self, record, header):
        converted_record = []
        for i in range(len(record)):
            if header[i] == "marital_status":
                converted_record.append(self._get_name_by_id(record[i], db_names.MARITAL_STATUS_TABLE))
            elif header[i] == "disability":
                converted_record.append(self._get_name_by_id(record[i], db_names.DISABILITY_TABLE))
            elif header[i] == "citizenship":
                converted_record.append(self._get_name_by_id(record[i], db_names.CITIZENSHIP_TABLE))
            elif header[i] == "residence_city" or header[i] == "registration_city":
                converted_record.append(self._get_name_by_id(record[i], db_names.CITY_TABLE))
            else:
                converted_record.append(record[i])
        return tuple(converted_record)

    def delete_person_by_id(self, person_id):
        return self._delete_from_table_by_field(db_names.PERSON_TABLE, "idPerson", person_id)

    def _convert_person_records(self, records, header):
        converted_records = []
        for record in records:
            converted_records.append(self._convert_person_record(record, header))
        return tuple(converted_records)

    def get_clients(self):
        """Return dict {
            "columns": (column_1_name, column_2_name, ...)
            "records": (record_1, record_2, ...)
        }
        where record_# is tuple (value_1, value_2, ...)
        :return: dictionary with values
        """
        clients = self._get_all_rows_from_table(db_names.PERSON_TABLE)
        header = self.cursor.column_names
        converted_records = self._convert_person_records(clients, header)
        return {
            "columns": header,
            "records": converted_records
        }

    """################## SPEC OPERATIONS ##################"""

    @staticmethod
    def _quote_value(value, needs_quote_char):
        if value is None:
            return value
        return f'"{value}"' if needs_quote_char else f'{value}'

    @staticmethod
    def _create_param_dict(field_name, value, need_quote_char):
        return {
            "field_name": field_name,
            "field_value": value,
            "quote_char": need_quote_char
        }

    def _update_record(self, table_name, list_of_params, list_of_id_params):
        """Update record in the db table
        :param table_name: name of the db table
        :param list_of_params: list with the following pattern:
                [
                    {
                        field_name: field_name_value, (string)
                        field_value: field_value_value, (any type)
                        quote_char: quote_char_value (bool)
                    },
                    ...
                ]
        :return:
        """

        # UPDATE table_name SET column_name1 = expr1, column_name2 = expr2 WHERE condition;

        sql_setted_params = []
        for param in list_of_params:
            if param["field_value"] is not None:
                value = DBController._quote_value(param["field_value"], param["quote_char"])
            else:
                value = "NULL"
            sql_setted_params.append(f"{param['field_name']}={value}")

        sql_settled_params = ",".join(sql_setted_params)
        sql_where_condition = DBController._generate_where_condition(list_of_id_params)
        sql_update_request = f"UPDATE {table_name} SET {sql_settled_params} WHERE {sql_where_condition}"
        try:
            self.cursor.execute(sql_update_request)
            self.db.commit()
        except mysql.Error as error:
            return str(error)

        return None

    def _write_to_db(self, table_name, list_of_params):
        """Insert new record into db table
        :param table_name: name of the db table
        :param list_of_params: list with the following pattern:
                [
                    {
                        field_name: field_name_value, (string)
                        field_value: field_value_value, (any type)
                        quote_char: quote_char_value (bool)
                    },
                    ...
                ]
        :return:
        """
        # INSERT INTO `table_name`(column_1,column_2,...) VALUES (value_1,value_2,...);
        sql_column_names = []
        sql_insert_values = []
        for param in list_of_params:
            if param["field_value"] is not None:
                value = DBController._quote_value(param["field_value"], param["quote_char"])
                sql_column_names.append(param['field_name'])
                sql_insert_values.append(value)

        sql_names = ",".join(sql_column_names)
        sql_values = ",".join(sql_insert_values)

        sql_insert_request = f"INSERT INTO {table_name} ({sql_names}) VALUES ({sql_values})"
        try:
            self.cursor.execute(sql_insert_request)
            self.db.commit()
        except mysql.Error as error:
            return str(error)

        return None

    @staticmethod
    def _generate_where_condition(list_of_params):
        sql_search_params = []
        for param in list_of_params:
            # add quote_char if needed and convert value to string
            value = DBController._quote_value(param["field_value"], param["quote_char"])
            # create string params like field=value
            sql_search_params.append(f"{param['field_name']}={value}")

        sql_where_params = " AND ".join(sql_search_params)
        return sql_where_params

    def _select_records_by_parameters(self, table_name, list_of_params):
        """Find records with list_of_param parameters and return it
        :param table_name: name of the db table
        :param list_of_params: list with the following pattern:
                [
                    {
                        "field_name": field_name_value, (string)
                        "field_value": field_value_value, (any type)
                        "quote_char": quote_char_value (bool)
                    },
                    ...
                ]
            example:
                "field_name": passport_series
                "field_value": 2222222
                "quote_char": True
            without quote_char is value
            with quote_char is 'value' (or "value")

            if there are no any parameters just pass empty list
        :return: list of found values
        """

        sql_where_params = DBController._generate_where_condition(list_of_params)

        sql_request = f"SELECT * FROM {table_name}"
        if sql_where_params:
            sql_request += f" WHERE {sql_where_params}"
        self.cursor.execute(sql_request)
        return self.cursor.fetchall()

    def get_tables(self):
        self.cursor.execute("SHOW TABLES")
        tables = [table for (table, ) in self.cursor.fetchall()]
        return tables

    def _get_id_by_name(self, name, table_name):
        map_list = self._get_all_rows_from_table(table_name)
        value_id = None
        for record in map_list:
            if record[1] == name:
                value_id = record[0]
                break
        return value_id

    def _get_name_by_id(self, value_id, table_name):
        map_list = self._get_all_rows_from_table(table_name)
        value_name = None
        for record in map_list:
            if record[0] == value_id:
                value_name = record[1]
                break
        return value_name

    def get_last_inserted_id(self):
        return self.cursor.lastrowid

    @staticmethod
    def get_names_from_values(values):
        return [item[1] for item in values] if values else []

    def _get_all_rows_from_table(self, table_name):
        return self._select_records_by_parameters(table_name, [])

    def _get_name_list(self, table_name):
        return DBController.get_names_from_values(self._get_all_rows_from_table(table_name))

    def _delete_from_table_by_field(self, table_name, field_name, field_value):
        try:
            sql_request = f"DELETE FROM {table_name} WHERE {field_name}={field_value}"
            self.cursor.execute(sql_request)
            self.db.commit()
        except mysql.Error as error:
            return str(error)
        return None

    @staticmethod
    def _get_field_by_name(records, header, field_name):
        column = []
        if records and len(header) != len(records[0]):
            raise Exception("Error. Sizes of header and records must be the same.")
        for i in range(len(header)):
            if header[i] == field_name:
                column = [record[i] for record in records]
                break
        return column

    @staticmethod
    def _get_first_list_value(some_list):
        return None if not some_list else some_list[0]

    @staticmethod
    def _get_field_value(records, header, field_name):
        return DBController._get_first_list_value(DBController._get_field_by_name(records, header, field_name))

    @staticmethod
    def _convert_db_record_to_dict(record, header):
        record_dict = {}
        if len(header) != len(record):
            raise Exception("Error. Sizes of header and record must be the same.")
        for i in range(len(header)):
            record_dict[header[i]] = record[i]
        return record_dict

    """################## DEPOSIT PART ##################"""

    def is_deposit_number_exists(self, deposit_number):
        params = [
            DBController._create_param_dict("contract_number", deposit_number, True)
        ]
        found_records = self._select_records_by_parameters(db_names.CLIENT_DEPOSIT_TABLE, params)

        if found_records:
            return True
        return False

    def get_deposits(self, is_credit=0):
        """
        type 0 - дифференцированный
             1 - ануированный
        :param is_credit:
        :return:
        """
        params = [
            DBController._create_param_dict("type", is_credit, False),
        ]
        deposits = self._select_records_by_parameters(db_names.DEPOSIT_TABLE, params)
        return DBController.get_names_from_values(deposits)

    def get_currencies(self):
        return self._get_name_list(db_names.CURRENCY_TABLE)

    def get_currency_id_by_name(self, currency):
        return self._get_id_by_name(currency, db_names.CURRENCY_TABLE)

    def get_currency_name_by_id(self, currency_id):
        return self._get_name_by_id(currency_id, db_names.CURRENCY_TABLE)

    def get_terms(self, deposit_name, currency_name):
        deposit_id = self._get_id_by_name(deposit_name, db_names.DEPOSIT_TABLE)
        currency_id = self._get_id_by_name(currency_name, db_names.CURRENCY_TABLE)
        params = [
            DBController._create_param_dict("deposit_id", deposit_id, False),
            DBController._create_param_dict("currency_id", currency_id, False)
        ]
        programs = self._select_records_by_parameters(db_names.DEPOSIT_PROGRAM_TABLE, params)
        header = self.cursor.column_names
        return DBController._get_field_by_name(programs, header, "term")

    def get_deposit_info(self, deposit_name, currency_name, term):
        deposit_id = self._get_id_by_name(deposit_name, db_names.DEPOSIT_TABLE)
        # get main deposit info
        params = [DBController._create_param_dict("id", deposit_id, False)]
        deposit = self._select_records_by_parameters(db_names.DEPOSIT_TABLE, params)
        header = self.cursor.column_names
        deposit_dict = DBController._convert_db_record_to_dict(deposit[0], header)

        # get deposit program info
        currency_id = self._get_id_by_name(currency_name, db_names.CURRENCY_TABLE)
        params = [
            DBController._create_param_dict("deposit_id", deposit_id, False),
            DBController._create_param_dict("currency_id", currency_id, False),
            DBController._create_param_dict("term", term, False)
        ]
        program = self._select_records_by_parameters(db_names.DEPOSIT_PROGRAM_TABLE, params)
        header = self.cursor.column_names

        return {
            "id": DBController._get_field_value(program, header, "id"),
            "min_amount": DBController._get_field_value(program, header, "min_amount"),
            "max_amount": DBController._get_field_value(program, header, "max_amount"),
            "rate": DBController._get_field_value(program, header, "rate"),
            "start_date": DBController._get_field_value(program, header, "start_date"),
            "end_date": DBController._get_field_value(program, header, "end_date"),
            "deposit_name": deposit_dict["name"],
            "is_revocable": True if deposit_dict["is_revocable"] else False
        }

    def get_bdfas(self):
        params = [DBController._create_param_dict("is_bdfa", 1, False)]
        bdfas = self._select_records_by_parameters(db_names.CLIENT_ACCOUNT_TABLE, params)
        header = self.cursor.column_names

        return {
            "columns": header,
            "records": bdfas
        }

    def get_cash_registers(self):
        params = [DBController._create_param_dict("is_cash_register", 1, False)]
        bdfas = self._select_records_by_parameters(db_names.CLIENT_ACCOUNT_TABLE, params)
        header = self.cursor.column_names

        return {
            "columns": header,
            "records": bdfas
        }

    def is_deposit_revocable(self, deposit_name):
        params = [DBController._create_param_dict("name", deposit_name, True)]
        deposit = self._select_records_by_parameters(db_names.DEPOSIT_TABLE, params)
        # 0 - возвратный
        # 1 - невозвратный
        is_revocable = True if deposit[0][2] == 1 else False
        return is_revocable

    def _get_account_by_id(self, account_id):
        params = [DBController._create_param_dict("id", account_id, False)]
        account = self._select_records_by_parameters(db_names.CLIENT_ACCOUNT_TABLE, params)
        if account:
            return account[0]
        return None

    def _get_deposit_by_id(self, deposit_id):
        params = [DBController._create_param_dict("id", deposit_id, False)]
        deposit = self._select_records_by_parameters(db_names.DEPOSIT_TABLE, params)
        if deposit:
            return deposit[0]
        return None

    def get_deposits_instances(self, client_id,
                               create_account_entity_func, create_deposit_entity_func, deposit_number=None,
                               is_credits=0):
        """Return dict {
            "records": [record_1, record_2, ...],
            "deposit_columns": (column_1_name, column_2_name, ...),
            "account_columns": (column_1_name, column_2_name, ...)
        } where record_# is Deposit instance
        :return:
        """
        result_deposit_list = []
        if deposit_number:
            params = [DBController._create_param_dict("contract_number", deposit_number, False)]
            deposits = self._select_records_by_parameters(db_names.CLIENT_DEPOSIT_TABLE, params)
            if not deposits:
                return "Депозита с таким номером нет."
        elif client_id is not None:
            deposits = self._get_all_clients_deposits(client_id)
        else:
            deposits = self._get_all_rows_from_table(db_names.CLIENT_DEPOSIT_TABLE)
        header = self.cursor.column_names
        for deposit in deposits:
            deposit_dict = DBController._convert_db_record_to_dict(deposit, header)
            current_account = self._get_account_object(deposit_dict["current_account"], create_account_entity_func)
            credit_account = self._get_account_object(deposit_dict["credit_account"], create_account_entity_func)
            deposit_program = self._get_deposit_program_by_id(deposit_dict["deposit_id"])
            deposit_program_dict = self._convert_db_record_to_dict(deposit_program, self.cursor.column_names)

            main_deposit_info = self._get_deposit_by_id(deposit_program_dict["deposit_id"])
            main_deposit_info = self._convert_db_record_to_dict(main_deposit_info, self.cursor.column_names)
            if is_credits == main_deposit_info["type"]:
                # if credit - 0 and type - 0 or credit - 1 and type - 1
                deposit_entity = create_deposit_entity_func(
                    client_id=deposit_dict["client"], deposit_id=deposit_dict["deposit_id"],
                    contract_number=deposit_dict["contract_number"], start_date=deposit_dict["deposit_start_date"],
                    currency_id=deposit_program_dict["currency_id"], rate=deposit_program_dict["rate"],
                    term=deposit_program_dict["term"],
                    current_account=current_account, credit_account=credit_account,
                    is_revocable=main_deposit_info["is_revocable"], deposit_name=main_deposit_info["name"],
                    end_date=deposit_dict["deposit_end_date"]
                )
                result_deposit_list.append(deposit_entity)

        return result_deposit_list

    def _get_all_clients_deposits(self, client_id):
        params = [
            DBController._create_param_dict("client", client_id, False)
        ]
        deposits = self._select_records_by_parameters(db_names.CLIENT_DEPOSIT_TABLE, params)
        return deposits

    def _get_deposit_program_by_id(self, deposit_id):
        params = [DBController._create_param_dict("id", deposit_id, False)]
        deposit_program = self._select_records_by_parameters(db_names.DEPOSIT_PROGRAM_TABLE, params)
        if deposit_program:
            return deposit_program[0]
        return None

    def _get_account_object(self, account_id, creating_func):
        account_db_form = self._get_account_by_id(account_id)
        account_header = self.cursor.column_names
        account_dict = DBController._convert_db_record_to_dict(account_db_form, account_header)
        return creating_func(
            account_type=account_dict["type"],
            chart_of_accounts=account_dict["chart_of_accounts"],
            currency_id=account_dict["currency_id"],
            start_debit=account_dict["debit"],
            start_credit=account_dict["credit"],
            account_number=account_dict["number"],
            account_id=account_dict["id"]
        )

    def get_current_date(self):
        params = [DBController._create_param_dict("id", db_names.CURRENT_DATE_ID, False)]
        curr_date = self._select_records_by_parameters(db_names.CURRENT_DATE_TABLE, params)
        return curr_date[0][1]

    def update_current_date(self, new_date):
        params = [DBController._create_param_dict("curr_date", new_date, True)]
        id_params = [DBController._create_param_dict("id", db_names.CURRENT_DATE_ID, False)]
        return self._update_record(db_names.CURRENT_DATE_TABLE, params, id_params)

    def update_deposit_end_date(self, current_account_id, credit_account_id, new_end_date):
        params = [DBController._create_param_dict("deposit_end_date", new_end_date, True)]
        id_params = [
            DBController._create_param_dict("current_account", current_account_id, False),
            DBController._create_param_dict("credit_account", credit_account_id, False)
        ]
        print(current_account_id, credit_account_id)
        return self._update_record(db_names.CLIENT_DEPOSIT_TABLE, params, id_params)

    def insert_account(self, update_mode=False, account_id=None, **kwargs):
        account_data = [
            DBController._create_param_dict("is_bdfa", kwargs["is_bdfa"], False),
            DBController._create_param_dict("is_cash_register", kwargs["is_cash_register"], False),
            DBController._create_param_dict("debit", kwargs["debit"], False),
            DBController._create_param_dict("credit", kwargs["credit"], False),
            DBController._create_param_dict("type", kwargs["account_type"], False),
            DBController._create_param_dict("currency_id", kwargs["currency_id"], False),
            DBController._create_param_dict("chart_of_accounts", kwargs["chart_of_accounts_number"], False),
            DBController._create_param_dict("number", kwargs["account_number"], True)
        ]
        if update_mode and account_id is not None:
            id_params = [DBController._create_param_dict("id", account_id, False)]
            return self._update_record(db_names.CLIENT_ACCOUNT_TABLE, account_data, id_params)

        return self._write_to_db(db_names.CLIENT_ACCOUNT_TABLE, account_data)

    @staticmethod
    def create_deposit_accounts_id_dict(current_id, credit_id):
        return {
            "current": current_id,
            "credit": credit_id
        }

    def insert_deposit(self, update_mode=False, deposit_id=None, accounts_ids=None, **kwargs):
        """

        :param update_mode:
        :param deposit_id:
        :param accounts_ids: {
            "current": current_account_id,
            "credit": credit_account_id
        }
        :param kwargs:
        :return:
        """
        account_data = [
            DBController._create_param_dict("client", kwargs["client_id"], False),
            DBController._create_param_dict("current_account", kwargs["current_account"], False),
            DBController._create_param_dict("credit_account", kwargs["credit_account"], False),
            DBController._create_param_dict("contract_number", kwargs["contract_number"], True),
            DBController._create_param_dict("deposit_id", kwargs["deposit_program_id"], False),
            DBController._create_param_dict("deposit_start_date", kwargs["deposit_start_date"], True),
            DBController._create_param_dict("deposit_end_date", kwargs["deposit_end_date"], True)
        ]
        if update_mode and deposit_id is not None:
            id_params = [
                DBController._create_param_dict("current_account", accounts_ids["current"], False),
                DBController._create_param_dict("credit_account", accounts_ids["credit"], False),
            ]
            return self._update_record(db_names.CLIENT_DEPOSIT_TABLE, account_data, id_params)

        return self._write_to_db(db_names.CLIENT_DEPOSIT_TABLE, account_data)


if __name__ == '__main__':
    db = DBController(creds.HOST, creds.USER, creds.PASSWORD, creds.DATABASE)
    print(db.get_disabilities())
