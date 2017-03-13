#!/usr/bin/env python
#-*- coding: utf-8 -*-
import svgwrite


class Barra(object):
    def __init__(self, filename, cfg, descriptors):
        self.filename = filename
        self.cfg = cfg
        self.descriptors = descriptors

        self.escala = cfg.ancho_barra / (cfg.vmax - cfg.vmin)
        self.xorigen = cfg. margen_izquierdo + cfg.ancho_descrip + cfg.margen_descrip_barra
        self.xfin = self.xorigen + cfg.ancho_barra

        self.y_ini_barra = cfg.margen_superior
        self.y_fin_barra = cfg.margen_superior + cfg.alto_barra
        self.y_cen_barra = cfg.margen_superior + cfg.alto_barra / 2

        self.x_descrip = cfg.margen_izquierdo
        self.y_descrip = self.y_cen_barra

        self.ancho_svg = cfg.margen_izquierdo + cfg.ancho_descrip + cfg.margen_descrip_barra + cfg.ancho_barra + cfg.margen_dcho
        self.alto_svg = cfg.margen_superior + cfg.alto_barra + cfg.margen_inferior
        dimensiones = ('{}px'.format(self.ancho_svg), '{}px'.format(self.alto_svg))
        self.dwg = svgwrite.Drawing(filename, dimensiones, profile='tiny')

        self.fondo_svg()

        self.fondo_barra()

        if cfg.tipicos:
            self.tipicos(descriptors.first_non_outlier, descriptors.last_non_outlier)
        if cfg.intercuartil:
            self.intercuartil(descriptors.quartile_1, descriptors.quartile_3)

        self.mediana()

        if cfg.atipicos:
            self.atipicos(descriptors.atipicos)
        if cfg.liminf:
            self.lim_inf()
        if cfg.limsup:
            self.lim_sup()


        self.ultimo_valor(descriptors.ultimo)

        if cfg.grid:
            self.grid()

        texto_titulo = u'{} - {:.0f} {} - {}'.format(self.cfg.titulo, self.descriptors.ultimo, self.cfg.unidades, 'semana pasada')
        texto_titulo = u'{}'.format(self.cfg.titulo)
        self.titulo(texto_titulo)

        #self.explanation(u'Datos semanales, ultimo dato la semana pasada', color1=self.cfg.grid_color)

        self.texto_valor()


        self.save()

    def mediana(self):
        cmediana = self.x_coord(self.descriptors.mediana)
        median1 = self.dwg.polygon(
            [(cmediana - 4, self.y_ini_barra),
             (cmediana + 4, self.y_ini_barra),
             (cmediana, self.y_ini_barra + 2)],
            fill='white'
        )
        self.dwg.add(median1)
        median2 = self.dwg.polygon(
            [(cmediana - 4, self.y_fin_barra),
             (cmediana + 4, self.y_fin_barra),
             (cmediana, self.y_fin_barra - 2)],
            fill='white'
        )
        self.dwg.add(median2)

    def texto_valor(self):
        y_pos_texto = self.y_cen_barra + self.cfg.alto_barra / 2 + 14
        text = u'{:.0f} {}'.format(self.descriptors.ultimo, self.cfg.unidades)
        self.label_at_value(self.descriptors.ultimo, text, y_pos_texto, font_size="12px", color=self.cfg.value_color)

    def titulo(self, titulo):
        # Upper label
        if abs(self.descriptors.mediana - self.cfg.vmax) < (self.cfg.vmax - self.cfg.vmin) * 0.2:
            text_anchor = 'end'
            position = self.cfg.vmax
        else:
            text_anchor = 'middle'
            position = self.descriptors.mediana

        y_pos_texto = self.y_cen_barra - self.cfg.alto_barra / 2 - 2

        coords = (self.x_coord(position), y_pos_texto)

        coords = (self.x_descrip, self.y_descrip)

        text_anchor = 'start'
        # coords = (self.xorigen, self.y_cen_barra + self.cfg.alto_barra)
        t = self.dwg.text(titulo, insert=coords, fill=self.cfg.titulo_color, font_family="sans-serif", font_size="14px",
                          text_anchor=text_anchor)
        self.dwg.add(t)

    

    def fondo_svg(self):
        fondo = self.dwg.rect((0, 0),
                              (self.ancho_svg, self.alto_svg),
                              stroke='white',
                              fill='white'
                              )
        self.dwg.add(fondo)

    def fondo_barra(self):
        ini = (self.xorigen, self.y_cen_barra)
        fin = (self.xorigen + self.cfg.ancho_barra, self.y_cen_barra)
        fondo = self.dwg.line(ini, fin, stroke_width=self.cfg.alto_barra, stroke=self.cfg.fondo_color)
        self.dwg.add(fondo)


    def tipicos(self, inicio, fin):
        c_inicio = self.x_coord(inicio)
        c_fin = self.x_coord(fin)
        self.line(c_inicio, c_fin, stroke_width=self.cfg.alto_barra, stroke=self.cfg.tipicos_color)


    def intercuartil(self, inicio, fin):
        c_inicio = (self.x_coord(inicio), self.y_cen_barra)
        c_fin = (self.x_coord(fin), self.y_cen_barra)

        intercuartil = self.dwg.line(c_inicio,
                                     c_fin,
                                     stroke_width=self.cfg.alto_barra,
                                     stroke=self.cfg.intercuartil_color,
                                     opacity=1)
        self.dwg.add(intercuartil)

    def atipicos(self, atipicos):
        for value in atipicos:
            coord = self.x_coord(value)
            self.line(coord-1, coord+1, stroke_width=self.cfg.alto_barra-10, stroke=self.cfg.atipicos_color)

    def ultimo_valor(self, valor):
        coord = self.x_coord(valor)
        line = self.dwg.line((coord-2, self.y_cen_barra), (coord+2, self.y_cen_barra),
                             stroke_width=self.cfg.alto_barra, stroke=self.cfg.value_color)
        self.dwg.add(line)

    def x_coord(self, value):
        coord = self.xorigen + (value - self.cfg.vmin) * self.escala
        return coord

    def lim_inf(self):
        c_inicio = self.x_coord(self.cfg.liminf)
        line = self.dwg.line((c_inicio-5, self.y_cen_barra-5), (c_inicio, self.y_cen_barra), stroke_width=2, stroke=self.cfg.limite_color)
        self.dwg.add(line)
        line = self.dwg.line((c_inicio, self.y_cen_barra), (c_inicio-5, self.y_cen_barra + 5), stroke_width=2, stroke=self.cfg.limite_color)
        self.dwg.add(line)

    def lim_sup(self):
        c_inicio = self.x_coord(self.cfg.limsup)
        line = self.dwg.line((c_inicio+5, self.y_cen_barra-5), (c_inicio, self.y_cen_barra), stroke_width=2, stroke=self.cfg.limite_color)
        self.dwg.add(line)
        line = self.dwg.line((c_inicio, self.y_cen_barra), (c_inicio+5, self.y_cen_barra + 5), stroke_width=2, stroke=self.cfg.limite_color)
        self.dwg.add(line)

    def grid(self):
        value = 0

        y_pos_tick = self.y_fin_barra + 3

        y_pos_texto = y_pos_tick + 7

        i = 0

        while value <= self.cfg.vmax:
            cubre_valor = abs(value-self.descriptors.ultimo) < self.cfg.grid_espaciado * 1.0

            toca_texto = i % self.cfg.grid_texto_espaciado == 0

            if cubre_valor:
                pass
            else:

                if toca_texto:
                    self.label_at_value(value, u'{:.0f}'.format(value), y_pos_texto, color=self.cfg.grid_color,  font_size="12px")
                else:
                    coord = self.x_coord(value)
                    ini = (coord, y_pos_tick + 2)
                    fin = (coord, y_pos_tick + 4)

                    # self.line(coord - 1, coord + 1, stroke_width=self.stw, stroke=color, opacity=0.5)
                    line = self.dwg.line(ini, fin ,
                                         stroke_width=2, stroke=self.cfg.grid_color,
                                         opacity=0.5)
                    self.dwg.add(line)


            value += self.cfg.grid_espaciado
            i += 1

                # self.line(coord-1, coord+1, stroke_width=self.stw-10, stroke=color)

    def title(self, value, text, color='black'):
        t = self.dwg.text(text, insert=(self.xorigen, self.y_cen_barra-15), fill=color, font_family="sans-serif", font_size="14px")
        self.dwg.add(t)

    def line(self, ini, fin, stroke_width, stroke, opacity=1):
        line = self.dwg.line((ini, self.y_cen_barra), (fin, self.y_cen_barra), stroke_width=stroke_width, stroke=stroke, opacity=opacity)
        self.dwg.add(line)

    def label_at_value(self, value, text, y_coordenada, color='black', font_size="9px", text_anchor='middle'):
        coords = (self.x_coord(value), y_coordenada)
        # coords = (self.xorigen, self.y_cen_barra + self.cfg.alto_barra)
        t = self.dwg.text(text, insert=coords, fill=color, font_family="sans-serif", font_size=font_size, text_anchor=text_anchor)
        self.dwg.add(t)


    # def name(self, text1, text2, color='black'):
    #     t = self.dwg.text(text1, insert=(self.xorigen, self.y_cen_barra-15), fill=color, font_family="sans-serif", font_size="14px")
    #     tspan = self.dwg.tspan(text2, font_family="sans-serif", font_size="9px")
    #     t.add(tspan)
    #     self.dwg.add(t)


    def explanation(self, text1, color1='black', text2='', color2='black'):
        # Son dos textos, con dos colores
        coords = (self.xorigen, self.y_cen_barra + self.cfg.alto_barra / 2 + 14 + 2 +9)
        t = self.dwg.text(text1, insert=coords, fill=color1, font_family="sans-serif", font_size="9px")
        tspan = self.dwg.tspan(text2, font_family="sans-serif", font_size="9px", fill=color2)
        t.add(tspan)
        self.dwg.add(t)

    def save(self):
        self.dwg.save()