import pyodbc
import os

DB_SERVER = os.getenv("AEJG_DB_SERVER")
DATABASE = os.getenv("AEJG_DB")

DB_USER_NAME = os.getenv("AEJG_DB_USER_NAME")
DB_PASSWORD = os.getenv("AEJG_DB_PASSWORD")


class AejgDb:
    def __init__(self):
        connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={DB_SERVER};DATABASE={DATABASE};UID={DB_USER_NAME};PWD={DB_PASSWORD}'
        cnxn = pyodbc.connect(connectionString)
        self.cursor = cnxn.cursor()

    # not used, but ok to have when we need to update the table to get all column names into ./res/db_cols
    def get_db_schema(self):
        self.cursor.execute(
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'{{DATABASE}}\'")

    def execute_query(self, query) -> str:
        self.cursor.execute(query)
        result = ""
        for row in self.cursor:
            result += str(row)
        return result
