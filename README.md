# Проект "Анализ вакансий с hh.ru"

## Описание

Получение данных о компаниях и вакансиях с сайта hh.ru, используя публичный API, и сохранение этих данных в базе PostgreSQL. В этом проекте вы научитесь работать с внешним API, проектировать БД и выполнять запросы к ним с помощью Python и библиотеки psycopg2.

## Установка зависимостей

Установить библиотеки requests и psycopg2:

```
pip install requests psycopg2
```

## Настройка

1. Создайте базу данных PostgreSQL.

2. Замените значения `host`, `database`, `user` и `password` соответствующими значениями вашей БД:

```python
db_manager = DBManager("localhost", "your_db_name", "your_user", "your_password")
```

## Как использовать

1. Импортируйте `DBManager`.
2. Инициализируйте экземпляр `DBManager`.
3. Выполните вызовы различных методов класса:

```python
db_manager.get_companies_and_vacancies_count()
db_manager.get_all_vacancies()
db_manager.get_avg_salary()
db_manager.get_vacancies_with_higher_salary()
db_manager.get_vacancies_with_keyword("python")
```
