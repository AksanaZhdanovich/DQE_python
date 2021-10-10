from datetime import datetime


class NewInformation:
    file_to_write = "newsfeed.txt"
    length_of_description = 30

    def __init__(self, note_text):
        self.note = note_text
        self.end_record = '-' * self.length_of_description
        self.text_in_file = ''
        self.type_of_info = ''

    def add_new_info_in_the_file(self):
        with open(self.file_to_write, "a") as text_file:
            text_file.write(self.text_in_file + '\n\n')
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
        self.text_in_file = self.description + 'Actual until: ' + self.date + ', ' + self.expire_date + ' days left.' + '\n' + self.end_record + '\n'
        self.add_new_info_in_the_file()


class AddWeatherForecast(NewInformation):
    def __init__(self, note_text, city, date, degrees):
        super().__init__(note_text=note_text)
        self.date = date
        self.degrees = degrees
        self.city = city
        self.type_of_info = 'Weather Forecast'
        self.description = NewInformation.info_description(self)
        self.text_in_file = self.description + 'Temperature: ' + self.degrees + ' in ' + self.city + ' Date:' + self.date + '\n' + self.end_record + '\n'
        self.add_new_info_in_the_file()


def validation_date(type_of_info):
    while True:
        input_date = input(f'Please write the date for {type_of_info} in format DD/MM/YYYY')
        try:
            datetime.strptime(input_date, '%d/%m/%Y')
            return input_date
        except ValueError:
            print('Invalid date! Please try again!')
            continue


def main_menu():
    type_of_feed = ''
    print(' Hi, welcome to our news feed.')
    while type_of_feed != '0':
        type_of_feed = input('Choose number to add info:\n' + '1 - add news\n' + '2 - add private ad\n' +
                             '3 - add weather forecast\n' + '0 - quit\n' + 'Your choice:')
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
            forecast_text = input('Please type the forecast:').capitalize()
            forecast_date = validation_date('Weather forecast')
            forecast_city = input('Please type the city:').capitalize()
            forecast_temperature = input('Please type temperature:')
            AddWeatherForecast(forecast_text, forecast_city, forecast_date, forecast_temperature)
    else:
        print(f'All the information is in the file {NewInformation.file_to_write}')


main_menu()
