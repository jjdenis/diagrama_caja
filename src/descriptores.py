#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Descriptors(object):

    def __init__(self, valores):


        self.maximo = max(valores)

        self.ultimo = valores[-1]

        valores = sorted(valores)
        num_valores = len(valores)

        self.media = sum(valores) / num_valores

        index = int(num_valores * .25)
        self.quartile_1 = valores[index]

        index = num_valores / 2
        self.mediana = valores[index]

        index = int(num_valores * .75)
        self.quartile_3 = valores[index]

        intercuartil = self.quartile_3 - self.quartile_1

        self.lower_regular_range = self.quartile_1 - 1.5 * intercuartil

        self.upper_regular_range = self.quartile_3 + 1.5 * intercuartil

        self.first_non_outlier = next(v for v in valores if v > self.lower_regular_range)

        self.last_non_outlier = next(v for v in reversed(valores) if v < self.upper_regular_range)

        self.atipicos = [v for v in valores if v < self.lower_regular_range or v > self.upper_regular_range]