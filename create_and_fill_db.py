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
        name TEXT UNIQUE,
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
        url TEXT,
        employer_id INTEGER,
        FOREIGN KEY (employer_id) REFERENCES companies (id)
    );
    """)

conn.commit()

# Получение данных с API
companies_url = 'https://api.hh.ru/employers'
response = requests.get(companies_url)
companies_data = response.json()['items'][:10]

vacancies_url = 'https://api.hh.ru/vacancies'
n_vacancies_per_company = 10

for company in companies_data:
    cursor.execute("SELECT id FROM companies WHERE name=%s", (company["name"],))
    company_id_exists = cursor.fetchone()

    if not company_id_exists:
        cursor.execute(
            "INSERT INTO companies (name, url) VALUES (%s, %s) RETURNING id", (company["name"], company["url"])
        )
        company_id = cursor.fetchone()[0]
    else:
        company_id = company_id_exists[0]

    company_vacancies_url = f'{vacancies_url}/?employer_id={company["id"]}'
    response = requests.get(company_vacancies_url)
    vacancies_data = response.json()['items']

    for vacancy in vacancies_data[:n_vacancies_per_company]:
        salary = vacancy.get('salary')
        salary_min = salary.get('from') if salary else None
        salary_max = salary.get('to') if salary else None
        cursor.execute(
            "INSERT INTO vacancies (name, salary_min, salary_max, url, employer_id) VALUES (%s, %s, %s, %s, %s)",
            (vacancy["name"], salary_min, salary_max, vacancy["url"], company_id)
        )

conn.commit()
