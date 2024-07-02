from src.DBManager import *
from src.functions import *
import os.path

ROOT_DIR = os.path.dirname(__file__)

def user_interaction():
    '''
    Функция организует взаимодействие с пользователем
    '''
    search_query = input('''Введите названия компаний через запятую, вакансии которых хотите получить из hh.ru
    или Enter, чтобы загрузить компании по умолчанию: ''')
    if search_query:
        search_list = search_query.lower().split(', ')
    else:
        search_query = ['яндекс', 'ozon', 'vk', 'сбер', 'банк втб (пао)', 'т-банк',
                        'авито', 'wildberries', 'мтс', 'мегафон']
    employers, vacancies = get_data_from_hh(search_query)
    db_manager.write_data(employers, vacancies)
    companies = db_manager.get_companies_and_vacancies_count()
    if input("Вывести список компаний с количеством вакансий в каждой компании, да или Enter, чтобы пропустить: "):
        for company in companies:
            print(f'Компания: {company[0]}, количество вакансий: {company[1]}')
    all_vacancies = db_manager.get_all_vacancies()
    if input("Вывести список всех вакансий, да или Enter, чтобы пропустить: "):
        for vacancy in all_vacancies:
            print(f'Компания: {vacancy[1]}, вакансия: {vacancy[2]}, ссылка: {vacancy[3]}, зарплата от: {vacancy[4]}, '
                  f'зарплата до: {vacancy[5]}')
    average_salary = round(db_manager.get_avg_salary()) # получаем средную зп по всем вакансиям
    print(f'Средняя зарплата по вакансиям: {average_salary} руб.')
    # получаем список вакансий с зарплатой выше средней по всем вакансиям
    vacancies_list = db_manager.get_vacancies_with_higher_salary(average_salary)
    if input('''Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям, да или Enter,
             чтобы пропустить: '''):
        for vacancy in vacancies_list:
            print(f'Компания: {vacancy[1]}, вакансия: {vacancy[2]}, ссылка: {vacancy[3]}, зарплата от: {vacancy[4]}, зарплата до: {vacancy[5]}')
    search_words = input('''Введите ключевые слова через пробел для поиска в наименовании вакансии, или Enter, чтобы пропустить: ''')
    if search_words:
        search_words = search_words.lower().split()
        vacancies_list = db_manager.get_vacancies_with_keyword(search_words)
        for vacancy in vacancies_list:
            print(f'Компания: {vacancy[1]}, вакансия: {vacancy[2]}, ссылка: {vacancy[3]}, зарплата от: {vacancy[4]}, зарплата до: {vacancy[5]}')

if __name__ == '__main__':
    # Инициализируем объект для работы базой данных PostgreSQL
    db_manager = DBManager('hh_data')
    db_manager.create_database() # создаем базу данных, если ещё не существует
    db_manager.create_tables() # создаем таблицы
    user_interaction()




