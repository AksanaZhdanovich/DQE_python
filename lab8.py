import os
import lab4
from datetime import datetime
import json
from xml.etree import ElementTree as ElTree


class JsonProcess:
    def __init__(self, records_to_load, file_name, folder_to_load=str(os.path.abspath(os.curdir))):
        self.file_name = file_name
        self.records_to_load = int(records_to_load)
        self.folder_to_load = folder_to_load
        self.full_path = os.path.join(self.folder_to_load, self.file_name)
        self.type_of_notes = ['NEWS', 'WEATHER FORECAST', 'PRIVATE AD']
        self.length_of_description = 30
        self.end_record = '-' * self.length_of_description
        self.file_to_write = 'newsfeed.txt'
        self.json_dict = []

    def read_from_json(self):
        with open(self.full_path, 'r') as json_to_read:
            self.json_dict = json.loads(json_to_read.read())
        return self.json_dict

    def proceed_dict_json(self, dictionary):
        json_dict = dictionary
        for i in range(self.records_to_load):
            if json_dict[i]['header'].upper() == 'NEWS':
                JsonProcess.proceed_news(self, json_dict[i])
            if json_dict[i]['header'].upper() == 'PRIVATE AD':
                JsonProcess.proceed_ad(self, json_dict[i])
            if json_dict[i]['header'].upper() == 'WEATHER FORECAST':
                JsonProcess.proceed_weather(self, json_dict[i])

    def proceed_news(self, json_dict):
        with open(self.file_to_write, 'a') as file_for_insert:
            for i in json_dict:
                if i == 'header':
                    file_for_insert.write(lab4.sentence_with_capit_letters((json_dict[i].split('. '))) + ' '
                                          + '-' * (self.length_of_description - len(json_dict[i]) - 1) + '\n')
                if i == 'text':
                    file_for_insert.write(lab4.sentence_with_capit_letters((json_dict[i].split('. '))) + '\n')
                if i == 'city':
                    file_for_insert.write(json_dict[i].capitalize() + ', ')
                if i == 'date_time':
                    file_for_insert.write(json_dict[i] + '\n')
            file_for_insert.write(self.end_record + '\n')

    def proceed_ad(self, json_dict):
        with open(self.file_to_write, 'a') as file_for_insert:
            for i in json_dict:
                if i == 'header':
                    file_for_insert.write(
                        lab4.sentence_with_capit_letters((json_dict[i].split('. ')))
                        + ' ' + '-' * (self.length_of_description - len(json_dict[i]) - 1) + '\n')
                if i == 'text':
                    file_for_insert.write(lab4.sentence_with_capit_letters((json_dict[i].split('. '))) + '\n')
                if i == 'city':
                    file_for_insert.write(json_dict[i].capitalize() + ', ')
                if i == 'date':
                    file_for_insert.write('Actual until: ' + json_dict[i] + ', ' +
                                          str((datetime.strptime(json_dict[i], '%d/%m/%Y')
                                               - datetime.now()).days + 1) + ' days left.' + '\n')
            file_for_insert.write(self.end_record + '\n')

    def proceed_weather(self, json_dict):
        with open(self.file_to_write, 'a') as file_for_insert:
            for i in json_dict:
                if i == 'header':
                    file_for_insert.write(
                        lab4.sentence_with_capit_letters((json_dict[i].split('. ')))
                        + ' ' + '-' * (self.length_of_description - len(json_dict[i]) - 1) + '\n')
                if i == 'text':
                    file_for_insert.write(lab4.sentence_with_capit_letters((json_dict[i].split('. '))) + '\n')
                if i == 'temperature':
                    file_for_insert.write('Temperature: ' + json_dict[i])
                if i == 'city':
                    file_for_insert.write(' in ' + json_dict[i].capitalize() + ' ')
                if i == 'date':
                    file_for_insert.write('Date:' + json_dict[i] + '\n')
            file_for_insert.write(self.end_record + '\n')

    def is_file_can_be_processed(self):
        json_dict = JsonProcess.read_from_json(self)
        for i in range(self.records_to_load):
            if json_dict[i]['header'].upper() not in self.type_of_notes:
                print(f'Wrong header in json file, header should has values {self.type_of_notes}')
                return False
            else:
                return True

    def delete_json(self):
        if len(JsonProcess.read_from_json(self)) == self.records_to_load:
            os.remove(self.full_path)
            print(f'File {self.full_path} was deleted')


class XMLProceed(JsonProcess):
    def __int__(self, records_to_load, file_name, folder_to_load=str(os.path.abspath(os.curdir))):
        JsonProcess.__init__(self, records_to_load, file_name, folder_to_load=str(os.path.abspath(os.curdir)))
        self.tree = ElTree.parse(self.full_path)
        self.root = self.tree.getroot()
        self.note_list = []

    def xml_to_list_of_dicts(self):
        # note_list = []
        for item in self.root.findall('note'):
            note_dict = {}
            note_item = item.attrib
            note_dict.update(note_item)
            for child in item:
                note_dict[child.tag] = child.text
            self.note_list.append(note_dict)
        return self.note_list
