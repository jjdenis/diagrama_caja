#!/usr/bin/env python
#-*- coding: utf-8 -*-
import math
import random
import webbrowser

from barra import Barra
from descriptors import Descriptors
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


import svgwrite

muy_claro = svgwrite.rgb(229, 245, 224, 'RGB')
claro = svgwrite.rgb(161, 217, 155, 'RGB')
oscuro = svgwrite.rgb(49, 163, 84, 'RGB')


muy_claro = svgwrite.rgb(204, 204, 204, 'RGB')
claro = svgwrite.rgb(150, 150, 150, 'RGB')
oscuro = svgwrite.rgb(82, 82, 82, 'RGB')
muy_oscuro = svgwrite.rgb(0, 0, 0, 'RGB')
limite = svgwrite.rgb(49, 163, 84, 'RGB')


def crea_barra(values, filename, vorigin=0., vend=4000., grid=500, liminf=1500, limsup=3000):

    descriptors = Descriptors(values)

    barra = Barra(filename, xorigin=10., xend=300., y=25, vorigin=vorigin, vend=vend)
    barra.espacio(descriptors.first_non_outlier, descriptors.last_non_outlier, muy_claro)
    barra.espacio(descriptors.quartile_1, descriptors.quartile_3, claro)
    barra.grid(grid)
    barra.outliers(descriptors.outliers, claro)
    barra.value(descriptors.ultimo)
    barra.lim_inf(liminf)
    barra.lim_sup(limsup)
    barra.descrption_point(descriptors.ultimo, u'{} - {:.0f} μS/cm² - {}'.format(u'Conductividad entrada', descriptors.ultimo, 'La semana pasada'), color=muy_oscuro)
    barra.explanation(u'Datos semanales')
    barra.save()


class Filename(object):
    def __init__(self):
        self.index = 0
        self.template = 'scatter{}.{}'

    def next(self, extension='svg'):
        filename = self.template.format(self.index, extension)

        self.index += 1
        return filename


main()

















