import sqlite3
import logging


logger = logging.getLogger(__name__)

# it can alternatively be used in a
# flask context:
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
# but that would be an overkill here
class DBConnector:
    def __init__(self):
        self.db_path = "db/products.db"
        self.prepare_db()

    def prepare_db(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS sequences(number INTEGER PRIMARY KEY, sequence TEXT)"
        )
        connection.commit()
        connection.close()

    def insert_sequence(self, number, sequence):
        connection = sqlite3.connect(self.db_path)
        sql = "INSERT OR IGNORE INTO sequences(number,sequence) VALUES (?,?)"
        connection.cursor().execute(sql, (number, sequence))
        connection.commit()

    def get_sequence(self, number):
        connection = sqlite3.connect(self.db_path)
        sql = "SELECT * FROM sequences WHERE number=?"
        result = connection.cursor().execute(sql, (number,)).fetchone()
        connection.close()
        return result
