from src.api_hh import HeadHunterAPI
from src.manager_base import DBManager
from src.utils_database import *


def found_employers(name_bd, params):
    connect_hh = HeadHunterAPI()

    while True:
        name_comp = input('Введите название компании')
        count_comp = input('Введите их количество')

        employers = connect_hh.get_json_list(name_comp, count_comp)
        save_data_to_database(employers, name_bd, params)

        continue_comp = input('Продолжить? - 1\n'
                              'Закончить? - 0')
        if continue_comp == '1':
            continue
        else:
            break


def sorter_date(name_bd, params):
    manager = DBManager(name_bd, params)
    while True:
        answer = input('Введите:\n'
                       '1 - получить список всех компаний и количество вакансий у каждой компании.\n'
                       '2 - получить список всех вакансий с указаными данными\n'
                       '3 - получить среднюю зарплату по вакансиям\n'
                       '4 - получать список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n'
                       '5 - получает список всех вакансий, в названии которых содержатся переданные в метод слова\n'
                       )
        if answer == '1':
            manager.get_companies_and_vacancies_count()
            continue
        else:
            break


def main():
    params = open_params_config()
    name_bd = input('Введите название базы данных для сохранения')

    create_database(name_bd, params)
    create_table(name_bd, params)
    while True:
        answer = input('Введите:\n'
                       '1 - для поиска интересующих компаний и их сохранения\n'
                       '2 - для работы данными и сортировки\n'
                       '0 - для выхода')
        if answer == '1':
            found_employers(name_bd, params)
            continue
        elif answer == '2':
            sorter_date(name_bd, params)
            continue
        else:
            break


if __name__ == '__main__':
    main()
