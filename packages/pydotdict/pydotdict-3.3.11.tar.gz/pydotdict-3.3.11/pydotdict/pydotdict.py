from collections import OrderedDict
from collections.abc import MutableMapping


class DotDict(MutableMapping, OrderedDict):

    def __init__(self, *args, **kwargs):
        self._dict = dict()
        if args:
            d = args[0]
            if isinstance(d, dict):
                for k, v in d.items():
                    if isinstance(v, dict):
                        v = DotDict(v)
                    if type(v) is list:
                        l = []
                        for i in v:
                            n = i
                            if type(i) is dict:
                                n = DotDict(i)
                            l.append(n)
                        v = l
                    self._dict[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self._dict[k] = v

    def items(self):
        return self._dict.items()

    def __iter__(self):
        return self._dict.__iter__()

    def __setitem__(self, k, v):
        self._dict[k] = v

    def __getitem__(self, k):
        return self._dict[k]

    def __setattr__(self, k, v):
        if k in {'_dict', '_ipython_canary_method_should_not_exist_'}:
            super(DotDict, self).__setattr__(k, v)
        else:
            self[k] = v

    def __getattr__(self, k):
        if k in {'_dict', '_ipython_canary_method_should_not_exist_'}:
            super(DotDict, self).__getattr__(k)
        else:
            return self[k]

    def __delattr__(self, key):
        return self._dict.__delitem__(key)

    def __contains__(self, k):
        return self._dict.__contains__(k)

    def __str__(self):
        return f"{DotDict.__name__}({str(self._dict)})"

    def __repr__(self):
        return str(self)

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if type(v) is DotDict:
                if id(v) == id(self):
                    v = d
                else:
                    v = v.to_dict()
            elif type(v) in (list, tuple):
                l = []
                for i in v:
                    n = i
                    if type(i) is DotDict:
                        n = i.to_dict()
                    l.append(n)
                if type(v) is tuple:
                    v = tuple(l)
                else:
                    v = l
            d[k] = v
        return d

    def empty(self):
        return not any(self)

    def values(self):
        return self._dict.values()

    def __dir__(self):
        return self.keys()

    @classmethod
    def _get_dict(self, other):
        if isinstance(other, DotDict):
            return other._dict
        else:
            return other

    def __cmp__(self, other):
        return self._dict.__cmp__(DotDict._get_dict(other))

    def __eq__(self, other):
        return self._dict.__eq__(DotDict._get_dict(other))

    def __ge__(self, other):
        return self._dict.__ge__(DotDict._get_dict(other))

    def __gt__(self, other):
        return self._dict.__gt__(DotDict._get_dict(other))

    def __le__(self, other):
        return self._dict.__le__(DotDict._get_dict(other))

    def __lt__(self, other):
        return self._dict.__lt__(DotDict._get_dict(other))

    def __ne__(self, other):
        return self._dict.__ne__(DotDict._get_dict(other))

    def __delitem__(self, key):
        return self._dict.__delitem__(key)

    def __len__(self):
        return self._dict.__len__()

    def clear(self):
        self._dict.clear()

    def copy(self):
        return DotDict(self)

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo=None):
        return self.copy()

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def has_key(self, key):
        return key in self._dict

    def keys(self):
        return self._dict.keys()

    def pop(self, key, default=None):
        return self._dict.pop(key, default)

    def popitem(self):
        return self._dict.popitem()

    def setdefault(self, key, default=None):
        self._dict.setdefault(key, default)

    def update(self, *args, **kwargs):
        if len(args) != 0:
            self._dict.update(*args)
        self._dict.update(kwargs)

    @classmethod
    def fromkeys(cls, seq, value=None):
        d = DotDict()
        d._dict = OrderedDict.fromkeys(seq, value)
        return d

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

