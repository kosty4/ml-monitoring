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
        self.credentials = credentials.__dict__

    def run_query(self, query, params):
        conn = self.connection = psycopg2.connect(
            **self.credentials
        )
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
        except psycopg2.Error as e:
            print("Error inserting row:", e)
        except Exception as e:
            print("Generic exception:", e)
            conn.rollback()
        finally:
            conn.close()

    def add_prediction(self, userid: str, value: str):

        # Define the SQL statement to insert a row into the table
        insert_query = """
        INSERT INTO predictions (userid, prediction)
        VALUES (%s, %s)
        """

        insert_values = (userid, value)

        self.run_query(insert_query, insert_values)


    def add_actual(self, userid: str, value: str):

        # Define the SQL statement to insert a row into the table
        insert_query = """
        INSERT INTO actuals (userid, actual)
        VALUES (%s, %s)
        """

        insert_values = (userid, value)
        self.run_query(insert_query, insert_values)