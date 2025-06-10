import psycopg
import os
from config.setup import setup_commands
from pgvector.psycopg import register_vector

class DatabaseConnection:

    @staticmethod
    def setup():
        # Do intial setup
        with DatabaseConnection() as cur:
            print("Setup start")
            for command in setup_commands:
                cur.execute(command)
            print("Setup done")

    def __enter__(self):
        print("Connecting to db")
        self.conn = psycopg.connect(
            "postgresql://" + os.getenv("DB_USERNAME")
             + ":" + os.getenv("DB_PASSWORD")
             + "@localhost:" + os.getenv("DB_PORT")
             + "/" + os.getenv("DB_NAME")
        )

        register_vector(self.conn)
        self.cursor = self.conn.cursor()

        return self.cursor
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("Commiting and Closing DB connection")
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.commit()
            self.conn.close()
