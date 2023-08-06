# DotDict implementation for Python 3


Production ready implementation of a dictionary allowing dot style access to stored values.

Raises KeyError if the corresponding key does not exist.


## Usage

```

    >>> d = dict(a=1, b=2)
    >>> dd = DotDict(d)
    >>> dd.a
    1
    >>> dd.b
    2

```

