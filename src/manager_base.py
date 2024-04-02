from configparser import ConfigParser


class DBManager:
    """
    Класс, который будет подключаться к БД PostgreSQL
    """
    def config(filename="database.ini", section="postgresql"):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(
                'Section {0} is not found in the {1} file.'.format(section, filename))
        return db

    def get_companies_and_vacancies_count(self):
       """
        — получает список всех компаний и количество вакансий у каждой компании.
       :return:
       """

    def get_all_vacancies(self):
        """
         — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        :return:
        """

    def get_avg_salary(self):
        """
         — получает среднюю зарплату по вакансиям.
        :return:
        """

    def get_vacancies_with_higher_salary(self):
        """
         — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return:
        """

    def get_vacancies_with_keyword():
        """
         — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        :return:
        """
