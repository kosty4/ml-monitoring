from dataclasses import dataclass

import psycopg2

@dataclass
class DB_CREDENTIALS:
    dbname: str
    user: str
    password: str
    host: str
    port: int


class DatabaseManager:

    def __init__(self, credentials: DB_CREDENTIALS) -> None:

        self.connection = psycopg2.connect(
            **credentials.__dict__
        )


    def add_prediction(self, userid: str, value: str):

        # Define the SQL statement to insert a row into the table
        insert_query = """
        INSERT INTO predictions (userid, prediction)
        VALUES (%s, %s)
        """

        insert_values = (userid, value)

        self.insert_template(insert_query, insert_values)


    def add_actual(self, userid: str, value: str):

        # Define the SQL statement to insert a row into the table
        insert_query = """
        INSERT INTO actuals (userid, actual)
        VALUES (%s, %s)
        """

        insert_values = (userid, value)

        self.insert_template(insert_query, insert_values)
    

    def insert_template(self, query, values):
        try:
            self.connection.cursor().execute(query, values)
            self.connection.commit()

        except psycopg2.Error as e:
            print("Error inserting row:", e)
