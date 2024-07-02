import psycopg2


class DBManager:
    '''
    Класс для работы с базой данных PostgreSQL
    '''
    def __init__(self, database_name):
        self.database_name = database_name
        self.params = {'host': 'localhost', 'user': 'postgres', 'password': '12345'}

    def create_database(self):
        '''
        Метод создает базу данных, если она не существует
        '''
        conn = psycopg2.connect(database='postgres', **self.params)
        with conn.cursor() as cursor:
            conn.autocommit = True
            try:
                psycopg2.connect(database=self.database_name, **self.params)
            except Exception:
                cursor.execute(f"CREATE DATABASE {self.database_name}")
        conn.close()

    def create_tables(self):
        '''
        Метод создает таблицы в базе данных для заполнения данными
        '''
        conn = psycopg2.connect(database=self.database_name, **self.params)
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS employers CASCADE")
            cursor.execute("DROP TABLE IF EXISTS vacancies")
            cursor.execute('''CREATE TABLE employers
                                (employer_name varchar(30) PRIMARY KEY,
                                employer_url varchar(50) not null);
                                ''')
            cursor.execute('''CREATE TABLE vacancies
                                (vacancy_id serial,
                                employer_name varchar(30),
                                vacancy_name varchar(100) not null,
                                vacancy_url varchar(50) not null,
                                salary_from int,
                                salary_to int,
                                CONSTRAINT fk_vacancies_employer FOREIGN KEY(employer_name) REFERENCES employers(employer_name));
                                ''')
            conn.commit()
        conn.close()

    def write_data(self, employers, vacancies):
        '''
        Метод заполняем таблицы базны данных данными о работодателях и их вакансиях
        '''
        with psycopg2.connect(database=self.database_name, **self.params) as conn:
            with conn.cursor() as cursor:
                for employer in employers:
                    cursor.execute("INSERT INTO employers (employer_name, employer_url) VALUES (%s, %s);", employer)
                for vacancy in vacancies:
                    cursor.execute("INSERT INTO vacancies (employer_name, vacancy_name, vacancy_url, salary_from, salary_to)"
                                   "VALUES (%s, %s, %s, %s, %s);", vacancy)
            conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self):
        '''
        Метод получает список всех компаний и количество вакансий у каждой компании
        '''
        with psycopg2.connect(database=self.database_name, **self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''SELECT employer_name, COUNT(*) 
                                FROM vacancies
                                GROUP BY employer_name
                                ORDER BY COUNT(*) DESC;''')
                companies = cursor.fetchall()
        conn.close()
        return companies

    def get_all_vacancies(self):
        '''
        Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        Возвращает список вакансий
        '''
        with psycopg2.connect(database=self.database_name, **self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''SELECT employer_name, vacancy_name, salary_from, salary_to, vacancy_url
                                FROM vacancies
                                ORDER BY employer_name''')
                vacancies = cursor.fetchall()
        conn.close()
        return vacancies

    def get_avg_salary(self):
        '''
        Метод получает среднюю зарплату по вакансиям
        '''
        with psycopg2.connect(database=self.database_name, **self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''SELECT AVG(average_salary)
                                FROM (SELECT AVG((salary_from + salary_to)/2) AS average_salary
                                FROM vacancies
                                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
                                UNION
                                SELECT AVG(salary_from) AS average_salary
                                FROM vacancies
                                WHERE salary_to IS NULL
                                UNION
                                SELECT AVG(salary_to) AS average_salary
                                FROM vacancies
                                WHERE salary_from IS NULL);''')
                average_salary = cursor.fetchone()[0]
        conn.close()
        return average_salary

    def get_vacancies_with_higher_salary(self, average_salary):
        '''
        Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        '''
        with psycopg2.connect(database=self.database_name, **self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'''SELECT * FROM vacancies
                                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
                                AND (salary_from + salary_to)/2 > {average_salary}
                                UNION
                                SELECT * FROM vacancies
                                WHERE salary_to IS NULL
                                AND salary_from > {average_salary}
                                UNION
                                SELECT * FROM vacancies
                                WHERE salary_from IS NULL
                                AND salary_to > {average_salary}
                                ORDER BY vacancy_id;''')
                vacancies_list = cursor.fetchall()
        conn.close()
        return vacancies_list

    def get_vacancies_with_keyword(self, words):
        '''
        Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова
        '''
        with psycopg2.connect(database=self.database_name, **self.params) as conn:
            with conn.cursor() as cursor:
                first_word = words[0] # по первому поисковому слову получаем выборку из базы данных
                first_word_upper = first_word.title()
                first_word = first_word.center(len(first_word)+2, '%') # добавляем символы % в начало и конец слова
                first_word_upper = first_word_upper.center(len(first_word_upper)+2, '%')
                cursor.execute(f'''SELECT * FROM vacancies
                                WHERE vacancy_name LIKE '{first_word}' OR 
                                vacancy_name LIKE '{first_word_upper}';''')
                vacancies_list = cursor.fetchall()
                if len(words) > 1: # если в поисковом запросе несколько слов фультруем по ним полученный из БД список
                    vacancies_filtered = []
                    for word in words[1:]:
                        for vacancy in vacancies_list:
                            if word in vacancy[2]:
                                vacancies_filtered.append(vacancy)
                    vacancies_list = vacancies_filtered
        conn.close()
        return vacancies_list
