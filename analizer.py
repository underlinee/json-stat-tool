#!/usr/bin/python

import abc
import gzip
import json

ABC = abc.ABCMeta('ABC', (object,), {})


class Analizer(ABC):

    @abc.abstractmethod
    def result(self):
        pass

    @abc.abstractmethod
    def put(self, log):
        pass

    def analize(self, files):
        for file in files:
            with gzip.open(file) as f:
                for line in f:
                    log_dict = json.loads(line)
                    self.put(log_dict)
        return self.result()
