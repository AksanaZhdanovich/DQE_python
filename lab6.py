from datetime import datetime
import os
import lab10
import lab4
import lab7
import lab8
import lab9


class NewInformation:
    file_to_write = 'newsfeed.txt'
    length_of_description = 30
    end_record = '-' * length_of_description

    def __init__(self, note_text):
        self.note = note_text
        self.text_in_file = ''
        self.type_of_info = ''
        self.file_to_write = NewInformation.file_to_write

    def add_new_info_in_the_file(self):
        with open(self.file_to_write, "a") as text_file:
            text_file.write(self.text_in_file + '\n\n')
        create_files_csv()
        print('The information was added\n')

    def info_description(self):
        return self.type_of_info + ' ' + '-' * (
                    self.length_of_description - len(self.type_of_info)) + '\n' + self.note + '\n'


class AddNews(NewInformation):

    def __init__(self, note_text, city):
        super().__init__(note_text=note_text)
        self.datetime_news = datetime.now().strftime('%d/%m/%Y %H.%M')
        self.type_of_info = 'News'
        self.description = NewInformation.info_description(self)
        self.city = city
        self.text_in_file = self.description + self.city + ',' + self.datetime_news + '\n' + self.end_record + '\n'
        self.add_new_info_in_the_file()
        news_to_db = lab10.PostgreSqlInsert()
        lab10.PostgreSqlInsert.insert_new_records_news(news_to_db, self.type_of_info, note_text, self.city,
                                                       self.datetime_news, '')


class AddAd(NewInformation):

    def __init__(self, note_text, date):
        super().__init__(note_text=note_text)
        self.date = date
        self.expire_date = str((datetime.strptime(self.date, '%d/%m/%Y') - datetime.now()).days + 1)
        self.type_of_info = 'Private Ad'
        self.description = NewInformation.info_description(self)
        self.text_in_file = self.description + 'Actual until: ' + self.date + ', ' + self.expire_date + ' days left.' \
                            + '\n' + self.end_record + '\n'
        self.add_new_info_in_the_file()
        news_to_db = lab10.PostgreSqlInsert()
        lab10.PostgreSqlInsert.insert_new_records_news(news_to_db, self.type_of_info, note_text, '',
                                                       self.date, '')


class AddWeatherForecast(NewInformation):
    def __init__(self, note_text, city, date, degrees):
        super().__init__(note_text=note_text)
        self.date = date
        self.degrees = degrees
        self.city = city
        self.type_of_info = 'Weather Forecast'
        self.description = NewInformation.info_description(self)
        self.text_in_file = self.description + 'Temperature: ' + self.degrees + ' in ' + self.city + \
                            ' Date:' + self.date + '\n' + self.end_record + '\n'
        self.add_new_info_in_the_file()
        news_to_db = lab10.PostgreSqlInsert()
        lab10.PostgreSqlInsert.insert_new_records_news(news_to_db, self.type_of_info, note_text, self.city, self.date,
                                                       self.degrees)


class NewRecordsFromFile:
    default_folder = str(os.path.abspath(os.curdir))

    def __init__(self, count_of_records, name_of_txt_file, folder_to_load=default_folder):
        self.name_of_txt_file = name_of_txt_file
        self.count_of_records = int(count_of_records)
        self.folder_to_load = folder_to_load
        self.full_path = os.path.join(self.folder_to_load, self.name_of_txt_file)
        self.cnt_of_all_records = 0
        self.line_to_insert = ''
        self.dict_of_news = []

    def is_file_exists(self):
        if os.path.exists(self.full_path):
            return True
        else:
            return False

    def len_of_reading_file(self):
        return sum(1 for _ in open(self.full_path, 'r'))

    def read_from_file(self):
        cnt_of_records_in_file = 0
        if NewRecordsFromFile.is_file_exists(self):
            with open(self.full_path, 'r') as file_info_inserted:
                self.count_of_records = NewRecordsFromFile.count_of_records_less_then_len_of_file(self)
                while (cnt_of_records_in_file < self.count_of_records) and (
                        self.cnt_of_all_records < self.len_of_reading_file()):
                    cur_line_of_file = file_info_inserted.readline()
                    if (NewInformation.end_record not in cur_line_of_file) and (cur_line_of_file != ''):
                        self.line_to_insert += lab4.sentence_with_capit_letters((cur_line_of_file.split('. ')))
                        self.dict_of_news.append(lab4.sentence_with_capit_letters((cur_line_of_file.split('. '))))
                        self.cnt_of_all_records += 1
                    elif (NewInformation.end_record in cur_line_of_file) and (cur_line_of_file != '\n') \
                            and (cur_line_of_file != ''):
                        cnt_of_records_in_file += 1
                        self.cnt_of_all_records += 1
                        self.line_to_insert += cur_line_of_file
                        self.dict_of_news.append(cur_line_of_file)
                    elif cur_line_of_file == '':
                        cnt_of_records_in_file = self.len_of_reading_file()
            self.line_to_insert += '\n'
        return self.line_to_insert

    def insert_into_file(self):
        if self.is_file_exists:
            with open(NewInformation.file_to_write, 'a') as file_for_insert:
                file_for_insert.write(self.read_from_file())
                #print(self.line_to_insert)
                self.proceed_txt()
                print('New data was added into file')
            create_files_csv()

    def remove_file(self):
        if self.is_file_exists:

            if self.cnt_of_all_records >= self.len_of_reading_file():
                os.remove(self.full_path)
                print(f'File {self.full_path} was deleted')

    def count_of_records_less_then_len_of_file(self):
        len_of_file = self.len_of_reading_file()
        if self.count_of_records * 4 >= len_of_file:
            print('WARNING! You chose more records for load than in file, the whole file will be loaded')
        return self.count_of_records

    def proceed_txt(self):
        text_file_in_dict = self.line_to_insert.split('\n')
        delim = '-' * 30
        cnt_elem = 0
        while cnt_elem in range(len(text_file_in_dict)):
            text = ''
            if 'NEWS' in text_file_in_dict[cnt_elem].upper():
                start_feed = cnt_elem
                while delim not in text_file_in_dict[cnt_elem]:
                    cnt_elem += 1
                else:
                    end_feed = cnt_elem
                type_of_news = 'NEWS'
                city_time_news = text_file_in_dict[end_feed - 1]
                cnt = 0
                while city_time_news[cnt] != ',':
                    cnt += 1
                city_news = city_time_news[0: cnt]
                date_time_news = city_time_news[cnt + 2::]
                start_feed += 1
                while start_feed < end_feed - 1:
                    text += text_file_in_dict[start_feed]
                    start_feed += 1
                news_to_db = lab10.PostgreSqlInsert()
                lab10.PostgreSqlInsert.insert_new_records_news(news_to_db, type_of_news, text, city_news, date_time_news, '')
                text = ''
            if 'PRIVATE AD' in text_file_in_dict[cnt_elem].upper():
                start_feed = cnt_elem
                while delim not in text_file_in_dict[cnt_elem]:
                    cnt_elem += 1
                else:
                    end_feed = cnt_elem
                type_of_news = 'PRIVATE AD'
                date_news = (text_file_in_dict[end_feed - 1]).replace('Actual until: ', '')
                cnt = 0
                while date_news[cnt] != ',':
                    cnt += 1
                date_time_news = date_news[0: cnt]
                start_feed += 1
                while start_feed < end_feed - 1:
                    text += text_file_in_dict[start_feed]
                    start_feed += 1
                news_to_db = lab10.PostgreSqlInsert()
                lab10.PostgreSqlInsert.insert_new_records_news(news_to_db, type_of_news, text, '', date_time_news, '')
                text = ''
            if 'WEATHER FORECAST' in text_file_in_dict[cnt_elem].upper():
                start_feed = cnt_elem
                while delim not in text_file_in_dict[cnt_elem]:
                    cnt_elem += 1
                else:
                    end_feed = cnt_elem
                type_of_news = 'WEATHER FORECAST'
                date_news = (((text_file_in_dict[end_feed - 1]).replace('Temperature: ', '')).replace(' in ', ' ')).replace('date:', '')
                date_tem_city = date_news.split()
                temperature = date_tem_city[0]
                city_news = date_tem_city[1].capitalize()
                date_time_news = date_tem_city[2]
                start_feed += 1
                while start_feed < end_feed - 1:
                    text += text_file_in_dict[start_feed]
                    start_feed += 1
                news_to_db = lab10.PostgreSqlInsert()
                lab10.PostgreSqlInsert.insert_new_records_news(news_to_db, type_of_news, text, city_news, date_time_news, temperature)
            cnt_elem += 1

def create_files_csv():
    file_to_prov = lab7.CsvProcessing(NewInformation.file_to_write)
    lab7.CsvProcessing.write_to_file(file_to_prov)
    lab7.CsvProcessing.write_to_file_letters(file_to_prov)


def validation_date(type_of_info):
    input_date = input(f'Please write the date for {type_of_info} in format DD/MM/YYYY:\n')
    try:
        datetime.strptime(input_date, '%d/%m/%Y')
        return input_date
    except ValueError:
        print('Invalid date! Please try again!')
        return validation_date(type_of_info)


def validation_count_of_records_type():
    count_of_records = input('Write count of records to load in the file:\n')
    try:
        int(count_of_records)
        return abs(int(count_of_records))
    except ValueError:
        print('Count of records should be an int value!')
        return validation_count_of_records_type()


def type_new_info():
    type_of_feed = ''
    while type_of_feed != '0':
        type_of_feed = input('Choose number to add info:\n' + '1 - add news\n' + '2 - add private ad\n' +
                             '3 - add weather forecast\n' + '0 - quit\n' + 'Your choice:\n')
        if type_of_feed not in ['0', '1', '2', '3']:
            print(f'Your choice is "{type_of_feed}" and it is not an expected value, please try again')
        elif type_of_feed == '1':
            print('Your choice is 1 - add news:')
            news_text = input('Please type the text of your news:\n> ').capitalize()
            news_city = input('Please type the city:\n').capitalize()
            AddNews(news_text, news_city)
        elif type_of_feed == '2':
            print('Your choice is 2 - add ad:')
            ad_text = input('Please type the text of your private ad:\n> ').capitalize()
            ad_date = validation_date('Ad')
            print('ad_date', ad_date)
            AddAd(ad_text, ad_date)
        elif type_of_feed == '3':
            print('Your choice is 3 - add weather forecast:')
            forecast_text = input('Please type the forecast:\n').capitalize()
            forecast_date = validation_date('Weather forecast ')
            forecast_city = input('Please type the city:\n').capitalize()
            forecast_temperature = input('Please type temperature:\n')
            AddWeatherForecast(forecast_text, forecast_city, forecast_date, forecast_temperature)
    else:
        print(f'All the information is in the file {NewInformation.file_to_write}')


def load_from_file():
    type_of_file = input('Choose the type of the loaded file: 1 - txt, 2 - json, 3 - xml,  0 - exit:\n')
    if type_of_file not in ['0', '1', '2', '3']:
        print(f'Your choice is "{type_of_file}" and it is not an expected value, please try again')
    elif type_of_file in ['1', '2', '3']:
        folder_to_load_data = input(
            f'Type path to the file(if it is empty will be a current path {NewRecordsFromFile.default_folder}):\n')
        records_to_load = validation_count_of_records_type()
        file_name = input('Type file name:\n')
        file_to_load = NewRecordsFromFile(records_to_load, file_name, folder_to_load_data)
        if NewRecordsFromFile.is_file_exists(file_to_load):
            if type_of_file == '1':
                NewRecordsFromFile.insert_into_file(file_to_load)
                NewRecordsFromFile.remove_file(file_to_load)
            if type_of_file == '2':
                file_to_load = lab8.JsonProcess(records_to_load, file_name, folder_to_load_data)
                if lab8.JsonProcess.is_file_can_be_processed(file_to_load):
                    lab8.JsonProcess.proceed_dict_json(file_to_load, lab8.JsonProcess.read_from_json(file_to_load))
                    print('The data was added into file\n')
                    lab8.JsonProcess.delete_json(file_to_load)
            if type_of_file == '3':
                file_to_load = lab9.ProcessXml(records_to_load, file_name, folder_to_load_data)
                lab9.ProcessXml.xml_to_list_of_dicts(file_to_load)
                lab9.ProcessXml.proceed_dict_xml(file_to_load)
                print('The data was added into file\n')
                lab9.ProcessXml.delete_xml(file_to_load)
        else:
            print('Wrong file or path - data was not inserted!')


def main_menu():
    print(' Hi, welcome to our news feed.')
    work_with_db = ''
    while work_with_db != '0':
        mode_type = ''
        work_with_db = input('Would you like to add info into empty DB tables or insert into existed? 1 - empty tables,'
                             ' 2 - exist tables, 3- duplicate check 0 - exit\n')
        if work_with_db not in ['0', '1', '2', '3']:
            print(f'Your choice is "{work_with_db}" and it is not an expected value, please try again')
        elif work_with_db in ['1', '2', '3']:
            if work_with_db == '3':
                duplic = lab10.PostgreSqlInsert()
                lab10.PostgreSqlInsert.duplicate(duplic)
            while mode_type != '0' and work_with_db in ['1', '2']:
                if work_with_db == '1':
                    lab10.create_tables()
                mode_type = input(
                    ' Would you like to type info or load from file? 1 - type, 2 - load from file, 0 - exit\n')
                if mode_type not in ['0', '1', '2']:
                    print(f'Your choice is "{mode_type}" and it is not an expected value, please try again')
                elif mode_type == '1':
                    type_new_info()
                elif mode_type == '2':
                    load_from_file()
            else:
                print('Return to previous level')
    else:
        print('The program finished working.')


if __name__ == "__main__":
    main_menu()
