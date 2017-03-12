#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from string import Template


class Html(object):
    def __init__(self):

        self.rows = ''
        self.pars = ''

    def add_line1(self, filename1, filename2):
        html_svg1 = IMG.substitute(path=filename1, nombre=filename1)
        html_svg2 = IMG.substitute(path=filename2, nombre=filename2)
        par = PAR_IMAGES.substitute(fn1=html_svg1, fn2=html_svg2)
        self.pars += '\n' + par

    def add_line(self, filename1, filename2):
        html_svg1 = IMG.substitute(path=filename1, nombre=filename1)
        html_svg2 = IMG.substitute(path=filename2, nombre=filename2)
        par = PAR_IMAGE.substitute(fn1=html_svg1, fn2=html_svg2)
        self.pars += '\n' + par


    def crea_html(self):
        texto = WEBPAGE.substitute(body=self.pars,
                           estilos='estilos/graficas.css')

        f = codecs.open('resultado.html', "w", "utf-8")
        # Aplica template
        # relative_path_to_principal = '../' * nombre_archivo.count('/')
        f.write(texto)
        f.close()


PAR_IMAGES =  Template(u"""
<p>$fn1 $fn2</p>
""")

PAR_IMAGE =  Template(u"""
<p>$fn1</p>
""")


IMG = Template(
    u'<img src="$path" alt="$path" title="$path" name="$nombre"></img>\n')


WEBPAGE = Template(u"""

    <!DOCTYPE html>
    <html lang="es">
    <head>

    <!-- Fonts -->
    <link href='http://fonts.googleapis.com/css?family=Droid+Sans' rel='stylesheet' type='text/css'>
<link href='http://fonts.googleapis.com/css?family=Oswald' rel='stylesheet' type='text/css'>
    <!-- Common headers -->
    <meta charset="utf-8" />

    <title> Gráficas </title>

    <!-- For iphone -->
    <meta name="viewport" content = "width = 660, user-scalable = yes" />

    <!-- Mi css -->
    <link rel="stylesheet" href="$estilos"  type="text/css" />
    <style>
        p {
            margin-top: 0px;
            margin-bottom: 0px;
        }
    </style>

    <!-- JQuery -->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>


    </head>
    <body>

    $body

    </body>
    </html>

    """)