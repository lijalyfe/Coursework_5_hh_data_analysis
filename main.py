from db_manager import DBManager

db_manager = DBManager()

# получаем список компаний и количество вакансий у каждой компании
companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
print("Cписок компаний и количество вакансий у каждой компании:")
for company in companies_and_vacancies_count:
    print(company[0], company[1])

# получаем список всех вакансий
all_vacancies = db_manager.get_all_vacancies()
print("Cписок всех вакансий: ")
for vacancy in all_vacancies:
    print(*vacancy)

# получаем среднюю зарплату по вакансиям
avg_salary = db_manager.get_avg_salary()
print("Cредняя зарплата по вакансиям: ", avg_salary)

# получаем список всех вакансий, у которых зарплата выше средней по всем вакансиям
higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
if higher_salary_vacancies:
    print("Cписок всех вакансий, у которых зарплата выше средней по всем вакансиям: ")
    for vacancy in higher_salary_vacancies:
        print(*vacancy)
else:
    print("Нет вакансий с указанной информацией о зарплате.")

# запрашиваем ключевое слово от пользователя
user_keyword = input("Введите ключевое слово для поиска вакансий: ")

# получаем список всех вакансий, в названии которых содержатся переданные в метод слова
keyword_vacancies = db_manager.get_vacancies_with_keyword(user_keyword)
print("Cписок всех вакансий, в названии которых содержатся переданные в метод слова:")
for vacancy in keyword_vacancies:
    print(*vacancy)
