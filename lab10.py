import connect_to_db
import psycopg2


class PostgreSqlInsert:
    def __init__(self):
        self.dbname = 'news_feed'
        self.table_names = [f'{connect_to_db.database}.public.news', f'{connect_to_db.database}.public.private_ad',
                            f'{connect_to_db.database}.public.weather_forecast']
        self.queries_for_duplicate = [
            f'''SELECT 
                                     text
                                   , city
                                   , date_time
                                  
                                 FROM {self.table_names[0]}
                                 GROUP BY 
                                     text
                                   , city
                                   , date_time
                                 HAVING count(*) > 1
                             ''',
            f'''SELECT 
                                         text
                                       , date
                                  FROM {self.table_names[1]}
                                     GROUP BY 
                                         text
                                       , date
                                     HAVING count(*) > 1
                                   ''',
            f'''SELECT 
                                      text
                                    , temperature
                                    , city
                                    , date
                                  FROM {self.table_names[2]}
                                  GROUP BY 
                                      text
                                    , temperature
                                    , city
                                    , date
                                  HAVING count(*) > 1''']

    def duplicate(self):
        connection = connect()
        cursor = connection.cursor()
        for query_for_dupl in self.queries_for_duplicate:
            cursor.execute(query_for_dupl)
            records = cursor.fetchall()
            if not records:
                print(f'In the table {self.table_names[self.queries_for_duplicate.index(query_for_dupl)]} 0 duplicates')
            else:
                print(f'Duplicates in table {self.table_names[self.queries_for_duplicate.index(query_for_dupl)]}:''',
                      *records)

    def insert_new_records_news(self, type_of_news, text, city, date_time, temperature):
        connection = connect()
        cursor = connection.cursor()
        connection.set_session(autocommit=True)
        if type_of_news.upper() == 'NEWS':
            cursor.execute(
                f'''INSERT INTO {self.table_names[0]} (text, city, date_time)
                            VALUES ('{text}','{city}','{date_time}');''')
        if type_of_news.upper() == 'PRIVATE AD':
            cursor.execute(
                f'''INSERT INTO {self.table_names[1]} (text, date)
                            VALUES ('{text}','{date_time}');''')
        if type_of_news.upper() == 'WEATHER FORECAST':
            cursor.execute(
                f'''INSERT INTO {self.table_names[2]} (text, temperature, city, date)
                            VALUES ('{text}','{temperature}','{city}','{date_time}');''')


def connect():
    try:
        return psycopg2.connect(
            user=connect_to_db.user,
            password=connect_to_db.password,
            host=connect_to_db.host,
            port=connect_to_db.port,
            database=connect_to_db.database)
    except "Error" as connection_error:
        print(connection_error)


def create_tables():
    connection = connect()
    cursor = connection.cursor()
    connection.set_session(autocommit=True)
    cursor.execute(f'''DROP TABLE IF EXISTS {connect_to_db.database}.public.news''')
    cursor.execute(f'''CREATE TABLE {connect_to_db.database}.public.news(
                        text varchar
                       ,city varchar
                       ,date_time varchar)''')

    cursor.execute(f'''DROP TABLE IF EXISTS {connect_to_db.database}.public.private_ad''')
    cursor.execute(f'''CREATE TABLE {connect_to_db.database}.public.private_ad(
                         text varchar
                        ,date varchar)''')

    cursor.execute(f'''DROP TABLE IF EXISTS {connect_to_db.database}.public.weather_forecast''')
    cursor.execute(f'''CREATE TABLE {connect_to_db.database}.public.weather_forecast(
                         text varchar
                        ,temperature varchar
                        ,city varchar
                        ,date varchar)''')
