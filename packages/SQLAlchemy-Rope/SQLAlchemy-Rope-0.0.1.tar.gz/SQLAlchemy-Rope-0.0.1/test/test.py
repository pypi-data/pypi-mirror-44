from weakref import WeakValueDictionary


class S:
    pass

wd = WeakValueDictionary()
wd["s"] = S()
print(dict(wd))
print(dict(wd))