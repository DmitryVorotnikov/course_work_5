from __future__ import annotations

import json

import psycopg2
import requests


class HeadHunterAPI:
    """
    Класс для работы с API HeadHunter.
    """

    @staticmethod
    def get_request(employer_id: int, page: int) -> list:
        """
        Метод возвращает список-ответ от API с одной страницы.
        """
        params = {
            "employer_id": employer_id,
            "page": page,
            "per_page": 100,
        }
        return requests.get("https://api.hh.ru/vacancies", params=params).json()['items']

    def get_vacancies(self, employer_id: int) -> list:
        """
        Метод возвращает список-ответ от API с 5 страниц.
        """
        pages = 5
        response = []

        for page in range(pages):
            print(f'Парсинг страницы {page + 1}', end=': ')
            values = self.get_request(employer_id, page)
            print(f'Найдено {len(values)} вакансий.\n')
            response.extend(values)

        return response


class Vacancy:
    """
    Класс для работы с вакансиями.
    """
    __slots__ = (
        'title', 'salary_min', 'salary_max', 'currency', 'employer', 'link', 'salary_sort_min', 'salary_sort_max')

    def __init__(self, title: str, salary_min: int, salary_max: int, currency: str, employer: str, link: str) -> None:
        self.title = title  # Заголовок вакансии.
        self.salary_min = salary_min  # Минимальная зарплата.
        self.salary_max = salary_max  # Максимальная зарплата.
        self.currency = currency  # Валюта зарплаты.
        self.employer = employer  # Имя работодателя.
        self.link = link  # Ссылка на работодателя.

    def __str__(self) -> str:
        """
        Метод для печати в консоль вакансий.
        """
        return f'{self.employer}: {self.title} \n{self.salary_min} {self.salary_max} {self.currency} \nURL: {self.link}'


class JSONSaver:
    """
    Метод для работы с json файлом с вакансиями.
    """

    def __init__(self, employer_id: int) -> None:
        """
        Инициализатор сохранит в атрибут self.__filename название файла с вакансиями.
        """
        self.__filename = f'{employer_id}.json'

    @property
    def filename(self):
        return self.__filename

    def add_vacancies(self, data: list) -> None:
        """
        Метод создаст и перезапишет файл с вакансиями.
        """
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select_hh(self) -> list:
        """
        Метод прочтет файл с вакансиями из HeadHunter и создаст список с экземплярами класса Vacancy.
        """
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        vacancies = []

        for row in data:
            salary_min, salary_max, currency = None, None, None
            if row['salary']:
                salary_min, salary_max, currency = row['salary']['from'], row['salary']['to'], row['salary']['currency']
            vacancies.append(
                Vacancy(row['name'], salary_min, salary_max, currency, row['employer']['name'], row['alternate_url']))
        return vacancies


class DBManager:
    """
    Класс подключается к БД и производит выборку информации.
    """

    @staticmethod
    def get_companies_and_vacancies_count():
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        # Соединение с БД.
        conn = psycopg2.connect(host="localhost", database="course_work_5", user="postgres", password="04510451")
        try:
            with conn:
                with conn.cursor() as cur:
                    # Выполнение запросов.
                    cur.execute("SELECT name_company, COUNT(*) FROM vacancies GROUP BY name_company ORDER BY COUNT(*)")
                    rows = cur.fetchall()
                    print(f"Название компании, количество вакансий.")
                    for row in rows:
                        print(f"{row[0]}, {row[1]}")
        finally:
            # Закрытие соединения с БД.
            conn.close()

    @staticmethod
    def get_all_vacancies():
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        # Соединение с БД.
        conn = psycopg2.connect(host="localhost", database="course_work_5", user="postgres", password="04510451")
        try:
            with conn:
                with conn.cursor() as cur:
                    # Выполнение запросов.
                    cur.execute("SELECT name_company, title, salary_min, salary_max, link_vacancies FROM vacancies")
                    rows = cur.fetchall()
                    print(f"Название компании, название вакансии, зарплата минимальная, зарплата максимальная, URL.")
                    for row in rows:
                        print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}")
        finally:
            # Закрытие соединения с БД.
            conn.close()

    @staticmethod
    def get_avg_salary():
        """
        Получает среднюю зарплату по вакансиям.
        """
        # Соединение с БД.
        conn = psycopg2.connect(host="localhost", database="course_work_5", user="postgres", password="04510451")
        try:
            with conn:
                with conn.cursor() as cur:
                    # Выполнение запросов.
                    cur.execute("SELECT AVG(salary_min), AVG(salary_max) FROM vacancies")
                    rows = cur.fetchall()
                    print(f"Средняя минимальная зарплата, средняя максимальная зарплата.")
                    for row in rows:
                        print(f"{round(row[0])}, {round(row[1])}")
        finally:
            # Закрытие соединения с БД.
            conn.close()

    @staticmethod
    def get_vacancies_with_higher_salary():
        """
        Получает список всех вакансий, у которых минимальная и максимальная зарплата выше средней по всем вакансиям.
        """
        # Соединение с БД.
        conn = psycopg2.connect(host="localhost", database="course_work_5", user="postgres", password="04510451")
        try:
            with conn:
                with conn.cursor() as cur:
                    # Выполнение запросов.
                    cur.execute(
                        "SELECT * FROM vacancies "
                        "WHERE salary_min > (SELECT AVG(salary_min) FROM vacancies) "
                        "AND salary_max > (SELECT AVG(salary_max) FROM vacancies)")
                    rows = cur.fetchall()
                    print(
                        f"Название вакансии, минимальная зарплата, максимальная зарплата, "
                        f"валюта, название компании, URL.")
                    for row in rows:
                        print(f"{row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}")
        finally:
            # Закрытие соединения с БД.
            conn.close()

    @staticmethod
    def get_vacancies_with_keyword(keyword: str):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
        """
        # Соединение с БД.
        conn = psycopg2.connect(host="localhost", database="course_work_5", user="postgres", password="04510451")
        try:
            with conn:
                with conn.cursor() as cur:
                    # Выполнение запросов.
                    cur.execute(f"SELECT * FROM vacancies WHERE title LIKE '%{keyword}%'")
                    rows = cur.fetchall()
                    print(
                        f"Название вакансии, минимальная зарплата, максимальная зарплата, "
                        f"валюта, название компании, URL.")
                    for row in rows:
                        print(f"{row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}")
        finally:
            # Закрытие соединения с БД.
            conn.close()


def add_vacancies_to_db():
    """
    Функция для получения вакансий по API, сохранение в json-файлах, заполнения таблиц в БД 'course_work_5'.
    """
    ten_companies = {'МТС': 3776, 'Газпромбанк': 3388, 'Московский Кредитный Банк': 2492,
                     'ПАО Совкомбанк': 7944, 'Альфа Банк': 80, 'Тензор': 67611,
                     'Билайн': 4934, 'Яндекс': 1740, 'АО Россельхозбанк': 58320, 'Банк Открытие': 23040}

    # Цикл по одной компании.
    for employer_id in ten_companies.values():
        # Создание экземпляра класса для работы с API сайта с вакансиями.
        hh_api = HeadHunterAPI()
        # Получение вакансий с разных платформ.
        hh_vacancies = hh_api.get_vacancies(employer_id)
        # Сохранение информации о вакансиях в файл user_input_keyword.json и переменную data.
        json_saver = JSONSaver(employer_id)
        json_saver.add_vacancies(hh_vacancies)
        data = json_saver.select_hh()

        # Соединение с БД.
        conn = psycopg2.connect(host="localhost", database="course_work_5", user="postgres", password="04510451")
        # Создание курсора.
        cur = conn.cursor()
        try:
            # Выполнение запросов.
            for row in data:
                cur.executemany(
                    "INSERT INTO vacancies(title, salary_min, salary_max, currency, name_company, link_vacancies) VALUES (%s, %s, %s, %s, %s, %s)",
                    [(row.title, row.salary_min, row.salary_max, row.currency, row.employer, row.link)])
            conn.commit()
        finally:
            # Закрытие соединения с БД и курсора.
            cur.close()
            conn.close()
