import requests
from abc import ABC, abstractmethod


class Parser(ABC):

    @abstractmethod
    def load_data(self, keyword):
        pass


class HeadHunterAPI(Parser):
    '''
    Класс для работы с работодателями и вакансиями, загруженными с платформы hh.ru
    '''
    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'only_with_vacancies': True, 'only_with_salary': True, 'page': 0, 'per_page': 10}

    def load_data(self, keyword=None, per_page=10):
        '''
        Функция отправляет запрос на платформу hh.ru,
        загружает данные и возращает в виде списка словарей
        '''
        employers_list: list[dict] = []
        self.params['text'] = keyword
        self.params['per_page'] = per_page
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            employers_list = response.json()['items']
            return employers_list


