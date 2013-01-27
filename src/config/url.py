#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    url settings
    version 1.0
    history:
    2013-1-19    dylanninin@gmail.com    prototype
"""

from setting import config


"""urls"""
urls = (
    config.indexURL, 'controller.blog.Index',
    config.entryURL + '/(.+)','controller.blog.Entry',
    config.pageURL + '/(.+)', 'controller.blog.Page',
    config.searchURL + '?(.+)','controller.blog.Search',
    config.archiveURL + '/(.+)', 'controller.blog.Archive',
    config.faviconURL, 'controller.blog.Image',
    '/(.+)', 'controller.blog.Error',
)
