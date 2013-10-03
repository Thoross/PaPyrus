'''
    Copyright (c) 2013 Brendan Betts
    Created by: Brendan Betts (brendan.betts@live.com)
    Created on 7/21/13
'''

from os import path
import re
from url import url_request
import base64
from image_utils import get_file_path


def loop_tags(config_options):
    tags = config_options["tags"].split(",")
    response_html = ""
    for tag in tags:
        for i in range(int(config_options["page_count"])):
            tag = assign_tag(tag)
            response_html = get_html(tag, config_options, i)
            links = get_all_wallpaper_links(response_html)
            for link in links:
                download_link = get_wallpaper_download_link(link)
                filename = get_filename(download_link)
                get_file_path(path.join(config_options["save_location"], tag.capitalize()), download_link, filename)


def get_all_wallpaper_links(response_html):
    pattern = re.compile('<a href=\"http://wallbase.cc/wallpaper/(.*?)\"')
    links = pattern.findall(response_html)
    return links


def get_wallpaper_download_link(wallpaper_link):
    url_str = "http://wallbase.cc/wallpaper/%s" % str(wallpaper_link)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*'}
    download_link_request = url_request(url_str)
    response_html = download_link_request.do_get(headers)
    pattern = re.compile('<img src=\"(.*?)\" class=\"wall ')
    image_link = str(pattern.findall(response_html))
    return strip_link(image_link)


def get_url_paramas(tag, config_options):
    url_params = {}
    url_params["thpp"] = config_options["thpp"]
    url_params["query"] = tag
    url_params["res_opt"] = "eqeq"
    url_params["res"] = "0x0"
    url_params["aspect"] = "0"
    for rating in config_options:
        url_params[rating] = get_rating(config_options[rating])
    url_params["orderby"] = config_options["orderby"]
    url_params["orderby_opt"] = config_options["orderby_opt"]
    return url_params

def get_rating(rating):
    if rating == False:
        return "0"
    else:
        return "1"

def assign_tag(tag):
    if tag == "toplist":
        tag = "top"

    elif tag == "":
        tag = "new wallpapers"

    elif tag == "random":
        tag = "random"

    else:
        tag = tag
    return tag

def get_html(tag, config_options, i):
    search_url =""
    url_params = None

    if tag == "":
        search_url = "http://wallbase.cc/search/%s" % (str(i*int(config_options["thpp"])))

    elif tag == "toplist" or tag == "top":
        search_url = "http://wallbase.cc/toplist/%s" % (str(i*int(config_options["thpp"])))

    elif tag == "random":
        search_url = "http://wallbase.cc/random%s" % (str(i*int(config_options["thpp"])))

    else:
        search_url = "http://wallbase.cc/search?q=%s" % (str(tag))
        url_params = get_url_paramas(tag, config_options)

    request = url_request(search_url)
    return do_request(request, False, url_request)

def do_request(request, is_post, url_params):
    response_html = ""
    if is_post == True:
        response_html = request.do_post(url_params)
    else:
        response_html = request.do_get(None)

    return response_html

def strip_link(image_link):
    return image_link.split("u'")[1].strip('\']/')

def get_filename(image_link):
    length = len(image_link.split('/'))
    return image_link.split('/')[length-1]