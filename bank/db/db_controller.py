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
            {
                "field_name": "passport_series",
                "field_value": passport_series,
                "quote_char": True
            },
            {
                "field_name": "passport_number",
                "field_value": passport_number,
                "quote_char": False
            }
        ]
        found_records = self._select_records_by_parameters(db_names.PERSON_TABLE, params)
        if found_records:
            return True
        return False

    def is_passport_id_exists(self, passport_id):
        params = [{
            "field_name": "identification_number",
            "field_value": passport_id,
            "quote_char": True
        }]
        found_records = self._select_records_by_parameters(db_names.PERSON_TABLE, params)
        if found_records:
            return True
        return False

    @staticmethod
    def _quote_value(value, needs_quote_char):
        return f'"{value}"' if needs_quote_char else f'{value}'

    def insert_person(self):
        person_data = {
            "": "",
            "": "",
            "": "",
            "": "",
            "": "",
            "": "",
            "": ""
        }

        self._write_to_db(db_names.PERSON_TABLE, None)

    def _write_to_db(self, table_name, dict_of_params):
        """Insert new record into db table
        :param table_name: name of the db table
        :param dict_of_params: list with the following pattern:
                    {
                        field_name: field_name_value, (string)
                        field_value: field_value_value, (any type)
                        quote_char: quote_char_value (bool)
                    }
        :return:
        """
        # INSERT INTO `table_name`(column_1,column_2,...) VALUES (value_1,value_2,...);
        sql_column_names = []
        sql_insert_values = []

        if dict_of_params["field_value"]:
            value = DBController._quote_value(dict_of_params["field_value"], dict_of_params["quote_char"])
            sql_column_names.append(dict_of_params['field_name'])
            sql_insert_values.append(value)

        sql_names = ",".join(sql_column_names)
        sql_values = ",".join(sql_insert_values)

        sql_insert_request = f"INSERT INTO {table_name} ({sql_names}) VALUES ({sql_values})"
        try:
            self.cursor.execute(sql_insert_request)
            self.db.commit()
        except mysql.Error as error:
            return error

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

    def _get_all_rows_from_table(self, table_name):
        return self._select_records_by_parameters(table_name, [])

    def get_cities(self):
        return self._get_all_rows_from_table(db_names.CITY_TABLE)

    def get_citizenships(self):
        return self._get_all_rows_from_table(db_names.CITIZENSHIP_TABLE)

    def get_marital_status(self):
        return self._get_all_rows_from_table(db_names.MARITAL_STATUS_TABLE)

    def get_disabilities(self):
        return self._get_all_rows_from_table(db_names.DISABILITY_TABLE)


if __name__ == '__main__':
    db = DBController(creds.HOST, creds.USER, creds.PASSWORD, creds.DATABASE)
    print(db.get_disabilities())
