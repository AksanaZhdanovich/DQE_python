from xml.etree import ElementTree as ElTree
import lab8
import os


class ProcessXml:
    def __init__(self, records_to_load, file_name, folder_to_load=str(os.path.abspath(os.curdir))):
        self.file_name = file_name
        self.folder_to_load_data = folder_to_load
        self.full_path = os.path.join(self.folder_to_load_data, self.file_name)
        self.records_to_load = records_to_load
        self.tree = ElTree.parse(self.full_path)
        self.root = self.tree.getroot()

    def xml_to_list_of_dicts(self):
        note_list = []
        for item in self.root.findall('note'):
            note_dict = {}
            note_item = item.attrib
            note_dict.update(note_item)
            for child in item:
                note_dict[child.tag] = child.text
            note_list.append(note_dict)
        return note_list

    def proceed_dict_xml(self):
        test_dict = self.xml_to_list_of_dicts()
        connector = lab8.JsonProcess(self.records_to_load, self.file_name, self.folder_to_load_data)
        connector.proceed_dict_json(test_dict)

    def delete_xml(self):
        if len(ProcessXml.xml_to_list_of_dicts(self)) == self.records_to_load:
            os.remove(self.full_path)
            print(f'File {self.full_path} was deleted')



