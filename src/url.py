'''
    Copyright 2013 Brendan Betts
    Created by: Brendan Betts (brendan.betts@live.com)
    Created on July 18th, 2013
'''


import requests


class url_request():
    def __init__(self, url):
        self.url = url

    def do_request(self, headers):
        r = requests.get(self.url,headers=headers)
        return r.text

