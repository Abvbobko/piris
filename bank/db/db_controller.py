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
            return self._update_record(db_names.PERSON_TABLE, person_data, person_id)

        return self._write_to_db(db_names.PERSON_TABLE, person_data)

    def _update_record(self, table_name, list_of_params, person_id):
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

        sql_update_request = f"UPDATE {table_name} SET {sql_settled_params} WHERE idPerson={person_id}"
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

        sql_search_params = []
        for param in list_of_params:
            # add quote_char if needed and convert value to string
            value = DBController._quote_value(param["field_value"], param["quote_char"])
            # create string params like field=value
            sql_search_params.append(f"{param['field_name']}={value}")

        sql_where_params = " AND ".join(sql_search_params)

        sql_request = f"SELECT * FROM {table_name}"
        if sql_where_params:
            sql_request += f" WHERE {sql_where_params}"

        self.cursor.execute(sql_request)
        return self.cursor.fetchall()

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

    def close_connection(self):
        self.db.close()

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

    def get_citizenship_by_id(self, citizenship_id):
        return self._get_name_by_id(citizenship_id, db_names.CITIZENSHIP_TABLE)

    def get_marital_status_by_id(self, marital_status_id):
        return self._get_name_by_id(marital_status_id, db_names.MARITAL_STATUS_TABLE)

    def get_disability_by_id(self, disability_id):
        return self._get_name_by_id(disability_id, db_names.DISABILITY_TABLE)

    @staticmethod
    def get_names_from_values(values):
        return [item[1] for item in values] if values else []

    def _get_all_rows_from_table(self, table_name):
        return self._select_records_by_parameters(table_name, [])

    def _get_name_list(self, table_name):
        return DBController.get_names_from_values(self._get_all_rows_from_table(table_name))

    def get_cities(self):
        return self._get_name_list(db_names.CITY_TABLE)

    def get_citizenships(self):
        return self._get_name_list(db_names.CITIZENSHIP_TABLE)

    def get_marital_status(self):
        return self._get_name_list(db_names.MARITAL_STATUS_TABLE)

    def get_disabilities(self):
        return self._get_name_list(db_names.DISABILITY_TABLE)

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

    def _delete_from_table_by_field(self, table_name, field_name, field_value):
        try:
            sql_request = f"DELETE FROM {table_name} WHERE {field_name}={field_value}"
            self.cursor.execute(sql_request)
            self.db.commit()
        except mysql.Error as error:
            return str(error)
        return None

    def delete_person_by_id(self, person_id):
        return self._delete_from_table_by_field(db_names.PERSON_TABLE, "idPerson", person_id)


if __name__ == '__main__':
    db = DBController(creds.HOST, creds.USER, creds.PASSWORD, creds.DATABASE)
    print(db.get_disabilities())
