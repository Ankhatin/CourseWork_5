    Представляю консольную программу на Python для работы с вакансиями платформы hh.ru.
Программа в начале взаимодействия с пользователем просит ввести запрос со списком компаний-работодателей. 
По умолчанию список состоит из 10 компаний: ['яндекс', 'ozon', 'vk', 'сбер', 'банк втб (пао)', 'т-банк', 'авито', 
'wildberries', 'мтс', 'мегафон']. Далее программа отправляет запрос на hh.ru для поиска компаний и отбирает только те, 
название которых строго соответствует наименованиям из списка. Далее программа по ссылке, которая указана в информации о
работодателе, получает 100 открытых вакансий по каждой компании. Полученные данные программа сохраняет в таблицах
employers и vacansies базы данных PostgreSQL. Далее программа в ходе взаимодействия с пользователем предлагает получить
выборки данных из базы данных. Взаимодействие с базой данных реализовано через библиотеку psycopg2.
Пользователю предлагается получить следующие выборки из базы данных:
- список всех компаний и с общим количеством вакансий у каждой компании;
- список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию;
- средняя зарплата по всем вакансиям;
- список всех вакансий, у которых зарплата выше средней по всем вакансиям;
- список всех вакансий, в названии которых содержатся переданные в метод слова.
В случае, если у вакансии указаны значения зарплаты от и до, для последующих расчетов сначала рассчитывается средняя 
ЗП по данной вакансии.
    
  
