#!/usr/bin/env python
# -*- coding: utf-8 -*-

import svgwrite
from copy import copy


grid_color = '#F2F2F2'

class Colores():
    def __init__(self):

        self.muy_claro = svgwrite.rgb(240, 240, 240, 'RGB')
        self.claro = svgwrite.rgb(217, 217, 217, 'RGB')
        self.oscuro = svgwrite.rgb(82, 82, 82, 'RGB')
        self.muy_oscuro = svgwrite.rgb(0, 0, 0, 'RGB')

        self.limite = svgwrite.rgb(49, 163, 84, 'RGB')


class ConfigBarra(object):
    def __init__(self, colores, vmin=0., vmax=4000., grid=None, liminf=None, limsup=None):
        self.titulo = ''
        self.vmin = vmin
        self.vmax = vmax
        self.grid = grid
        self.liminf = liminf
        self.limsup = limsup
        self.xmin= 10
        self.xmax = 500
        self.y = 30.0
        self.alto_barra = 20.0
        self.size = ('{}px'.format(self.xmax+20), '{}px'.format(self.y+self.alto_barra / 2 + 14 + 2 + 9 + 5   ))

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
        self.unidades = ''

    def cambia(self, **kwargs):
        for key, value in kwargs.iteritems():
            if key in self.__dict__:
                self.__dict__[key]=value
            else:
                raise ValueError('El parametro {} no existe'.format(key))

    def nueva(self, **kwargs):
        new = copy(self)
        new.cambia(**kwargs)
        return new