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
import urllib2

def get_all_wallpaper_links(response_html):
    pattern = re.compile('<a href=\"http://wallbase.cc/wallpaper/(.*?)\"')
    links = pattern.findall(response_html)
    return links

def get_wallpaper_download_link(wallpaper_link):
    url_str = "http://wallbase.cc/wallpaper/%s" % str(link)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}
    download_link_request = url_request(url_str)
    response_html = download_link_request.do_request(headers)
    pattern = re.compile('<img src="\'\+B\(\'(.*)\'\)\+\'" />\'\);</script>')
    image_link = str(pattern.findall(response_html))
    stripped_link = image_link.split("u'")[1].strip('\']')
    decoded_link = base64.b64decode(stripped_link)
    return decoded_link

def download_image(decoded_link, file_path, full_file_path):
    if not path.exists(file_path):
        mkdir(file_path)
    with open(full_file_path, 'wb') as wallpaper:
        image = urllib2.urlopen(decoded_link)
        wallpaper.write(image.read())

if __name__ == "__main__":
    reader = config_reader.config_reader("conf\config")
    config_options = reader.parse_config_file()
    print config_options
    request = url_request("http://wallbase.cc/search/Abstract")

    response_html = request.do_request(None)
    links = get_all_wallpaper_links(response_html)
    for link in links:
        decoded_link = get_wallpaper_download_link(link)
        file_path = path.abspath(config_options["save_location"]+"/Abstract/")
        file_name = decoded_link.split("/")[5]
        full_file_path = file_path+"\\"+file_name
        print "Saving %s to %s" % (file_name, file_path)
        download_image(decoded_link, file_path, full_file_path)


