from requests import request


class HeadHunterAPI:
    """Класс, для работы с платформой hh.ru.
    Класс уметь подключаться к API и информацию о работодателе и вакансиях."""

    __url = 'https://api.hh.ru/employers'

    def get_employers(self, name_employers=None, pages=1):
        """
        Получает компании по названию
        :param name_employers: str Название компании
        :param pages: int Количество компании
        :return:
        """
        req = request('GET', self.__url, params={
            'text': name_employers,
            'per_page': pages,
            'only_with_vacancies': True,
            'sort_by': 'by_vacancies_open'
        })

        return req.json()['items']

    def get_vacancy(self, url_vacancy):
        """
        Получение вакансии по ссылки
        :param url_vacancy: Ссылка вакансии
        :return: json файл
        """
        vac = request('GET', url_vacancy)
        if vac.json()['found'] == 0:
            return None
        return vac.json()['items']

    def calculate_salary_avg(self, salary_to, salary_from):
        """
        Получение средней зарплаты в рублях
        :param salary_to:int,None: начальная зарплата
        :param salary_from:int,None: конечная заплата
        :return:int
        """
        if salary_to is None:
            salary_to = 0
        if salary_from is None:
            salary_from = 0
        return int((salary_to + salary_from)/2)

    def get_json_list(self, name_company, count_company=1) -> list[dict]:
        """
        Возвращает список словорей информации по компании и вакансии
        :param name_company:
        :param count_company:
        :return:
        """
        data = []

        employer = self.get_employers(name_company, pages=count_company)
        for emp in employer:
            vacancy = self.get_vacancy(emp['vacancies_url'])
            if vacancy is not None:
                for v in vacancy:
                    if v['salary'] is None:
                        salary = None
                        currency = None
                    else:
                        salary = self.calculate_salary_avg(v['salary']['to'], v['salary']['from'])
                        currency = v['salary']['currency']

                    if v['address'] is None:
                        address = None
                    else:
                        address = v['address']['raw']

                    data.append({'id': v.get('id'),
                                 'name': v.get('name'),
                                 'salary': salary,
                                 'currency': currency,
                                 'address': address,
                                 'url': v.get('url')})
                emp['vacancy'] = data
                data = []

        return employer
