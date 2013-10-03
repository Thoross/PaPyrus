#!/usr/bin/env python
# coding=UTF-8
'''
    Copyright (c) 2013 Brendan Betts
    Created by: Brendan Betts (brendan.betts@live.com)
    Created on: July 17th, 2013
'''
import config_reader
from wallpaper_utils import loop_tags

if __name__ == "__main__":
    print "Starting PaPyrus."
    reader = config_reader.config_reader("conf\config")
    config_options = reader.parse_config_file()
    loop_tags(config_options)
    print "All done!"
