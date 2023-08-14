import requests
import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

# Подключение к БД
conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
cursor = conn.cursor()

# Создание таблиц
cursor.execute("""
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name TEXT,
    url TEXT
);
""")
cursor.execute("""
CREATE TABLE vacancies (
    id SERIAL PRIMARY KEY,
    name TEXT,
    salary_min INTEGER,
    salary_max INTEGER,
    employer_id INTEGER,
    FOREIGN KEY (employer_id) REFERENCES companies (id)
);
""")
conn.commit()

# Получение данных с API
companies_url = 'https://api.hh.ru/employers'
response = requests.get(companies_url)
companies_data = response.json()

vacancies_url = 'https://api.hh.ru/vacancies'
vacancies_data = []

for company in companies_data:
    company_vacancies_url = f'{vacancies_url}/?employer_id={company["id"]}'
    response = requests.get(company_vacancies_url)
    company_vacancies_data = response.json()['items']
    vacancies_data.extend(company_vacancies_data)
