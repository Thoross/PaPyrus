'''
    Copyright (c) 2013 Brendan Betts
    Created by: Brendan Betts (brendan.betts@live.com)
    Created on 7/21/13
'''

import re
from url import url_request
import base64
from image_utils import get_file_path


def loop_tags(config_options):
    tags = config_options["tags"].split(",")
    for tag in tags:
        request = url_request("http://wallbase.cc/search/%s" % str(tag))
        response_html = request.do_request(None)
        links = get_all_wallpaper_links(response_html)
        for link in links:
            decoded_link = get_wallpaper_download_link(link)
            if tag == "":
                tag = "Random"
            get_file_path(config_options["save_location"] +"\\"+tag.capitalize(), decoded_link)


def get_all_wallpaper_links(response_html):
    pattern = re.compile('<a href=\"http://wallbase.cc/wallpaper/(.*?)\"')
    links = pattern.findall(response_html)
    return links


def get_wallpaper_download_link(wallpaper_link):
    url_str = "http://wallbase.cc/wallpaper/%s" % str(wallpaper_link)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}
    download_link_request = url_request(url_str)
    response_html = download_link_request.do_request(headers)
    pattern = re.compile('<img src="\'\+B\(\'(.*)\'\)\+\'" />\'\);</script>')
    image_link = str(pattern.findall(response_html))
    stripped_link = image_link.split("u'")[1].strip('\']')
    decoded_link = base64.b64decode(stripped_link)
    return decoded_link