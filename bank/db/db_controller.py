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

    def is_passport_number_exists(self, passport_series, passport_number):
        params = [
            DBController._create_param_dict("passport_series", passport_series, True),
            DBController._create_param_dict("passport_number", passport_number, False)
        ]
        found_records = self._select_records_by_parameters(db_names.PERSON_TABLE, params)
        if found_records:
            return True
        return False

    def is_passport_id_exists(self, passport_id):
        params = [
            DBController._create_param_dict("identification_number", passport_id, True)
        ]
        found_records = self._select_records_by_parameters(db_names.PERSON_TABLE, params)
        if found_records:
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

    def insert_person(self, first_name, surname, patronymic, birth_date, sex, passport_series, passport_number,
                      issued_by, issue_date, identification_number, birth_place, residence_address, home_phone,
                      mobile_phone, email, pension, monthly_income, marital_status, disability, citizenship,
                      residence_city, registration_city):

        person_data = [
            DBController._create_param_dict("first_name", first_name, True),
            DBController._create_param_dict("surname", surname, True),
            DBController._create_param_dict("patronymic", patronymic, True),
            DBController._create_param_dict("birth_date", birth_date, True),
            DBController._create_param_dict("sex", sex, False),
            DBController._create_param_dict("passport_series", passport_series, True),
            DBController._create_param_dict("passport_number", passport_number, False),
            DBController._create_param_dict("issued_by", issued_by, True),
            DBController._create_param_dict("issue_date", issue_date, True),
            DBController._create_param_dict("identification_number", identification_number, True),
            DBController._create_param_dict("birth_place", birth_place, True),
            DBController._create_param_dict("residence_address", residence_address, True),
            DBController._create_param_dict("home_phone", home_phone, True),
            DBController._create_param_dict("mobile_phone", mobile_phone, True),
            DBController._create_param_dict("email", email, True),
            DBController._create_param_dict("pension", pension, False),
            DBController._create_param_dict("monthly_income", monthly_income, False),
            DBController._create_param_dict(
                "marital_status", self._get_id_by_name(marital_status, db_names.MARITAL_STATUS_TABLE), False
            ),
            DBController._create_param_dict(
                "disability", self._get_id_by_name(disability, db_names.DISABILITY_TABLE), False
            ),
            DBController._create_param_dict(
                "citizenship", self._get_id_by_name(citizenship, db_names.CITIZENSHIP_TABLE), False
            ),
            DBController._create_param_dict(
                "residence_city", self._get_id_by_name(residence_city, db_names.CITY_TABLE), False
            ),
            DBController._create_param_dict(
                "registration_city", self._get_id_by_name(registration_city, db_names.CITY_TABLE), False
            )
        ]

        return self._write_to_db(db_names.PERSON_TABLE, person_data)

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
        print(sql_insert_request)
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
                        field_name: field_name_value, (string)
                        field_value: field_value_value, (any type)
                        quote_char: quote_char_value (bool)
                    },
                    ...
                ]
            example:
                field_name: passport_series
                field_value: 2222222
                quote_char: True
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

    def _convet_person_record(self, record, header):
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
            converted_records.append(self._convet_person_record(record, header))
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


if __name__ == '__main__':
    db = DBController(creds.HOST, creds.USER, creds.PASSWORD, creds.DATABASE)
    print(db.get_disabilities())
