# -*- coding: utf-8 -*-
import _pickle
import gzip
import pickle
from collections import defaultdict

import io


class GZDict:
    COMPRESS_LEVEL = 1

    def __init__(self, data, compress=False):
        self._data = data
        self._compress = compress

    def __getitem__(self, item):

        if self._compress:
            return _pickle.loads(gzip.decompress(self._data[item]))
        else:
            return self._data.__getitem__(item)

    def __setitem__(self, key, value):
        if self._compress:
            self._data[key] = gzip.compress(_pickle.dumps(value), self.COMPRESS_LEVEL)
        else:
            return self._data.__setitem__(key, value)

    def __delitem__(self, key):
        self._data.__delitem__(key)

    def __len__(self):
        return self._data.__len__()

    def __str__(self):
        if self._compress:
            return '{' + ', '.join(
                ["'%s': '%s'" % (a[0], _pickle.loads(gzip.decompress(a[1]))) for a in self._data.items()]) + '}'
        else:
            return self._data.__str__()

    def __repr__(self):
        if self._compress:
            return self.__str__()
        else:
            return self._data.__repr__()

    def __iter__(self):
        return self._data.__iter__()

    def keys(self):
        return self._data.keys()

    def values(self):
        if self._compress:
            for k in self.keys():
                yield self.__getitem__(k)
        else:
            self._data.values()

    def items(self):
        for k in self._data:
            yield ( k , self.__getitem__(k) )

    def __contains__(self, item):
        return self._data.__contains__(item)


class AliasDictError(BaseException):
    pass


class AliasDict(GZDict):

    def __init__(self, data=None, alias=None, ralias=None, compress=True):

        # for loading pickle
        if isinstance(data, io.IOBase):
            data_ls = pickle.load(data)
            self._alias_data = data_ls[0]
            self._ralias_data = data_ls[1]
            kwargs = data_ls[3]  # :dict
            super().__init__(data_ls[2], compress=kwargs.get("compress", True))

        elif isinstance(data, list):
            self._alias_data = data[0]
            self._ralias_data = data[1]
            kwargs = data[3]  # :dict
            super().__init__(data[2], compress=kwargs.get("compress", True))

        else:
            if alias is None:
                self._alias_data = dict()
            else:
                self._alias_data = alias

            if ralias is None:
                self._ralias_data = defaultdict(list)
            else:
                self._ralias_data = ralias

            if data is None:
                super().__init__(dict(), compress=compress)
            else:
                super().__init__(data, compress=compress)

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            pass

        if item in self.alias:
            try:
                return self.__getitem__(self.alias[item])
            except KeyError:
                pass
        raise KeyError(item)

    def __setitem__(self, key, value):
        if key in self.alias:
            true_key = self.alias[key]
            super().__setitem__(true_key, value)


        else:
            super().__setitem__(key, value)

    @property
    def data(self):
        return [self._alias_data, self._ralias_data, self._data, {"compress": self._compress}]

    def dumps(self):
        return pickle.dumps(self.data)

    def dump(self, file):
        return pickle.dump(self.data, file )

    @staticmethod
    def load(data):
        data = pickle.load(data)
        return AliasDict(data)

    @staticmethod
    def loads(data):
        return AliasDict(pickle.loads(data))

    @property
    def alias(self):
        return self._alias_data

    @property
    def ralias(self):
        return self._ralias_data

    def get_ralias(self, key):
        return self._ralias_data[key]

    def set_alias(self, true_key, alias):
        if super().__contains__(true_key):
            if not super().__contains__(alias):
                self.alias[alias] = true_key
                self.ralias[true_key].append(alias)
            else:
                raise AliasDictError("True Key Exists.:%s" % alias)
        else:

            if true_key in self.alias:
                true_key = self.alias[true_key]
                self.set_alias(true_key, alias)
            else:
                raise AliasDictError("True Key Not Exists:%s", true_key)

    def __delitem__(self, key):

        if super().__contains__(key):
            if key in self.ralias:
                aliases = self.ralias[key]
                del self.ralias[key]
                for alias in aliases:
                    del self.alias[alias]

            super().__delitem__(key)

        if key in self.alias:
            rkey = self.alias[key]
            del self.alias[key]
            if rkey in self.ralias and key in self.ralias[rkey]:
                self.ralias[rkey].remove(key)
            return

    def __contains__(self, item):
        if super().__contains__(item):
            return True
        elif item in self.alias:
            return True
        else:
            return False
