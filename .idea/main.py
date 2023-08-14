from db_manager import DBManager

db_manager = DBManager()

# получаем список компаний и количество вакансий у каждой компании
companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
for company in companies_and_vacancies_count:
    print(company[0], company[1])
