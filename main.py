from __future__ import annotations

from utils import DBManager, add_vacancies_to_db


def user_interaction():
    """
    Пользовательский интерфейс.
    """

    # Приветствие.
    print(f"Перед началом: Пользователю необходимо выбирать варианты ответов посредством указания цифр.")

    # Пользователь выбирает нужно ли ему обновлять БД.
    while True:
        try:
            users_input_update_bd = int(input(
                f"""{'_' * 100}\nЖелаете обновить базу данных по вакансиям?\n1 - Да, 2 - Нет.\n"""))
        except ValueError:
            print('Введите корректные данные!')
        else:
            if users_input_update_bd == 1:
                add_vacancies_to_db()
                break
            elif users_input_update_bd == 2:
                break
            else:
                print('Введите корректные данные!')

    while True:
        try:

            users_input_method = int(input(f"""{'_' * 100}\nКаким методом желаете воспользоваться?
1 - get_companies_and_vacancies_count(), Получает список всех компаний и количество вакансий у каждой компании.
2 - get_all_vacancies(), Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
3 - get_avg_salary(), Получает среднюю зарплату по вакансиям.
4 - get_vacancies_with_higher_salary(), Получает список всех вакансий, у которых минимальная и максимальная зарплата выше средней по всем вакансиям.
5 - get_vacancies_with_keyword(), Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
6 - Закончить работу программы, выйти.\n{'_' * 100}\n"""))

        except ValueError:
            print('Введите корректные данные!')
        else:
            manager_db = DBManager()
            if users_input_method == 1:
                manager_db.get_companies_and_vacancies_count()
            elif users_input_method == 2:
                manager_db.get_all_vacancies()
            elif users_input_method == 3:
                manager_db.get_avg_salary()
            elif users_input_method == 4:
                manager_db.get_vacancies_with_higher_salary()
            elif users_input_method == 5:
                users_input_keyword = input('Введите слово для поиска: ')
                manager_db.get_vacancies_with_keyword(users_input_keyword)
            elif users_input_method == 6:
                print('Выход!')
                break
            else:
                print('Введите корректные данные!')


user_interaction()
