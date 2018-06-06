"""
Bastian

22.05.2018

"""


import xml.etree.ElementTree as ET
import openpyxl
import os



class Xml_handler():
    xml_delimiter = ','
    xml_file = "Fahrzeug.xml"

    def __init__(self, parent):
        self.parent = parent
        tree = ET.parse(self.xml_file)
        self.xml_root = tree.getroot()

        self.parent.file_types, self.parent.file_types_index = self.collect_entries()
        self.parent.keywords = self.collect_keywords()

    def collect_entries(self):
        _types = list()
        _types_index = list()
        for index, source_type in enumerate(self.xml_root):
            if source_type.tag == 'sourceType':
                for ending in source_type.iter('ending'):
                    for _type in ending.text.replace(' ', '').split(self.xml_delimiter):
                        if _type in _types:
                            _types_index[_types.index(_type)].append(index)
                        else:
                            _types.append(_type)
                            _types_index.append([index])
        return _types, _types_index

    def collect_keywords(self):
        _tags = list()
        for index, source_type in enumerate(self.xml_root):
            if source_type.tag == 'sourceType':
                for tags in source_type.iter('tags'):
                    _tags.append(tags.text.replace(' ', '').lower().split(self.xml_delimiter))
        return _tags



#
# class Main():
#
#     xml_delimiter = ','
#     xml_file = "Fahrzeug.xml"
#     test_filepath = "_Auswertung_.xlsx"
#
#     def __init__(self):
#         tree = ET.parse(self.xml_file)
#         self.xml_root = tree.getroot()
#
#         for data in self.xml_root.find('data'):
#             for datatype in data:
#                 name = datatype.tag
#                 print(name)



        # self.file_checker(self.test_filepath)
        #
        # for child in self.xml_root:
        #     print(child.tag)




        # new_Fzg = ET.SubElement(root, "Fahrzeug", attrib={"id": "1"})
        # new_Fzg_name = ET.SubElement(new_Fzg, "name")
        # new_Fzg_name.text = "VW"
        #  tree.write(xml_file)


    # def file_checker(self, filename):
    #     for source in self.xml_root.iter('sourceType'):
    #         if self.check_ending(source, filename):
    #             if self.check_tags(source, filename):
    #                 self.file_extractor(filename, source)
    #
    # def file_extractor(self, filename, source):
    #     try:
    #         book = openpyxl.load_workbook(filename)
    #     except Exception:
    #         print('ERROR: Worbbook could not be read: %s' %filename)
    #         return 1
    #
    #     if source.find('workbook'):
    #         sheets = source.find('workbook').split(self.xml_delimiter)
    #     else:
    #         sheets = [book.active]
    #     if sheets:
    #         temp = dict()
    #         for sheet in sheets:
    #             for entries in source.iter('entries'):
    #                for data in list(entries):
    #                 temp[data.tag] = sheet[data.text].value
    #         print(temp)
    #
    #
    # def check_ending(self,source, filename):
    #         for ending in source.find('ending').text.split(self.xml_delimiter):
    #             if filename.endswith(ending.lower()):
    #                 return True
    #         return False
    #
    # def check_tags(self, source, filename):
    #     for tag in source.find('tags').text.split(self.xml_delimiter):
    #         if tag.lower() in filename.lower():
    #             return True
    #     return False




if __name__ == "__main__":
    xlm = Xml_handler()


