'''
    Copyright (c) 2013 Brendan Betts
    Created by: Brendan Betts (brendan.betts@live.com)
    Created on July 17th, 2013
'''

import ConfigParser


class config_reader ():

    def __init__(self, file_path):
        self.file_path = file_path
        self.config_parser = ConfigParser.ConfigParser()

    def parse_config_file(self):

        try:
            self.config_parser.read(self.file_path)
            config_sections = self.config_parser.sections()
            config_options = self.get_section_data(config_sections)
            return config_options

        except ConfigParser.Error, e:
            print "There was an error with your config!\n%s" % str(e)

    def get_section_data(self, config_sections):

        section_data = {}
        for section in config_sections:
            section_data[section] = self.config_parser.get(section, section)

        return section_data