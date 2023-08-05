"""
Extended type:
    ExtList, rewrite multiple operation

    ExtDict, rewrite getitem so that '/a/b/c/d' -> ['a']['b']['c']['d']
"""
from collections import Iterable 

class ExtList(list):
    """
    Extended list
    """
    def __mul__(self, a):
        assert isinstance(a, Iterable),\
            'multiplier should be Iterable, instead of {1}'.format(a, type(a))
        assert len(self) == len(a),\
            'multiple length should be same'
        return self.__class__([x for i, x in enumerate(self) for time in range(a[i])])

class ExtDict(dict):
    """
    Extended Dict
    """
    def __getitem__(self, name):
        if name in self.keys():
            return dict.__getitem__(self, name)
        name = name.split('/')
        sdict = self
        while name:
            key = name.pop(0)
            if key:
                sdict = sdict[key]
        return sdict

    def get_all_keys(self, basename='', depth=10000):
        result = []
        if depth == 0:
            return result
        for key, val in self.items():
            keyname = basename+'/'+key
            if isinstance(val, dict):
                result += ExtDict.get_all_keys(val, keyname, depth-1)
            else:
                result.append(keyname)
        return result
