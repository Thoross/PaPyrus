'''
    Copyright (c) 2013 Brendan Betts
    Created by: Brendan Betts (brendan.betts@live.com)
    Created on 7/21/13
'''
from os import path
from os import makedirs
import urllib2

def download_image(decoded_link, file_path, full_file_path):
    if not path.exists(file_path):
        makedirs(file_path)
    with open(full_file_path, 'wb') as wallpaper:
        image = urllib2.urlopen(decoded_link)
        wallpaper.write(image.read())


def get_file_path(save_location, decoded_link):
    file_path = path.abspath(save_location)
    file_name = decoded_link.split("/")[5]
    full_file_path = file_path+"\\"+file_name
    if not path.exists(full_file_path):
        print "Saving %s to %s" % (file_name, file_path)
        download_image(decoded_link, file_path, full_file_path)
    else:
        print "%s has already been downloaded to %s." % (file_name, full_file_path)
