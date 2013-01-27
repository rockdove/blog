#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Dict2Object helper 
    version 1.0
    history:
    2013-1-19    dylanninin@gmail.com    prototype
"""

class Dict2Object(dict):
    """
        dict to object
        so you can access like a.attribute but not a['attribute']
        http://stackoverflow.com/questions/1305532/convert-python-dict-to-object
    """
    def __init__(self, data = None):
        super(Dict2Object, self).__init__()
        if data:
            self.__update(data, {})

    def __update(self, data, did):
        dataid = id(data)
        did[dataid] = self

        for k in data:
            dkid = id(data[k])
            if did.has_key(dkid):
                self[k] = did[dkid]
            elif isinstance(data[k], Dict2Object):
                self[k] = data[k]
            elif isinstance(data[k], dict):
                obj = Dict2Object()
                obj.__update(data[k], did)
                self[k] = obj
                obj = None
            else:
                self[k] = data[k]

    def __getattr__(self, key):
        return self.get(key, None)

    def __setattr__(self, key, value):
        if isinstance(value,dict):
            self[key] = Dict2Object(value)
        else:
            self[key] = value

    def update(self, *args):
        for obj in args:
            for k in obj:
                if isinstance(obj[k],dict):
                    self[k] = Dict2Object(obj[k])
                else:
                    self[k] = obj[k]
        return self

    def merge(self, *args):
        for obj in args:
            for k in obj:
                if self.has_key(k):
                    if isinstance(self[k],list) and isinstance(obj[k],list):
                        self[k] += obj[k]
                    elif isinstance(self[k],list):
                        self[k].append(obj[k])
                    elif isinstance(obj[k],list):
                        self[k] = [self[k]] + obj[k]
                    elif isinstance(self[k],Dict2Object) and isinstance(obj[k],Dict2Object):
                        self[k].merge(obj[k] )
                    elif isinstance(self[k],Dict2Object) and isinstance(obj[k],dict):
                        self[k].merge(obj[k])
                    else:
                        self[k] = [self[k], obj[k]]
                else:
                    if isinstance(obj[k],dict):
                        self[k] = Dict2Object(obj[k])
                    else:
                        self[k] = obj[k]
        return self
 

def test01():
    class UObject( Dict2Object ):
        pass
    obj = Dict2Object({1:2})
    d = {}
    d.update({
        "a": 1,
        "b": {
            "c": 2,
            "d": [ 3, 4, 5 ],
            "e": [ [6,7], (8,9) ],
            "self": d,
        },
        1: 10,
        "1": 11,
        "obj": obj,
    })
    x = UObject(d)


    assert x.a == x["a"] == 1
    assert x.b.c == x["b"]["c"] == 2
    assert x.b.d[0] == 3
    assert x.b.d[1] == 4
    assert x.b.e[0][0] == 6
    assert x.b.e[1][0] == 8
    assert x[1] == 10
    assert x["1"] == 11
    assert x[1] != x["1"]
    assert id(x) == id(x.b.self.b.self) == id(x.b.self)
    assert x.b.self.a == x.b.self.b.self.a == 1

    x.x = 12
    assert x.x == x["x"] == 12
    x.y = {"a":13,"b":[14,15]}
    assert x.y.a == 13
    assert x.y.b[0] == 14

def test02():
    x = Dict2Object({
        "a": {
            "b": 1,
            "c": [ 2, 3 ]
        },
        1: 6,
        2: [ 8, 9 ],
        3: 11,
    })
    y = Dict2Object({
        "a": {
            "b": 4,
            "c": [ 5 ]
        },
        1: 7,
        2: 10,
        3: [ 12 , 13 ],
    })
    z = {
        3: 14,
        2: 15,
        "a": {
            "b": 16,
            "c": 17,
        }
    }
    x.merge( y, z )
    assert 2 in x.a.c
    assert 3 in x.a.c
    assert 5 in x.a.c
    assert 1 in x.a.b
    assert 4 in x.a.b
    assert 8 in x[2]
    assert 9 in x[2]
    assert 10 in x[2]
    assert 11 in x[3]
    assert 12 in x[3]
    assert 13 in x[3]
    assert 14 in x[3]
    assert 15 in x[2]
    assert 16 in x.a.b
    assert 17 in x.a.c

if __name__ == '__main__':
    test01()
    test02()
