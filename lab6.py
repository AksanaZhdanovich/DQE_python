from datetime import datetime
import os
import lab4
import lab7


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
        return self.type_of_info + '-' * (self.length_of_description - len(self.type_of_info)) + '\n' + self.note + '\n'


class AddNews(NewInformation):

    def __init__(self, note_text, city):
        super().__init__(note_text=note_text)
        self.datetime_news = datetime.now().strftime('%d/%m/%Y %H.%M')
        self.type_of_info = 'News '
        self.description = NewInformation.info_description(self)
        self.city = city
        self.text_in_file = self.description + self.city + ',' + self.datetime_news + '\n' + self.end_record + '\n'
        self.add_new_info_in_the_file()


class AddAd(NewInformation):

    def __init__(self, note_text, date):
        super().__init__(note_text=note_text)
        self.date = date
        self.expire_date = str((datetime.strptime(self.date, '%d/%m/%Y') - datetime.now()).days + 1)
        self.type_of_info = 'Private Ad '
        self.description = NewInformation.info_description(self)
        self.text_in_file = self.description + 'Actual until: ' + self.date + ', ' + self.expire_date + ' days left.' \
                            + '\n' + self.end_record + '\n'
        self.add_new_info_in_the_file()


class AddWeatherForecast(NewInformation):
    def __init__(self, note_text, city, date, degrees):
        super().__init__(note_text=note_text)
        self.date = date
        self.degrees = degrees
        self.city = city
        self.type_of_info = 'Weather Forecast '
        self.description = NewInformation.info_description(self)
        self.text_in_file = self.description + 'Temperature: ' + self.degrees + ' in ' + self.city + \
                            ' Date:' + self.date + '\n' + self.end_record + '\n'
        self.add_new_info_in_the_file()


class NewRecordsFromFile:
    default_folder = str(os.path.abspath(os.curdir))

    def __init__(self, count_of_records, name_of_txt_file, folder_to_load=default_folder):
        self.name_of_txt_file = name_of_txt_file
        self.count_of_records = int(count_of_records)
        self.folder_to_load = folder_to_load
        self.full_path = os.path.join(self.folder_to_load, self.name_of_txt_file)
        self.cnt_of_all_records = 0
        self.line_to_insert = ''

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
                while (
                        cnt_of_records_in_file < self.count_of_records) and (
                        self.cnt_of_all_records < self.len_of_reading_file()):
                    cur_line_of_file = file_info_inserted.readline()
                    if (cur_line_of_file != '\n') and ('------' not in cur_line_of_file) and cur_line_of_file != '':
                        self.line_to_insert += lab4.sentence_with_capit_letters((cur_line_of_file.split('. ')))
                        cnt_of_records_in_file += 1
                        self.cnt_of_all_records += 1
                    elif cur_line_of_file == '\n':
                        self.line_to_insert += cur_line_of_file
                        self.cnt_of_all_records += 1
                    elif '----------' in cur_line_of_file:
                        self.line_to_insert += cur_line_of_file.capitalize()
                        cnt_of_records_in_file += 1
                        self.cnt_of_all_records += 1
        return self.line_to_insert

    def insert_into_file(self):
        if self.is_file_exists:
            with open(NewInformation.file_to_write, 'a') as file_for_insert:
                file_for_insert.write(self.read_from_file())
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
            self.count_of_records = len_of_file
            return self.count_of_records
        else:
            return self.count_of_records * 4


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


def main_menu():
    print(' Hi, welcome to our news feed.')
    mode_type = ''
    while mode_type != '0':
        mode_type = input(' Would you like to type info or load from file? 1 - type, 2 - load from file, 0 - exit\n')
        if mode_type not in ['0', '1', '2']:
            print(f'Your choice is "{mode_type}" and it is not an expected value, please try again')
        elif mode_type == '1':
            type_new_info()
        elif mode_type == '2':
            folder_to_load_data = input(
                f'Type path to the file(if it is empty will be a current path {NewRecordsFromFile.default_folder}):\n')
            records_to_load = validation_count_of_records_type()
            file_name = input('Type file name:\n')
            file_to_load = NewRecordsFromFile(records_to_load, file_name, folder_to_load_data)
            if NewRecordsFromFile.is_file_exists(file_to_load):
                NewRecordsFromFile.insert_into_file(file_to_load)
                NewRecordsFromFile.remove_file(file_to_load)
            else:
                print('Wrong file or path - data was not inserted!')
    else:
        print('The program finished working.')


if __name__ == "__main__":
    main_menu()

