# coding=UTF-8
'''
    Copyright (c) 2013 Brendan Betts
    Created by: Brendan Betts (brendan.betts@live.com)
    Created on: July 17th, 2013
'''
from src import config_reader
from src.url import url_request
import re
import base64
from os import path, mkdir
import requests
import urllib2


if __name__ == "__main__":
    reader = config_reader.config_reader("conf\config")
    config_options = reader.parse_config_file()
    print config_options
    request = url_request("http://wallbase.cc/search/Abstract")

    response_html = request.do_request()
    pattern = re.compile('<a href=\"http://wallbase.cc/wallpaper/(.*?)\"')
    links = pattern.findall(response_html)
    for link in links:
        url = "http://wallbase.cc/wallpaper/%s" % str(link)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}
        response_html = requests.get(url, headers=headers)
        pattern = re.compile('<img src="\'\+B\(\'(.*)\'\)\+\'" />\'\);</script>')
        image_link = str(pattern.findall(response_html.text))
        stripped_link = image_link.split("u'")[1].strip('\']')
        decoded_link = base64.b64decode(stripped_link)
        file_path = path.abspath(config_options["save_location"]+"/Abstract/")
        file_name = decoded_link.split("/")[5]
        full_file_path = file_path+"\\"+file_name
        print "Saving %s to %s" % (file_name, file_path)
        if not path.exists(file_path):
            mkdir(file_path)
        with open(full_file_path, 'wb') as wallpaper:
            image = urllib2.urlopen(decoded_link)
            wallpaper.write(image.read())

