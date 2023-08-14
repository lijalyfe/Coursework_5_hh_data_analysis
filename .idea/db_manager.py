import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        self.cursor = self.conn.cursor()

