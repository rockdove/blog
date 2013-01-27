#!/usr/bin/env python
# -*- coding:utf-8 -*-
import web
import pymongo

"""
    gloabl config
    version 1.0
    history:
    2013-1-19    dylanninin@gmail.com    prototype
"""


"""gloabl config"""
config = web.storage(
    siteName = 'Pastime Paradise',
    siteURL = 'http://www.dylanninin.com:8080',
    author = 'dylanninin',
    static = '/static',
    publish = '/publish',
    template = 'template',
    indexURL = "/([\d]*)",
    entryURL = '/entries',
    pageURL = '/pages',
    archiveURL = '/archives',
    searchURL = '/search',
    faviconURL = '/favicon.ico',
    start = 1,
    limit = 5,
    searchHolder = 'search all site',
    cache = False,
    debug = True,
)

"""log config"""
logcfg = web.storage(
    file='blog.log',
    interval_type = 'D',
    interval = 30,
    backups = 10,
    tofile = True,
    toprint = False,
    format = '%(asctime)s - %name)s - %(levelname)s - %(message)s',
    
)

"""database configure"""
dbcfg = web.storage(
    type = "mongodb",
    host = 'localhost',     
    port = 27017,
    db = 'blog'
)


web.config.debug = config.debug
render = web.template.render(config.template, cache=config.cache)
web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render

__database = pymongo.MongoClient(dbcfg.host,dbcfg.port)
blog = __database[dbcfg.db]


if __name__ == "__main__":
    print blog
