import requests
import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

# Подключение к БД
conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
cursor = conn.cursor()

# Проверка наличия таблиц
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
existing_tables = [row[0] for row in cursor.fetchall()]

# Создание таблиц
if 'companies' not in existing_tables:
    cursor.execute("""
    CREATE TABLE companies (
        id SERIAL PRIMARY KEY,
        name TEXT,
        url TEXT
    );
    """)

if 'vacancies' not in existing_tables:
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
companies_data = response.json()['items']

vacancies_url = 'https://api.hh.ru/vacancies'
vacancies_data = []

for company in companies_data:
    company_vacancies_url = f'{vacancies_url}/?employer_id={company["id"]}'
    response = requests.get(company_vacancies_url)
    company_vacancies_data = response.json()['items']
    vacancies_data.extend(company_vacancies_data)

# Заполнение таблиц данными
for company in companies_data:
    cursor.execute("INSERT INTO companies (name, url) VALUES (%s, %s)", (company["name"], company["url"]))

conn.commit()  # Добавление всех компаний в БД перед добавлением вакансий

for vacancy in vacancies_data:
    employer_id = vacancy["employer"]["id"]

    cursor.execute("SELECT id FROM companies WHERE id=%s", (employer_id,))

    if cursor.fetchone() is not None:
        salary = vacancy.get('salary')
        salary_min = salary.get('from') if salary else None
        salary_max = salary.get('to') if salary else None
        cursor.execute(
            "INSERT INTO vacancies (name, salary_min, salary_max, employer_id) VALUES (%s, %s, %s, %s)",
            (vacancy["name"], salary_min, salary_max, employer_id)
        )

conn.commit()
