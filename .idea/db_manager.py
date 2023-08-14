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

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        self.cursor.execute(
            "SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url FROM vacancies LEFT JOIN companies ON vacancies.employer_id=companies.id"
        )
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        self.cursor.execute(
            "SELECT AVG((vacancies.salary_min + vacancies.salary_max)/2) FROM vacancies"
        )
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        self.cursor.execute(
            f"SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url FROM vacancies LEFT JOIN companies ON vacancies.employer_id=companies.id WHERE ((vacancies.salary_min + vacancies.salary_max)/2) > {avg_salary}"
        )
        return self.cursor.fetchall()

