#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from string import Template


class Html(object):
    def __init__(self):

        self.rows = ''

    def add_line(self, filename1, filename2):
        html_svg1 = IMG.substitute(path=filename1, nombre=filename1)
        html_svg2 = IMG.substitute(path=filename2, nombre=filename2)
        row = ROW.substitute(fn1=html_svg1, fn2=html_svg2)
        self.rows += '\n' + row

    def crea_html(self):
        table = TABLE.substitute(rows=self.rows)
        texto = WEBPAGE.substitute(body=table,
                           estilos='estilos/graficas.css')

        f = codecs.open('resultado.html', "w", "utf-8")
        # Aplica template
        # relative_path_to_principal = '../' * nombre_archivo.count('/')
        f.write(texto)
        f.close()

TABLE = Template(
    u"""<table>
    $rows
    </table>
    """)

ROW =  Template(u"""
<tr>
    <th>$fn1</th>
    <th>$fn2</th>
</tr>
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

    <!-- JQuery -->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>


    </head>
    <body>

    $body

    </body>
    </html>

    """)