#!/usr/bin/env python
#-*- coding: utf-8 -*-

import math
import random
import webbrowser

from barra import Barra
from config import Colores, ConfigBarra
from descriptores import Descriptors
from html import Html
from spark import graph

grid_color = '#F2F2F2'

from dateutil.relativedelta import relativedelta
import datetime


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

    pinta_y_genera_html(aleatorios, dates, gen_filename, html)

    crece_lineal = [i*3000/100. for i, d in enumerate(dates)]
    pinta_y_genera_html(crece_lineal, dates, gen_filename, html)

    values = [2000+math.cos(d)*500. for d in crece_lineal]
    pinta_y_genera_html(values, dates, gen_filename, html)

    values = [2000+math.cos(d)*1500.*math.exp(-d/1000.) for d in crece_lineal]
    pinta_y_genera_html(values, dates, gen_filename, html)

    values = [2000+math.cos(d)*1500.*math.exp(-d/1000.) for d in reversed(crece_lineal)]
    pinta_y_genera_html(values, dates, gen_filename, html)

    values = [a + c for a, c in zip(aleatorios, crece_lineal)]
    pinta_y_genera_html(values, dates, gen_filename, html)

    html.crea_html()
    webbrowser.open_new_tab('prueba.html')


def pinta_y_genera_html(aleatorios, dates, gen_filename, html):

    filename1 = gen_filename.next()
    crea_barra(aleatorios, filename1)

    filename2 = gen_filename.next()
    graph(dates, aleatorios, filename2)


    html.add_line(filename1, filename2)



def crea_barra(values, filename):

    descriptors = Descriptors(values)
    colores = Colores()
    c= ConfigBarra(filename, colores=colores, liminf = 300, limsup=1000)

    barra = Barra(cfg=c, descriptors=descriptors)


class Filename(object):
    def __init__(self):
        self.index = 0
        self.template = 'scatter{}.{}'

    def next(self, extension='svg'):
        filename = self.template.format(self.index, extension)

        self.index += 1
        return filename


main()

















