'''

    Created by: Brendan Betts (brendan.betts@live.com)
    Created on: July 17th, 2013
'''
from src import config_reader

if __name__ == "__main__":
    reader = config_reader.config_reader("conf\config")
    config_options = reader.parse_config_file()
    print config_options