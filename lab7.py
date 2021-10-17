import csv


class CsvProcessing:

    def __init__(self, file_to_write):
        self.csv_file_words = 'words_in_newsfeed.csv'
        self.csv_file_letters = 'letters_in_newsfeed.csv'
        self.txt_file_in_str = ''
        self.file_to_write = file_to_write
        self.part_of_words = ['_', '-', "'"]
        self.only_words = []
        self.only_letters = []
        self.only_letters_lower = []
        self.all_letters = []
        self.custom_header = ['word', 'count']
        self.custom_header_letters = ['letter', 'count_all', 'count_uppercase', 'percentage']
        self.not_symbols_from_words = ['!', '.', ',', '"', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/',
                                       '\\', ':', ';']
        self.str_for_file_with_words = []
        self.str_for_file_with_letters_low = []
        self.count_of_letters = 0

    def txt_file_into_str(self):
        with open(self.file_to_write, "r") as text_file:
            self.txt_file_in_str = text_file.read().replace('\n', ' ').strip()
        return self.txt_file_in_str

    def words_in_str_from_file(self):
        str_for_words = CsvProcessing.txt_file_into_str(self).lower()
        for i in str_for_words:
            if i in self.not_symbols_from_words:
                str_for_words = str_for_words.replace(i, '')
        all_words = str_for_words.split(' ')
        for words in all_words:
            if len(words) > 0 and words[0].isalpha():
                self.only_words.append(words)
        return self.only_words

    def count_of_words(self):
        unique = sorted(set(CsvProcessing.words_in_str_from_file(self)))
        for word in unique:
            self.str_for_file_with_words.append([word, self.only_words.count(word)])
        return self.str_for_file_with_words

    def write_to_file(self):
        with open(self.csv_file_words, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', lineterminator='\r')
            writer.writerow(self.custom_header)
            for res in self.count_of_words():
                writer.writerow(res)

    def letters_in_str_from_file(self):
        str_for_letters = CsvProcessing.txt_file_into_str(self)
        for letter in str_for_letters:
            if letter.isalpha():
                self.only_letters.append(letter)
                self.only_letters_lower.append(letter.lower())
        return self.only_letters

    def count_of_letters_all(self):
        unique = sorted(set(CsvProcessing.letters_in_str_from_file(self)))
        unique_low = sorted(set(self.only_letters_lower))
        self.count_of_letters = 0
        for letter in unique:
            self.count_of_letters += self.only_letters.count(letter)
        for letter in unique_low:
            self.str_for_file_with_letters_low.append([letter, self.only_letters_lower.count(letter),
                                                       self.only_letters.count(chr(ord(letter) - 32)), round(
                    self.only_letters_lower.count(letter) * 100 / self.count_of_letters, 2)])
        return self.str_for_file_with_letters_low

    def write_to_file_letters(self):
        with open(self.csv_file_letters, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', lineterminator='\r')
            writer.writerow(self.custom_header_letters)
            for res in self.count_of_letters_all():
                writer.writerow(res)
