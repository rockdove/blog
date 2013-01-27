#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Blog App Entrance
    version 1.0
    history:
    2013-1-19    dylanninin@gmail.com    prototype
"""

import web
from config import url

app = web.application(url.urls, globals())

if __name__ == "__main__":
    app.run()
