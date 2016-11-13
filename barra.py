import svgwrite

muy_claro = svgwrite.rgb(204, 204, 204, 'RGB')
claro = svgwrite.rgb(150, 150, 150, 'RGB')
oscuro = svgwrite.rgb(82, 82, 82, 'RGB')
muy_oscuro = svgwrite.rgb(0, 0, 0, 'RGB')
limite = svgwrite.rgb(49, 163, 84, 'RGB')


class Barra(object):
    def __init__(self, filename, xorigin, xend, y, vorigin, vend):
        self.dwg = svgwrite.Drawing(filename, size=('400px', '50px'), profile='tiny')

        self.xorigin = float(xorigin)
        self.xend=xend
        self.y = float(y)
        self.stw = 20.0
        self.vorigin = float(vorigin)
        self.vend = float(vend)

        self.scale = (self.xend - self.xorigin) / (self.vend - self.vorigin)

        line = self.dwg.line((xorigin,y), (xend,y), stroke_width=self.stw, stroke='white', opacity=0.1)
        self.dwg.add(line)

    def value(self, value):
        coord = self.coord_value(value)
        line = self.dwg.line((coord-2,self.y), (coord+2, self.y), stroke_width=self.stw, stroke=muy_oscuro)
        self.dwg.add(line)

    def coord_value(self, value):
        coord = self.xorigin + (value - self.vorigin) * self.scale
        return coord

    def espacio(self, inicio, fin, color='blue'):
        c_inicio = self.coord_value(inicio)
        c_fin = self.coord_value(fin)
        self.line(c_inicio, c_fin, stroke_width=self.stw, stroke=color)

    def line(self, ini, fin, stroke_width, stroke, opacity=1):
        line = self.dwg.line((ini, self.y), (fin, self.y), stroke_width=stroke_width, stroke=stroke, opacity=opacity)
        self.dwg.add(line)

    def lim_inf(self, value):
        c_inicio = self.coord_value(value)
        line = self.dwg.line((c_inicio-5, self.y-5), (c_inicio, self.y), stroke_width=2, stroke=limite)
        self.dwg.add(line)
        line = self.dwg.line((c_inicio, self.y), (c_inicio-5, self.y + 5), stroke_width=2, stroke=limite)
        self.dwg.add(line)

    def lim_sup(self, value):
        c_inicio = self.coord_value(value)
        line = self.dwg.line((c_inicio+5, self.y-5), (c_inicio, self.y), stroke_width=2, stroke=limite)
        self.dwg.add(line)
        line = self.dwg.line((c_inicio, self.y), (c_inicio+5, self.y + 5), stroke_width=2, stroke=limite)
        self.dwg.add(line)


    def outliers(self, outliers, color = 'blue'):
        for value in outliers:
            coord = self.coord_value(value)
            self.line(coord-1, coord+1, stroke_width=self.stw-10, stroke=color)

    def grid(self, space, color='white'):
        value = 0
        while value <= self.vend:
            coord = self.coord_value(value)
            # self.line(coord - 1, coord + 1, stroke_width=self.stw, stroke=color, opacity=0.5)
            line = self.dwg.line((coord, self.y + self.stw / 2), (coord, self.y + self.stw / 2 + 2), stroke_width=2, stroke='grey',
                                     opacity=0.5)
            value += space

            self.dwg.add(line)
            # self.line(coord-1, coord+1, stroke_width=self.stw-10, stroke=color)

    def descrption_point(self, value, text, color='black'):
        coord = self.coord_value(value)
        t = self.dwg.text(text, insert=(self.xorigin, self.y-15), fill=color, font_family="sans-serif", font_size="14px")
        self.dwg.add(t)


    # def name(self, text1, text2, color='black'):
    #     t = self.dwg.text(text1, insert=(self.xorigin, self.y-15), fill=color, font_family="sans-serif", font_size="14px")
    #     tspan = self.dwg.tspan(text2, font_family="sans-serif", font_size="9px")
    #     t.add(tspan)
    #     self.dwg.add(t)


    def explanation(self, text1, color1='black', text2='', color2='black'):
        t = self.dwg.text(text1, insert=(self.xorigin, self.y + self.stw), fill=color1, font_family="sans-serif", font_size="9px")
        tspan = self.dwg.tspan(text2, font_family="sans-serif", font_size="9px", fill=color2)
        t.add(tspan)
        self.dwg.add(t)

    def save(self):
        self.dwg.save()