#!/usr/bin/env python
#-*- coding: utf-8 -*-

import datetime
import math
import random
import webbrowser
from dateutil.relativedelta import relativedelta

from src.barra import Barra
from src.html import Html
from src.spark import graph

from config import Colores, ConfigBarra
from src.descriptores import Descriptors


def main():

    today = datetime.datetime.today()
    fist_date = today + relativedelta(years=-1, month=1, day=3)
    num_weeks = 75
    dates = []

    for x in range(0, num_weeks):
        dates.append(fist_date+ relativedelta(weeks=x))

    html = Html()
    gen_filename = Filename()

    aleatorios = [float(random.randint(1500, 3000)) for i in dates]
    aleatorios[0] = 5
    aleatorios[1]=105

    colores = Colores()
    config = ConfigBarra(colores=colores)

    fn1, fn2 = gen_filename.gen_two()
    config.cambia(vmax=4000, liminf=500, limsup=3000)
    pinta_barra_y_spark(dates, aleatorios, fn1, fn2, config)
    html.add_line(fn1, fn2)

    crece_lineal = [i*3000/100. for i, d in enumerate(dates)]
    fn1, fn2 = gen_filename.gen_two()
    cf1 = config.nueva(vmax=6000)
    pinta_barra_y_spark(dates, crece_lineal, fn1, fn2, cf1)
    html.add_line(fn1, fn2)

    crece_lineal = [i*3000/100. for i, d in enumerate(dates)]
    fn1, fn2 = gen_filename.gen_two()
    pinta_barra_y_spark(dates, crece_lineal, fn1, fn2, config)
    html.add_line(fn1, fn2)

    values = [2000+math.cos(d)*500. for d in crece_lineal]
    fn1, fn2 = gen_filename.gen_two()
    pinta_barra_y_spark(dates, values, fn1, fn2, config)
    html.add_line(fn1, fn2)

    values = [2000+math.cos(d)*1500.*math.exp(-d/1000.) for d in crece_lineal]
    fn1, fn2 = gen_filename.gen_two()
    pinta_barra_y_spark(dates, values, fn1, fn2, config)
    html.add_line(fn1, fn2)

    values = [2000+math.cos(d)*1500.*math.exp(-d/1000.) for d in reversed(crece_lineal)]
    fn1, fn2 = gen_filename.gen_two()
    pinta_barra_y_spark(dates, values, fn1, fn2, config)
    html.add_line(fn1, fn2)

    values = [a + c for a, c in zip(aleatorios, crece_lineal)]
    fn1, fn2 = gen_filename.gen_two()
    pinta_barra_y_spark(dates, values, fn1, fn2, config)
    html.add_line(fn1, fn2)

    html.crea_html()
    webbrowser.open_new_tab('resultado.html')


def pinta_barra_y_spark(dates, values, fn1, fn2, config, vmin=None, vmax=None, liminf=None, limsup=None):

    descriptors = Descriptors(values)

    Barra(filename=fn1, cfg=config, descriptors=descriptors)

    graph(dates, values, fn2, config)

class Filename(object):
    def __init__(self):
        self.index = 0
        self.template = 'images/graf_redu{}.{}'

    def gen_one(self, extension='svg'):
        filename = self.template.format(self.index, extension)

        self.index += 1
        return filename


    def gen_two(self, extension='svg'):
        fn1 = self.template.format(self.index, extension)
        self.index += 1
        fn2 = self.template.format(self.index, extension)
        self.index += 1
        return fn1, fn2


main()

















