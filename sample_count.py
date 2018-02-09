#!/usr/bin/python

from analizer import Analizer


class SampleCount(Analizer):

    def __init__(self):
        self.count = 0

    def put(self, log):
        self.count += 1

    def result(self):
        return self.count
