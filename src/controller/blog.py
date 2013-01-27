#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Blog handler for urls
    version 1.0
    history:
    2013-1-19    dylanninin@gmail.com    prototype
"""

import os
from config import setting
from entry import EntryService

render = setting.render
web = setting.web
config = setting.config

class Index:
    """
        Index Handler for /([\d]*)"
        example:
            /    
                 request the index of this blog and list the first page of all
                 entries of this blog from newest to oldest
                 the default page size is 5 which is configured with config.limit
                 refer:    config/setting.py
            /1   
                  equivalent with /
            /2?limit=10
                  request the second page with 10 entries
            
    """
    def GET(self, start):
        params = web.input(limit=config.limit)
        limit = int(params.limit)
        if start in ['', '0']:
            start = 1
        start = int(start)
        entryService = EntryService()
        entries = entryService.findByPage(start,limit)
        return render.index(entries)


class Entry:
    """
        Entry Handler for /entries/(.+)
        example:
            /entries/the-importance-of-complex-password.html
    """
    def GET(self, url):
        entryService = EntryService()
        result = entryService.findByUrl(url)
        if result == None:
            web.seeother('/error')
        else:
            return render.entry(result)


class Page:
    """
        Page Handler for /pages/(.+)
        example:
            /pages/about.html
            /pages/contact.html
            /pages/subscribe.html
    """
    def GET(self, url):
        return render.page()

class Archive:
    """
        Archive Handler for /archives/(.+)
        example:
            /archives/main.html
            /archives/2013-01.html
            /archives/2012-12.html
    """
    def GET(self, url):
        return render.archive()


class Search:
    """
        Search Handler for /search?params
        exampe:  
            /search?query=value&start=1&limit=5
            /search?tag=webpy&start=1&limit=5
            /search?category=python
    """
    def GET(self, request):
        return render.search()


class Image:
    """
        favicon.ico handle
        refer: http://webpy.org/images
    """
    def GET(self):
        name = 'favicon.ico'
        ext = name.split('.')[-1]
        cType = {
            "png":"images/png",
            "jpg":"images/jpeg",
            "gif":"images/gif",
            "ico":"images/x-icon"
        }
        static = config.static[1:]      #config.static is /static
        if name in os.listdir(static):
            web.header('Content-Type', cType[ext])      #set content-type
            return open('%s/%s' %(static, name), 'rb').read()


class Error:
    """
        Error Handler for any url other than above
    """
    def GET(self, request):
        return render.error()

if __name__ == "__main__":
    pass
