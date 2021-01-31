import mysql.connector as mysql


class DBController:
    def __init__(self, host, user, password, database):
        self.db = self.__get_connection(host, user, password, database)

    def connect(self, host, user, password, database):
        self.db = self.__get_connection(host, user, password, database)

    @staticmethod
    def __get_connection(host, user, password, database):
        return mysql.connect(
            host=host,  # "localhost",
            user=user,  # "root",
            passwd=password,  # "dbms",
            database=database  # "bank_db"
        )
