from configparser import ConfigParser
from typing import Any
import psycopg2
from settertion import NAME_DIR


def open_params_config(filename=NAME_DIR, section="postgresql"):
    """
    Получает секретные данные для Базы данных
    :param filename: файл кодов для входа
    :param section: ключ
    :return:dict: список данных
    """
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


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о компании и вакансиях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()


def create_table(database_name: str, params: dict):
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                open_vacancy INTEGER,
                employer_url TEXT
            );
            
            CREATE TABLE vacancy (
                vacancy_id INTEGER PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                name_vacancy VARCHAR NOT NULL,
                average_salary INT,
                currency VARCHAR(7),
                vacancy_url TEXT,
                address VARCHAR(255)
            )"""
                    )

    conn.commit()
    conn.close()


def save_data_to_database(employers: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о каналах и видео в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in employers:

            cur.execute(
                """
                INSERT INTO employers (employer_id, company_name, open_vacancy, employer_url)
                VALUES (%s, %s, %s, %s)
                """,
                (employer['id'], employer['name'], employer['open_vacancies'], employer['alternate_url'])
            )

            vacancy_employer = employer['vacancy']

            for vacancy in vacancy_employer:
                cur.execute(
                    """
                    INSERT INTO vacancy (vacancy_id, employer_id, name_vacancy, average_salary, currency, vacancy_url, address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (vacancy['id'], employer['id'], vacancy['name'], vacancy['salary'],
                     vacancy['currency'], vacancy['url'], vacancy['address'])
                )

    conn.commit()
    conn.close()