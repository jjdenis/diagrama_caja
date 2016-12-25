#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy
import json
import pprint

class ConfigBarra(object):
    def __init__(self, vmin=0., vmax=4000., grid=None, liminf=None, limsup=None):
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
        self.width = self.xmax+20
        self.height = self.y + self.alto_barra / 2 + 14 + 2 + 9 + 5

        self.value_width = 2
        self.not_outlier_zone=True
        self.not_outlier_zone_color= (240, 240, 240)  # muy claro

        self.interquartile_zone=True
        self.interquartile_zone_color = (217, 217, 217) # claro

        self.grid=True
        self.grid_color=(82, 82, 82)  # oscuro
        self.grid_space = 500
        self.outliers=True
        self.outliers_color=(240, 240, 240)  # muy claro
        self.limite_color = (49, 163, 84) # verdoso
        self.value_color = (0, 0, 0)  # negro

        self.description_point = ''
        self.explanation = ''
        self.unidades = ''

        self.json = json.dumps(self.__dict__, indent=4)
        print self.json


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