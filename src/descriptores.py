#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Descriptors(object):
    def __init__(self, values):
        self.values = values
        self.maximo = max(values)
        self.ultimo = values[-1]

        values = sorted(values)
        self.length = len(values)

        self.media = sum(values) / self.length

        index = int(self.length * .25)
        self.quartile_1 = values[index]

        index = self.length/2
        self.median = values[index]

        index = int(self.length * .75)
        self.quartile_3 = values[index]

        interaquartile = self.quartile_3 - self.quartile_1

        self.lower_regular_range = self.quartile_1 - 1.5 * interaquartile

        self.upper_regular_range = self.quartile_3 + 1.5 * interaquartile

        self.first_non_outlier = next(v for v in values if v > self.lower_regular_range)

        self.last_non_outlier = next(v for v in reversed(values) if v < self.upper_regular_range)

        self.outliers = [v for v in values if v < self.lower_regular_range or v > self.upper_regular_range]

        self.json = json.dumps(self.__dict__)

        print self.json