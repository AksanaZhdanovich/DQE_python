from datetime import datetime


class NewNews:
    datetime_news = datetime.now().strftime('%d/%m/%Y %H.%M')

    def __init__(self, note_text):
        self.note = note_text
        self.end_record = '-' * 30
        self.text_in_file = ''
        self.type_of_news = ''

    def add_new_note_in_the_file(self):
        with open(file_to_write, "a") as text_file:
            text_file.write(self.text_in_file + '\n\n')
        print('The information was added\n')

    def news_description(self):
        return self.type_of_news + '-' * (30 - len(self.type_of_news)) + '\n' + self.note + '\n'


class AddNews(NewNews):

    def __init__(self, note_text, city):
        NewNews.__init__(self, note_text=note_text)
        self.type_of_news = 'News '
        description = NewNews.news_description(self)
        self.city = city
        self.text_in_file = description + self.city + ',' + self.datetime_news + '\n' + self.end_record + '\n'
        self.add_new_note_in_the_file()


class AddAd(NewNews):

    def __init__(self, note_text, date):
        NewNews.__init__(self, note_text=note_text)
        self.date = date
        self.expire_date = str((datetime.strptime(self.date, '%d/%m/%Y') - datetime.now()).days + 1)
        self.type_of_news = 'Private Ad '
        description = NewNews.news_description(self)
        self.text_in_file = description + 'Actual until: ' + self.date + ', ' + self.expire_date + ' days left.' + '\n' + self.end_record + '\n'
        self.add_new_note_in_the_file()


class AddWeatherForecast(NewNews):
    def __init__(self, note_text, city, date, degrees):
        NewNews.__init__(self, note_text=note_text)
        self.date = date
        self.degrees = degrees
        self.city = city
        self.type_of_news = 'Weather Forecast'
        description = NewNews.news_description(self)
        self.text_in_file = description + 'Temperature: ' + self.degrees + ' in ' + self.city + ' Date:' + self.date + '\n' + self.end_record + '\n'
        self.add_new_note_in_the_file()


def main_menu():
    type_of_feed = str()
    print(' Hi, welcome to our news feed.')
    while type_of_feed != '0':
        print('Choose number to add info:\n', '1 - add news\n', '2 - add private ad\n', '3 - add weather forecast\n',
              '0 - quit\n', 'Your choice:')
        type_of_feed = input()
        if type_of_feed not in ['0', '1', '2', '3']:
            print(f'Your choice is "{type_of_feed}" and it is not an expected value, please try again')
        elif type_of_feed == '1':
            print('Your choice is 1 - add news:')
            news_text = input('Please type the text of your news:\n> ').capitalize()
            news_city = input('Please type the city:\n').capitalize()
            AddNews(news_text, news_city)
        elif type_of_feed == '2':
            print('Your choice is 2 - add ad:')
            news_text = input('Please type the text of your private ad:\n> ').capitalize()
            news_date = input('Please type the date of your ad:(right format is DD/MM/YYYY):')
            try:
                valid_date = datetime.strptime(news_date, '%d/%m/%Y')
            except ValueError:
                print('Invalid date! Please try again!')
                continue
            AddAd(news_text, news_date)
        elif type_of_feed == '3':
            print('Your choice is 3 - add weather forecast:')
            news_text = input('Please type the forecast:').capitalize()
            news_date = input('Please type the date of your forecast:(right format is DD/MM/YYYY):')
            try:
                valid_date = datetime.strptime(news_date, '%d/%m/%Y')
            except ValueError:
                print('Invalid date! Please try again!')
                continue
            news_city = input('Please type the city:').capitalize()
            news_temperature = input('Please type temperature:')
            AddWeatherForecast(news_text, news_city, news_date, news_temperature)
        if type_of_feed == '0':
            print(f'All the information is in the file {file_to_write}')


file_to_write = "newsfeed.txt"
main_menu()
