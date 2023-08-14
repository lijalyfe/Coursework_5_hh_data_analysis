import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        self.cursor.execute(
            "SELECT companies.name, COUNT(vacancies.id) AS vacancies_count FROM companies LEFT JOIN vacancies ON companies.id=vacancies.employer_id GROUP BY companies.id ORDER BY vacancies_count DESC"
        )
        return self.cursor.fetchall()