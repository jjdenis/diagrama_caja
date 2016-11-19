#!/usr/bin/env python
# -*- coding: utf-8 -*-

import svgwrite


class Colores():
    def __init__(self):

        self.muy_claro = svgwrite.rgb(240, 240, 240, 'RGB')
        self.claro = svgwrite.rgb(217, 217, 217, 'RGB')
        self.oscuro = svgwrite.rgb(82, 82, 82, 'RGB')
        self.muy_oscuro = svgwrite.rgb(0, 0, 0, 'RGB')

        self.limite = svgwrite.rgb(49, 163, 84, 'RGB')


class ConfigBarra(object):
    def __init__(self, filename, colores, vorigin=0., vend=4000., grid=None, liminf=None, limsup=None):
        self.filename = filename
        self.vorigin = vorigin
        self.vend = vend
        self.grid = grid
        self.liminf = liminf
        self.limsup = limsup
        self.xorigin= 10
        self.xend = 500
        self.y = 30
        self.alto_barra = 20.0
        self.size = ('400px', '50px')

        self.not_outlier_zone=True
        self.not_outlier_zone_color= colores.muy_claro

        self.interquartile_zone=True
        self.interquartile_zone_color = colores.claro

        self.grid=True
        self.grid_color=colores.oscuro
        self.grid_space = 500
        self.outliers=True
        self.outliers_color=colores.muy_claro
        self.limite_color = colores.limite
        self.value_color = colores.muy_oscuro

        self.description_point = ''
        self.explanation = ''

