#!/usr/bin/env python
#-*- coding: utf-8 -*-
import svgwrite


class Barra(object):
    def __init__(self, filename, cfg, descriptors):
        self.filename = filename
        self.scale = (cfg.xmax - cfg.xmin) / (cfg.vmax - cfg.vmin)
        self.cfg = cfg
        self.descriptors = descriptors

        self.xorigin = cfg.xmin
        self.xend=cfg.xmax

        self.dwg = svgwrite.Drawing(filename, self.cfg.size, profile='tiny')

        line = self.dwg.line((cfg.xmin, cfg.y), (cfg.xmax, cfg.y),
                             stroke_width=self.cfg.alto_barra, stroke='white', opacity=0.1)
        self.dwg.add(line)

        if cfg.not_outlier_zone:
            self.not_oulier_zone(descriptors.first_non_outlier, descriptors.last_non_outlier)

        if cfg.interquartile_zone:
            self.interquartile_zone(descriptors.quartile_1, descriptors.quartile_3)

        if cfg.grid:
            self.grid(self.cfg.grid_space)

        if cfg.outliers:
            self.outliers(descriptors.outliers)
        if cfg.liminf:
            self.lim_inf(cfg.liminf)
        if cfg.limsup:
            self.lim_sup(cfg.limsup)

        self.value(descriptors.ultimo)

        # Upper label
        texto = u'{}'.format(self.cfg.titulo)
        if abs(self.descriptors.ultimo - self.cfg.vmax) < (self.cfg.vmax-self.cfg.vmin)*0.2:
            text_anchor = 'end'
            position = self.cfg.vmax
        else:
            text_anchor = 'middle'
            position = self.descriptors.ultimo
        self.label_at_value(position, texto, position = 'top', font_size="14px", text_anchor=text_anchor)

        self.explanation(u'Datos semanales, ultimo dato la semana pasada')

        text = u'{:.0f} {}'.format(self.descriptors.ultimo, self.cfg.unidades)
        self.label_at_value(self.descriptors.ultimo, text, font_size="14px")

        self.save()

    def value(self, value):
        coord = self.coord_value(value)
        line = self.dwg.line((coord-2, self.cfg.y), (coord+2, self.cfg.y),
                             stroke_width=self.cfg.alto_barra, stroke=self.cfg.value_color)
        self.dwg.add(line)

    def coord_value(self, value):
        coord = self.xorigin + (value - self.cfg.vmin) * self.scale
        return coord

    def interquartile_zone(self, inicio, fin):
        c_inicio = self.coord_value(inicio)
        c_fin = self.coord_value(fin)
        self.line(c_inicio, c_fin, stroke_width=self.cfg.alto_barra, stroke=self.cfg.interquartile_zone_color)

    def not_oulier_zone(self, inicio, fin):
        c_inicio = self.coord_value(inicio)
        c_fin = self.coord_value(fin)
        self.line(c_inicio, c_fin, stroke_width=self.cfg.alto_barra, stroke=self.cfg.not_outlier_zone_color)

    def lim_inf(self, value):
        c_inicio = self.coord_value(value)
        line = self.dwg.line((c_inicio-5, self.cfg.y-5), (c_inicio, self.cfg.y), stroke_width=2, stroke=self.cfg.limite_color)
        self.dwg.add(line)
        line = self.dwg.line((c_inicio, self.cfg.y), (c_inicio-5, self.cfg.y + 5), stroke_width=2, stroke=self.cfg.limite_color)
        self.dwg.add(line)

    def lim_sup(self, value):
        c_inicio = self.coord_value(value)
        line = self.dwg.line((c_inicio+5, self.cfg.y-5), (c_inicio, self.cfg.y), stroke_width=2, stroke=self.cfg.limite_color)
        self.dwg.add(line)
        line = self.dwg.line((c_inicio, self.cfg.y), (c_inicio+5, self.cfg.y + 5), stroke_width=2, stroke=self.cfg.limite_color)
        self.dwg.add(line)


    def outliers(self, outliers):
        for value in outliers:
            coord = self.coord_value(value)
            self.line(coord-1, coord+1, stroke_width=self.cfg.alto_barra-10, stroke=self.cfg.outliers_color)

    def grid(self, space):
        value = 0
        while value <= self.cfg.vmax:
            coord = self.coord_value(value)
            ini = (coord, self.cfg.y + self.cfg.alto_barra / 2)
            fin = (coord, self.cfg.y + self.cfg.alto_barra / 2 + 2)

            # self.line(coord - 1, coord + 1, stroke_width=self.stw, stroke=color, opacity=0.5)
            line = self.dwg.line(ini, fin ,
                                 stroke_width=2, stroke=self.cfg.grid_color,
                                 opacity=0.5)

            if abs(value-self.descriptors.ultimo) > self.cfg.grid_space * 1.0:
                self.label_at_value(value, u'{:.0f}'.format(value))

            value += space

            self.dwg.add(line)
            # self.line(coord-1, coord+1, stroke_width=self.stw-10, stroke=color)

    def title(self, value, text, color='black'):
        t = self.dwg.text(text, insert=(self.xorigin, self.cfg.y-15), fill=color, font_family="sans-serif", font_size="14px")
        self.dwg.add(t)

    def line(self, ini, fin, stroke_width, stroke, opacity=1):
        line = self.dwg.line((ini, self.cfg.y), (fin, self.cfg.y), stroke_width=stroke_width, stroke=stroke, opacity=opacity)
        self.dwg.add(line)

    def label_at_value(self, value, text, color='black', font_size="9px", position='bottom', text_anchor='middle'):
        if position == 'top':
            y = self.cfg.y - self.cfg.alto_barra / 2 - 2
        else:
            y = self.cfg.y + self.cfg.alto_barra / 2 + 14
        print value, text
        coords = (self.coord_value(value), y)
        # coords = (self.xorigin, self.cfg.y + self.cfg.alto_barra)
        print coords
        t = self.dwg.text(text, insert=coords, fill=color, font_family="sans-serif", font_size=font_size, text_anchor=text_anchor)
        self.dwg.add(t)


    # def name(self, text1, text2, color='black'):
    #     t = self.dwg.text(text1, insert=(self.xorigin, self.cfg.y-15), fill=color, font_family="sans-serif", font_size="14px")
    #     tspan = self.dwg.tspan(text2, font_family="sans-serif", font_size="9px")
    #     t.add(tspan)
    #     self.dwg.add(t)


    def explanation(self, text1, color1='black', text2='', color2='black'):
        coords = (self.xorigin, self.cfg.y + self.cfg.alto_barra / 2 + 14 + 2 +9)
        t = self.dwg.text(text1, insert=coords, fill=color1, font_family="sans-serif", font_size="9px")
        tspan = self.dwg.tspan(text2, font_family="sans-serif", font_size="9px", fill=color2)
        t.add(tspan)
        self.dwg.add(t)

    def save(self):
        self.dwg.save()