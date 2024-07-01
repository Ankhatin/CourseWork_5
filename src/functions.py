from src.webServicesAPI import HeadHunterAPI


def load_data_from_hh(keywords):
    '''
    Функция выполняет запросы к hh.ru для получения списка компаний
    и списка вакансий в данных компаниях.
    Возвращает список компаний и список вакансий
    '''
    employers_list: list[list] = []
    vacancies_list: list[list] = []
    employer_request = HeadHunterAPI('https://api.hh.ru/employers') # инициализуем объект для запроса компаний
    for word in keywords: # цикл по названиям компаний
        employers = employer_request.load_data(word) # выполняем запрос для поиска и загрузки компаний
        for employer in employers: # в цикле проходим по компаниям с похожими названиями, ищем строгое соответствие
            if employer['name'].lower() in keywords:
                employer_data = [employer['name'], employer['alternate_url']]
                employers_list.append(employer_data) # получили искомую компанию, поместили в список
                vacancies_url = employer['vacancies_url'] # ссылка для получения вакансий в данной компании
                vacancies_request = HeadHunterAPI(vacancies_url) # инициализируем объект для запроса вакансий
                vacancies = vacancies_request.load_data(per_page=100) # выполняем запрос для загрузки вакансий
                for vacancy in vacancies:
                    vacancy_data = [employer['name'], vacancy['name'], vacancy['alternate_url'], vacancy['salary']['from'], vacancy['salary']['to']]
                    vacancies_list.append(vacancy_data) # поместили вакансию в список
    return employers_list, vacancies_list




