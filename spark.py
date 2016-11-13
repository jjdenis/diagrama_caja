#!/usr/bin/env python
#-*- coding: utf-8 -*-

import datetime
from dateutil.relativedelta import relativedelta

import matplotlib
from matplotlib import pyplot as plt


def graph(dates, values, filename):
    matplotlib.rc('font', size=6,
                  #family    = 'Baskerville',
                  family='sans-serif',
                  #family    = 'monospace',
                  )

    fig = plt.figure(num=None, figsize=(2, 0.7), dpi=80, facecolor='w', edgecolor='k')

    ax = plt.subplot()
    set_eje_x(u'2años', ax)
    set_eje_y(ax, 0, 4000)
    tick_lines(ax)
    set_y_labels(ax)
    ax.plot(dates, values, alpha=1, color='black')
    # ax.set_axis_off()

    fig.tight_layout()
    fig.canvas.print_figure(filename)

    return

def set_y_labels(ax):
    labels = ax.get_yticks().tolist()
    print(labels)
    last = labels[-1]
    new_labels = []
    for label in labels:
        new_labels.append('')
    new_labels[-1]='{:.0f}'.format(labels[-1])
    new_labels[0]='{:.0f}'.format(labels[0])
    ax.set_yticklabels(new_labels)

def set_eje_y(ax, ymin, ymax):
    # Eje y
    ax.axis(ymin=ymin, ymax=ymax)
    ax.yaxis.tick_right()
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('grey')


def set_eje_x(alcance, ax, freq=['week'], ):
    today = datetime.datetime.today()
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('grey')

    # Eje x
    if alcance == u'2años':
        xmin = today + relativedelta(years=-1, month=1, day=1)
        # xmax = today + relativedelta(months=3, day=31)
        xmax = today + relativedelta(month=12, day=31)
        ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator(12))
        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(mes_y_anyo))
        # ax.xaxis.set_major_formatter(matplotlib.ticker.NullFormatter())
        # if 'month' in freq:
        #     ax.xaxis.set_minor_locator(matplotlib.dates.MonthLocator())
        # else:
        #     ax.xaxis.set_minor_locator(
        #         matplotlib.dates.MonthLocator(bymonthday=15))
        # ax.xaxis.set_minor_formatter(matplotlib.ticker.FuncFormatter(tres_letras_del_mes))

    else:  # 1 mes
        xmin = today + relativedelta(months=-1, day=1)
        # xmin = today + relativedelta(weeks=-5, weekday=SU)
        # xmax = today + relativedelta(weeks=0,  weekday=calendar.SUNDAY)
        xmax = today + relativedelta(months=0, day=31)

        # # ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
        # ax.xaxis.set_major_locator(
        #     matplotlib.dates.WeekdayLocator(byweekday=SU))
        #
        # ax.xaxis.set_major_formatter(matplotlib.ticker.NullFormatter())
        #
        # # ax.xaxis.set_minor_locator(matplotlib.dates.WeekdayLocator(byweekday=SU))
        # ax.xaxis.set_minor_locator(matplotlib.dates.DayLocator())
        #
        # ax.xaxis.set_minor_formatter(matplotlib.ticker.FuncFormatter(dia))

    ax.axis(xmin=xmin, xmax=xmax)


def tick_lines(ax):

    # Lineas tick invisibles, poniéndolas del mismo color que el fondo
    for tline in ax.yaxis.get_majorticklines():
        tline.set_color('white')
    # for tline in ax.yaxis.get_minorticklines():
    #    tline.set_color(grid_color)
    for tline in ax.xaxis.get_majorticklines():
        tline.set_color('white')


    # for tline in ax.xaxis.get_minorticklines():
    #    tline.set_color(grid_color)


def primera_letra_del_mes(f, pos=0):
    return datetime.date.fromordinal(int(f)).strftime('%b')[0]


def tres_letras_del_mes(f, pos=0):
    return datetime.date.fromordinal(int(f)).strftime('%B')[0:3]


def mes_y_anyo(f, pos=0):
    date = datetime.date.fromordinal(int(f))
    mes = date.strftime('%B')[0:1]
    year = date.fromordinal(int(f)).strftime('%Y')[2:4]
    return '{}{}'.format(mes, year)


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













def graph1(dates, values, filename):
    y = [1]*len(values)
    fig = plt.figure(num=None, figsize=(12, 1), dpi=80, facecolor='w', edgecolor='k')

    gs = GridSpec(1, 4)


    ax = plt.subplot(gs[0, 1:])
    last_value = values[-1]
    colors = plt.cm.Blues(np.linspace(0, 1, len(dates)))
    sizes = np.linspace(0, 100, len(dates))
    ax.scatter(values, y, c=colors, s=sizes, alpha=1, edgecolors='none')
    ax.plot(last_value, 1, 'o', color='red', markeredgecolor='red', markeredgewidth=5)
    ax.annotate(
        'hola',
        color='blue',
        xy=(last_value, 1),
        # xy=(0.01 * default_sizex * ppp * 0.55,
        #     (sizey - (1 - 0.95) * default_sizey) * ppp * 0.59),  # 0.576),
        # Tal vez mejor fijar el titulo principal con 'axes fraction' y anotar el
        # título secundario desplazado respecto el principal con 'offset points'
        # igual que se hace con la anotación de las expresiones
        # xycoords = 'axes fraction',
        # xycoords = 'axes fraction',
        # xycoords = 'figure points',
        xytext=(4, 10),
        textcoords='offset points',
        ha='left',
        va='center',
        size=16,
        # bbox=bbox,
        # arrowprops=dict(facecolor='white', shrink=0.05, ec='white'),
        zorder=9,
    )
    # ax.set_xlabel('Lio', fontsize=20)
    # ax.set_ylabel(r'gordo', fontsize=20)
    # ax.set_title('Volume and percent change')
    # ax.set_axis_off()
    ax.get_yaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('bottom')

    ax = plt.subplot(gs[0, 0])
    ax.plot(dates, values, alpha=1)
    ax.set_axis_off()

    fig.tight_layout()
    fig.canvas.print_figure(filename)

    return


