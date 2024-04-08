import psycopg2


class DBManager:
    """
    Класс, который будет подключаться к БД PostgreSQL
    """

    def __init__(self, name_base, params):
        self.name_base = name_base
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        — получает список всех компаний и количество вакансий у каждой компании.
       :return:
       """
        conn = psycopg2.connect(dbname=self.name_base, **self.params)

        with conn.cursor() as cur:
            cur.execute("""SELECT company_name, COUNT(*) AS count_vacancy
                            FROM employers
                            JOIN vacancy USING(employer_id)
                            GROUP BY company_name
                            """)
        conn.close()

    def get_all_vacancies(self):
        """
         — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        :return:
        """
        conn = psycopg2.connect(dbname=self.name_base, **self.params)

        with conn.cursor() as cur:
            cur.execute("""SELECT company_name, name_vacancy, salary, currency, vacancy_url
                            FROM vacancy
                            JOIN employers USING(employer_id)
                            """)
        conn.close()

    def get_avg_salary(self):
        """
         — получает среднюю зарплату по вакансиям.
        :return:
        """
        conn = psycopg2.connect(dbname=self.name_base, **self.params)

        with conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary)
                            FROM vacancy""")
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """
         — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return:
        """
        conn = psycopg2.connect(dbname=self.name_base, **self.params)

        with conn.cursor() as cur:
            cur.execute("""SELECT name_vacancy, salary
                            FROM vacancy
                            WHERE salary >= (SELECT AVG(salary) from vacancy)
                            """)
        conn.close()

    def get_vacancies_with_keyword(self, found_name):
        """
         — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        :return:
        """
        conn = psycopg2.connect(dbname=self.name_base, **self.params)

        with conn.cursor() as cur:
            cur.execute(f"""SELECT name_vacancy, salary
                            FROM vacancy
                            WHERE name_vacancy LIKE('%{found_name}%')
                        """)
        conn.close()
