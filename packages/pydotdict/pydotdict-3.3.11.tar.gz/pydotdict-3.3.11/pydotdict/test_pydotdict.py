import pickle
import pytest
import copy
from pydotdict.pydotdict import DotDict


@pytest.fixture
def testdict():
    d = dict(a=1, b=2, c=dict(a=3))
    return d


def test_basics(testdict):
    dd = DotDict(testdict)
    assert dd == testdict
    assert len(dd) == len(testdict)
    assert len(copy.copy(dd)) == len(testdict)


def test_pickle(testdict):
    dd = DotDict(testdict)
    s = pickle.dumps(dd)
    d = pickle.loads(s)
    assert d == dd


def test_keys(testdict):
    dd = DotDict(testdict)
    with pytest.raises(KeyError):
        _ = dd.nonexistingkey

