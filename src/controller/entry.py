#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Entry Handler
    version 1.0
    history:
    2013-1-19    dylanninin@gmail.com    prototype
"""
from datetime import datetime
from config import setting
from util import d2o


class EntryService():
    """
        Entry Service
    """
    def __init__(self):
        self.name = 'entries'
        self.entryCollection = setting.blog[self.name]
        self.model = self.example()
    
    def example(self):
        """
            model entry
        """
        entry = {
                 'author':{
                        'name':'dylan',
                        'url':'http://www.dylanninin.com'
                           },
                 'title':'your-title',
                 'count':'100',
                 'url':'your-url.html',
                 'status':'published',
                 'date':datetime.utcnow(),
                 'excerpt':'''
                     excerpt of this entry.
                 ''',
                 'content':'''
                     content of this entry.
                 ''',
                 'tags':['python', 'web.py', 'Activist', 'Web'],
                 'categories':['阅读'],
                 'more':'nothing to do'
        }
        return entry   
    
    
    def post(self, entry):
        """
            post a new entry
        """
        self.entryCollection.save(entry)
    
    
    def update(self, entry):
        """
            update an entry
        """
        pass
    
    def findByUrl(self, url):
        """
            find entry by url
        """
        documents = self.entryCollection.find({'url':url})
        if documents.count() == 0:
            return None
        else:
            return d2o.Dict2Object(documents[0])
    
    
    def findByTag(self, tag):
        """
            find entry by tag
        """
        pass
    
    
    def findByCategory(self, category):
        """
            find entry by category
        """
        pass
    
    
    def findByPage(self, start=setting.config.start, limit=setting.config.limit, query=None):
        """
            find entries by page
               start: the start page
               limit: the page size
               query: some query based on read operations rule of pymongo
                   such as {'tag':'python'},{'query':'any filtered input from search'}
                sort:
                    sort(key_or_list, direction=None)
                    Sorts this cursor’s results.
                    Takes either a single key and a direction, or a list of (key, 
                    direction) pairs. The key(s) must be an instance of (str, 
                    unicode), and the direction(s) must be one of (ASCENDING, 
                    DESCENDING).
                    Raises InvalidOperation if this cursor has already been used. 
                    Only the last sort() applied to this cursor has any effect.
                refer: http://api.mongodb.org/python/current/api/pymongo/cursor.html
                ?highlight=sort#pymongo.cursor.Cursor.sort
        """
        skip = limit * (start - 1)
        cursor = self.entryCollection.find(query).limit(limit).skip(skip)
        return self.cursor2Object(cursor)


    def cursor2Object(self, cursor):
        """
            cursor to object
            iterate this cursor returned by mongo query and then convert it 
            to object respectively
        """
        data = []
        for document in cursor:
            data.append(d2o.Dict2Object(document))
        return data



if __name__ == '__main__':
    entryService = EntryService()
    print dir(entryService)
    print entryService.model