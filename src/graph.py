#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import logging
import sys
import datetime
import locale


import dateutil.relativedelta
from dateutil.relativedelta import *
from dateutil.rrule import *

import pandas

import matplotlib as matplotlib
matplotlib.use('Agg')  # before importing pyplot

from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D


import codecs

logger = logging.getLogger('main')

sistema_operativo = 'osx'
if sistema_operativo == 'osx':
    locale.setlocale(locale.LC_ALL, 'es_ES')
elif sistema_operativo == 'linux':
    locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

paper_white = '#EBE7E0'
paper_black = 'black'
paper_blue = '#000069'
paper_red = '#FF0000'
paper_grey = '#E3DDDe'
axaragua_color = '#264a97'

grid_color = '#F2F2F2'
backg_color = 'white'
letters_color = axaragua_color
default_sizex = 16
default_sizey = 8


def paint_graph(
    pinta_si=u'',
    data=[],
    names=[],
    colors=[],
    alphas=[],
    title='',
    expression='',
    filepath='',
    ymax=0,
    ymin=0,
    location='',
    short_name='',
    limits=[],
    dinamic_limits=[],
    dinamic_lim_names=[],
    din_lim_alpha=0.3,
    alarm=0,
    path_alarm='',
    units='g',
    letters_color=letters_color,
    grid_color=grid_color,
    backg_color=backg_color,  # 'white',
    grid=grid_color,
    linewidth=4,
    drawstyle='line',
    linestyle='solid',
    markersize=4,
    annotate_last_value=[True] * 10,
    freq=['week'],
    alcance=u'2años',
    legend=False,
    sizex=default_sizex,         # Tamaño en pulgadas de la gráfica
    sizey=default_sizey,
):
    with codecs.open("graficas.txt", 'a', 'UTF-8') as f:
        f.write(filepath)
        f.write('\n')

    if pinta_si and (pinta_si not in filepath):
        return filepath

    #logger.debug(u'Pintando {}'.format(short_name))
    logger.debug(u'Pintando {}'.format(title))
    # Si no hay datos, vuelve

    for d, n in zip(data + dinamic_limits, names + dinamic_lim_names):
        if d.count() < 1:
            logger.debug(
                u'No hay datos para {} de {} en {}'.format(
                    short_name, n, location))
            return filepath

    # first_date  = min( [ds.index.min() for ds in data + dinamic_limits])
    last_date = max([ds.index.max() for ds in data + dinamic_limits])
    today = datetime.datetime.today()

    last_values = []
    for ds in data + dinamic_limits:
        for d in reversed(ds):
            if not pandas.isnull(d):
                last_values.append(d)
                break

    max_last_value = max(last_values)
    min_last_value = min(last_values)

    # Si los valores son muy altos, reescala
    if (max_last_value > 0.9 * ymax):
        logger.debug(
            u'warning: valores muy altos en la gráfica de {}: {} frente\
              \na {} --> reescalamos'.format(short_name, max_last_value, ymax))
        ymax = max_last_value * 1.1

    # Si los valores son muy bajos, reescala
    if min_last_value < ymin:
        ymin = min_last_value * 1.1

    #y_height = (sizey-2*fig_pad_inches)/(ymax-ymin)

    matplotlib.rc('font', size=10,
                  #family    = 'Baskerville',
                  family='sans-serif',
                  #family    = 'monospace',
                  )
    matplotlib.rc('pdf', fonttype=42)
    # Pone la rejilla por detrás
    matplotlib.rc('axes', axisbelow='True', hold=True, edgecolor=backg_color)
    matplotlib.rc('path', simplify='True')

    ppp = 100  # dpi
    fig_pad_inches = 0.3
    matplotlib.rc('figure', figsize=(sizex, sizey), dpi = ppp)  # 72
    # matplotlib.rc('figure', figsize = (12, 6), dpi = 100)  # 72
    matplotlib.rc('figure', facecolor=backg_color)
    matplotlib.rc('legend', fontsize=9)
    matplotlib.rc('mathtext', default='regular')

    fig = plt.figure()
    #ax  = fig.add_subplot(111)
    ax = host_subplot(111)
    #ax_med = ax.twiny()

    ax2 = ax.twin()

    # Text background box
    bbox = {'fc': 'white', 'ec': 'white', 'boxstyle': 'round,pad=0'}

    # Eje y
    ax.axis(ymin=ymin, ymax=ymax)
    ax.yaxis.tick_right()

    # Eje x
    if alcance == u'2años':
        xmin = today + relativedelta(years=-1, month=1, day=1)
        # xmax = today + relativedelta(months=3, day=31)
        xmax = today + relativedelta(month=12, day=31)
        ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
        ax.xaxis.set_major_formatter(ticker.NullFormatter())
        if 'month' in freq:
            ax.xaxis.set_minor_locator(matplotlib.dates.MonthLocator())
        else:
            ax.xaxis.set_minor_locator(
                matplotlib.dates.MonthLocator(bymonthday=15))
        ax.xaxis.set_minor_formatter(ticker.FuncFormatter(tres_letras_del_mes))

    else:  # 1 mes
        xmin = today + relativedelta(months=-1, day=1)
        #xmin = today + relativedelta(weeks=-5, weekday=SU)
        #xmax = today + relativedelta(weeks=0,  weekday=calendar.SUNDAY)
        xmax = today + relativedelta(months=0,  day=31)

        # ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
        ax.xaxis.set_major_locator(
            matplotlib.dates.WeekdayLocator(byweekday=SU))

        ax.xaxis.set_major_formatter(ticker.NullFormatter())

        # ax.xaxis.set_minor_locator(matplotlib.dates.WeekdayLocator(byweekday=SU))
        ax.xaxis.set_minor_locator(matplotlib.dates.DayLocator())

        ax.xaxis.set_minor_formatter(ticker.FuncFormatter(dia))

        if title:
            title += " - {} y {}".format(
                (last_date + relativedelta(months=-1)).strftime("%B"), last_date.strftime("%B"))

    # print xmin, xmax
    ax.axis(xmin=xmin, xmax=xmax)
    #
    #xmax = datetime.datetime.today()+relativedelta(day=31, month=12)
    #ax.axis(xmax = xmax )

    for tick in ax.xaxis.get_minor_ticks():
        tick.label1.set_verticalalignment('baseline')
        tick.label1.set_y(-0.02)
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)

    # Lineas tick invisibles, poniéndolas del mismo color que la grid
    for tline in ax.yaxis.get_majorticklines():
        tline.set_color(grid_color)
    # for tline in ax.yaxis.get_minorticklines():
    #    tline.set_color(grid_color)
    for tline in ax.xaxis.get_majorticklines():
        tline.set_color(grid_color)
    # for tline in ax.xaxis.get_minorticklines():
    #    tline.set_color(grid_color)

    # Rejilla (pinta los sábados y domingos más anchos, y la separación entre
    # años también)
    ax.xaxis.grid(
        True, which='major', color=grid, linestyle='solid', linewidth=1)
    #ax.xaxis.grid(True, which='major', color=grid, linestyle='solid', linewidth=8)
    for fecha in rrule(YEARLY, dtstart=xmin, until=xmax)[1:]:
        ax.axvline(x=fecha, ymin=0, ymax=1, color=grid, linewidth=8)

    if alcance != u'2años':
        ax.xaxis.grid(
            True, which='major', color=grid, alpha=0.5, linestyle='solid', linewidth=30)
        ax.xaxis.grid(
            True, which='minor', color=grid, linestyle='solid', linewidth=1)

    #ax.xaxis.grid(True, which='minor', color=grid, linestyle='solid', linewidth=1)

    ax.yaxis.grid(
        True, which='major', color=grid, linestyle='solid', linewidth=2)
    #ax.yaxis.grid(True, which='minor', color=grid, linestyle='solid', linewidth=1)

    # Pinta línea horizontal en y=0 si hay valores negativos
    if ymin < 0:
        ax.axhline(y=0, xmin=0, xmax=1, linestyle='--')

    # pinta el título
    # ax.set_title(title, fontsize=10, color= 'blue')

    t_from = ''
    t_what = ''

    if '-' in title:
        t_from = title.split('-', 1)[0].strip()
        t_what = title.split('-', 1)[1].strip()
    else:
        t_from = location
        t_what = title

    ax.annotate(
        t_what,
        color=letters_color,
        #xy=(0.01, 0.95),
        xy=(0.01 * default_sizex * ppp * 0.55,
            (sizey - (1 - 0.95) * default_sizey) * ppp * 0.59),  # 0.576),
        # Tal vez mejor fijar el título principal con 'axes fraction' y anotar el
        # título secundario desplazado respecto el principal con 'offset points'
        # igual que se hace con la anotación de las expresiones
        #xycoords = 'axes fraction',
        xycoords = 'axes points',
        #xycoords = 'figure points',
        ha = 'left',
        va = 'center',
        size=16,
        bbox=bbox,
        # arrowprops=dict(facecolor='white', shrink=0.05, ec='white'),
        zorder = 9,
    )

    title2 = t_from + ' ' + \
        datetime.datetime.today().strftime(
            '%a, %d de %b de %y').decode('utf_8')

    ax.annotate(
        title2,
        #location + ' ' +short_name,
        color=letters_color,
        #xy=(0.01, 0.92),
        xy=(0.01 * default_sizex * ppp * 0.55,
            (sizey - (1 - 0.92) * default_sizey) * ppp * 0.59),
        # Tal vez mejor fijar el título principal con 'axes fraction' y anotar el
        # título secundario desplazado respecto el principal con 'offset points'
        # igual que se hace con la anotación de las expresiones
        #xycoords = 'axes fraction',
        xycoords = 'axes points',
        ha = 'left',
        va = 'center',
        size=12,
        bbox=bbox,
        # arrowprops=dict(facecolor='white', shrink=0.05, ec='white'),
        zorder = 9,
    )

    # pinta la expresión de lo que se representa
    ax.annotate(
        expression,
        color=letters_color,
        xy=(0, 0.92),
        xycoords = 'axes fraction',
        xytext = (20, -20),
        textcoords = 'offset points',
        ha = 'left',
        va = 'top',
        size=10,
        bbox=bbox,
        # arrowprops=dict(facecolor='white', shrink=0.05, ec='white'),
        zorder = 9,
    )

    # Eje x2
    ax2.xaxis.set_major_locator(matplotlib.dates.YearLocator(month=7))
    ax2.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y'))

    # Eje y2
    ax2.yaxis.set_major_formatter(ticker.NullFormatter())

    zipped_data = list(
        zip(data, names, colors, alphas, freq, annotate_last_value))
    # ordena los datos por su último valor, de menor a mayor
    zipped_data.sort(key=lambda i: i[0][-1])
    # print zipped_data

    # Comprueba que las listas de datos tienen una longitud mínima
    num_datos = len(data)

    def l_correcta(ls):
        if len(ls) < num_datos:
            return False
        return True
    l = map(l_correcta, [names, colors, alphas, freq, annotate_last_value])
    if not reduce(lambda x, y: x and y, l):
        print u"LONGITUD INCORRECTA"

    for ds, name, color, alpha, frequency, annotate in zipped_data:
        # Pinta la entrada
        dates = ds.index
        values = ds
        # print ds
        ax.plot(dates,  # Col dates
                values,  # Col values
                color=color,
                alpha=alpha,
                linewidth=linewidth,
                linestyle=linestyle,
                solid_capstyle='round',
                solid_joinstyle='round',
                marker='o',
                markeredgecolor=color,
                markersize=markersize,
                drawstyle=drawstyle,
                # solid_joinstyle='bevel',
                label=name
                )

        last_value = values[-1]
        last_date = dates[-1]
        for v, d in reversed(zip(values, dates)):
            if not pandas.isnull(v):
                last_value = v
                last_date = d
                break
        if annotate:
            # Anota el último valor de cada
            sn = u''
            if short_name:
                sn = short_name + ' - '

            text = sn + name + '\n' + \
                float_to_text_3_significant(
                    last_value) + ' ' + units + '\n' + date_in_text(last_date, frequency)
            ax.annotate(
                text,
                # float_to_text_3_significant(in_d[-1,1]),
                color=color,
                #xy     = (last_value_date, (last_value_value + 0.05) * factor  + offset ),
                #xytext = (last_value_date, (last_value_value + 0.25) * factor  + offset ),
                xy=(last_date, last_value),
                xytext = (4, 0),
                textcoords = 'offset points',
                ha = 'left',
                va = 'center',
                size=8,
                bbox=bbox,
                # arrowprops=dict(facecolor='white', shrink=0.05, ec='white'),
                zorder = 9,
            )

    if legend:
        leyenda = ax.legend(loc='best').set_zorder(9)

    # Límites dinámicos

    for ds, name in zip(dinamic_limits, dinamic_lim_names):
        # Pinta la entrada
        dates = ds.index
        values = ds
        ax.plot(dates,  # Col dates
                values,  # Col values
                color='blue',
                linewidth=1,
                linestyle='--',
                solid_capstyle='round',
                solid_joinstyle='round',
                drawstyle=drawstyle,
                marker='.',
                markersize=2,
                alpha=din_lim_alpha,
                )

        last_value = values[-1]
        last_date = dates[-1]
        for v, d in reversed(zip(values, dates)):
            if not pandas.isnull(v):
                last_value = v
                last_date = d
                break

        # Anota el último valor de cada
        text = name
        ax.annotate(
            text,
            color='blue',
            xy=(last_date, last_value),
            xytext = (4, 0),
            textcoords = 'offset points',
            ha = 'left',
            va = 'center',
            size=8,
            bbox=bbox,
            # arrowprops=dict(facecolor='white', shrink=0.05, ec='white'),
            zorder = 8,
        )

    # Banda entre límites dinámicos

    if len(dinamic_limits) == 2:
        dates = dinamic_limits[0].index
        ax.fill_between(dates, dinamic_limits[0], dinamic_limits[1],
                        facecolor='yellow', alpha=0.4, linewidth=0)

    # Linea de límite
    for limit in limits:
        parameter = Line2D([0, 1],
                           [(float(limit) - ymin) / (ymax - ymin),
                            (float(limit) - ymin) / (ymax - ymin)],
                           transform=ax.transAxes,
                           linewidth=1,
                           linestyle='--',
                           color='blue',
                           zorder=9
                           )
        ax.lines.append(parameter)

        ax.annotate(
            float_to_text_3_significant(limit) + ' ' + units,
            # float_to_text_3_significant(in_d[-1,1]),
            color='blue',
            #xy     = (last_value_date, (last_value_value + 0.05) * factor  + offset ),
            #xytext = (last_value_date, (last_value_value + 0.25) * factor  + offset ),
            xy=(xmax, limit),
            #transform = ax.transAxes,
            xytext = (-4, 5),
            textcoords = 'offset points',
            ha = 'right',
            va = 'center',
            size=8,
            bbox=bbox,
            # arrowprops=dict(facecolor='white', shrink=0.05, ec='white'),
            zorder = 9,
        )
        '''
        absolute_or_reduction(limit=35, in_d=in_d, reduction=0.75)
        ax.fill_between(limit[:,0], limit[:,1], np.interp(limit[:,0], out_d[:,0], out_d[:,1]))
        '''

    # Banda entre límites

    if len(limits) == 2:
        ax.fill_between([0, 1],
                        [(float(limits[0]) - ymin) / (ymax - ymin),
                         (float(limits[0]) - ymin) / (ymax - ymin)],
                        [(float(limits[1]) - ymin) / (ymax - ymin),
                         (float(limits[1]) - ymin) / (ymax - ymin)],
                        transform=ax.transAxes,
                        facecolor='yellow', alpha=0.4, linewidth=0)

    # Crea la gráfica
    try:
        plt.savefig(filepath,
                    # facecolor=fig.get_facecolor(),
                    facecolor=grid_color,
                    # edgecolor=backg_color,
                    edgecolor=grid_color,
                    bbox_inches='tight',
                    pad_inches=fig_pad_inches,
                    dpi=ppp,
                    # pad_inches=0.01,
                    )
    except KeyboardInterrupt:
        raise
    except:
        logger.error("Error pintando grafica" + str(sys.exc_info()[0]))
        raise

    plt.close(fig)

    return filepath


def hora_sin_minutos(f, pos=0):
    d = matplotlib.dates.num2date(f, tz=None)
    if int(d.strftime('%H')) < 6 and d.strftime('%d') != tmax.strftime('%d'):
        return ''
    return d.strftime('%H')


def primera_letra_del_mes(f, pos=0):
    return datetime.date.fromordinal(int(f)).strftime('%b')[0]


def tres_letras_del_mes(f, pos=0):
    return datetime.date.fromordinal(int(f)).strftime('%B')[0:3]


def dia(f, pos=0):
    d = datetime.date.fromordinal(int(f))
    ds = d.strftime('%a')
    if ds[0:2] == 'mi':
        ds = 'X'
    else:
        ds = ds[0:1].upper()

    # if d.day==1:
    #     return "1"+d.strftime('%B')[0:3].lower()
    if ds == "L":
        return '          L' + d.strftime('%d').lstrip('0') + d.strftime('%B')[0:3].lower()
    else:
        return ''

    return ds


def nombre_del_mes(f, pos=0):
    return datetime.date.fromordinal(int(f)).strftime('%B')


def float_to_text_3_significant(value):
    if value > 100:
        text = "%.0f" % value
    elif value > 10:
        text = "%.1f" % value
    elif value > 1:
        text = "%.2f" % value
    else:
        text = "%.3f" % value

    if text.find('.') != -1:
        if text[-1] == '0':
            text = text[0:-1]
        if text[-1] == '0':
            text = text[0:-1]

    if text[-1] == '.':
        text = text[0:-1]

    return text


def no_pintes_nada(f, pos=0):
    return ''


def date_in_text(date, frequency):
    # Para que el texto sea correcto la frecuencia que se especifique
    # en la definición de la gráfica debe coincidir con la menor
    # frecuencia de muestreo de los datos que se pintan (si los datos
    # son semanales y se dice que la frecuencia es diaria, el texto
    # que resulta no es correcto)

    tdy = datetime.datetime.now()
    tdy = tdy.replace(hour=23, minute=59)

    ago = relativedelta(tdy, date)
    ago_months = ago.months + 12 * ago.years
    # ago_weeks = ago.weeks # Esto no funciona

    if frequency == 'month':
        dt_txt = date.strftime("%B")
        return dt_txt

    if frequency == 'week':
        # ago_weeks = tdy.isocalendar()[1] - date.isocalendar()[1] # No
        # funciona en los cambios de año
        ago_weeks = iso_weeks_between_dates(tdy, date)
        #dt_txt = u''
        if ago_weeks == 0:
            dt_txt = u'esta semana'
        elif ago_weeks == 1:
            dt_txt = u'la semana pasada'
        else:
            dt_txt = u'hace {} semanas'.format(ago_weeks)
        return dt_txt

    # frequency in ('day', 'hour'):
    if ago_months == 0:
        if ago.days == 0:
            dt_txt = u'ayer'
        elif ago.days == 1:
            dt_txt = u'anteayer'
        # elif ago.days > 1 and ago < 8:
        #    dt_txt = u'hace {} días'.format(ago.days)
        else:
            dt_txt = u'hace {} días'.format(ago.days)
    else:
        if ago_months == 1:
            if ago.days == 0:
                dt_txt = u'hace 1 mes justo'
            elif ago.days == 1:
                dt_txt = u'hace 1 mes y 1 día'
            else:
                dt_txt = u'hace 1 mes y {} días'.format(ago.days)
        else:
            if ago.days == 0:
                dt_txt = u'hace {} meses justos'.format(ago_months)
            elif ago.days == 1:
                dt_txt = u'hace {} meses y 1 día'.format(ago_months)
            else:
                dt_txt = u'hace {} meses y {} días'.format(
                    ago_months, ago.days)

    return dt_txt


def iso_weeks_between_dates(date_1, date_2):
    if date_1 < date_2:
        return -iso_weeks_between_dates(date_2, date_1)

    iso_weeks_ago = 0
    while date_1.isocalendar()[0:2] != date_2.isocalendar()[0:2]:
        date_1 += relativedelta(weeks=-1)
        iso_weeks_ago += 1
    return iso_weeks_ago
