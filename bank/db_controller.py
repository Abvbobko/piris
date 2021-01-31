import mysql.connector as mysql
import bank.creds as creds


class DBController:
    def __init__(self, host, user, password, database):
        self.db = self.__get_connection(host, user, password, database)
        self.cursor = self.db.cursor()

    def connect(self, host, user, password, database):
        self.db = self.__get_connection(host, user, password, database)

    @staticmethod
    def __get_connection(host, user, password, database):
        try:
            return mysql.connect(
                host=host,
                user=user,
                passwd=password,
                database=database
            )
        except Exception:
            print("Can't connect to database")
        return None

    def close_connection(self):
        self.db.close()

    def get_tables(self):
        self.cursor.execute("SHOW TABLES")
        tables = [table for (table, ) in self.cursor.fetchall()]
        return tables

    def _get_all_rows_from_table(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return list(self.cursor.fetchall())

    def get_cities(self):
        return self._get_all_rows_from_table("city")

    def get_citizenships(self):
        return self._get_all_rows_from_table("citizenship")

    def get_marital_status(self):
        return self._get_all_rows_from_table("maritalstatus")

    def get_disabilities(self):
        return self._get_all_rows_from_table("disability")




if __name__ == '__main__':
    db = DBController(creds.HOST, creds.USER, creds.PASSWORD, creds.DATABASE)
    print(db.get_disabilities())

