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
            value = f'"{param["field_value"]}"' if param["quote_char"] else f'{param["field_value"]}'
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
