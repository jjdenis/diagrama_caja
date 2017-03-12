#!/usr/bin/env python
# -*- coding: utf-8 -*-

import svgwrite
from copy import copy


grid_color = '#F2F2F2'

class Colores():
    def __init__(self):


        self.gris_muy_claro = svgwrite.rgb(240, 240, 240, 'RGB')
        self.gris_claro = svgwrite.rgb(189, 189, 189, 'RGB')
        self.gris_oscuro = svgwrite.rgb(150, 150, 150, 'RGB')

        self.negro = svgwrite.rgb(0, 0, 0, 'RGB')

        self.verde = svgwrite.rgb(49, 163, 84, 'RGB')

        self.azul_oscuro = svgwrite.rgb(166, 206, 227, 'RGB') #e5f5f9
        self.azul_claro = svgwrite.rgb(192, 220, 235, 'RGB')
        self.azul_muy_oscuro = svgwrite.rgb(66, 82, 90, 'RGB')



        self.verde_claro = svgwrite.rgb( 178, 223, 138, 'RGB') #e5f5f9
        self.verde_oscuro = svgwrite.rgb(51, 160, 44, 'RGB')


        self.muy_claro = self.gris_muy_claro
        self.claro = self.gris_claro
        self.oscuro = self.gris_oscuro
        self.muy_oscuro = self.negro

        self.limite = self.verde



class ConfigBarra(object):
    def __init__(self, colores, vmin=0., vmax=4000., grid=None, liminf=None, limsup=None):
        self.titulo = ''
        self.vmin = vmin
        self.vmax = vmax
        self.grid = grid
        self.liminf = liminf
        self.limsup = limsup

        self.x_ini_barra= 10
        self.ancho_barra = 500
        self.x_margen_dcho =20

        self.margen_superior = 20.0
        self.alto_barra = 20.0
        self.margen_inferior = 20
        self.y_ini_barra = self.margen_superior
        self.y_fin_barra = self.margen_superior + self.alto_barra
        self.y_cen_barra = self.margen_superior + self.alto_barra / 2

        self.ancho_svg = self.x_ini_barra + self.ancho_barra + self.x_margen_dcho
        self.alto_svg = self.margen_inferior + self.alto_barra +self.margen_inferior

        self.size = ('{}px'.format(self.ancho_svg), '{}px'.format(self.alto_svg))

        self.fondo_color = 'white'
        self.tipicos_color= colores.azul_claro
        self.intercuartil_color = colores.azul_oscuro
        self.atipicos_color=colores.azul_oscuro
        self.limite_color = colores.verde_oscuro
        self.value_color = colores.verde_oscuro
        self.titulo_color = colores.azul_muy_oscuro
        self.grid_color=colores.azul_muy_oscuro
        self.explicacion_color = colores.azul_muy_oscuro

        self.tipicos=True
        self.intercuartil=True
        self.atipicos=True
        self.grid=True
        self.grid_espaciado = 500 # Unidades de lo que sea
        self.grid_texto_espaciado = 2

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