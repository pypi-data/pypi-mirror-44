# coding=utf-8

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import itertools
import random

import sopel.module
import sopel.formatting
import requests


def configure(config):
    pass


def setup(bot):
    pass


def request_api():
    """ Fetch json from checkiday api """
    r = requests.get('https://www.checkiday.com/api/3/?d')

    rj = r.json()

    if rj['error'] != 'none':
        raise ValueError('Api call returned error: {}'.format(rj['error']))

    return rj


def get_days_from_json(j):
    """ Return just the day names from the json response """
    return [i['name'] for i in j['holidays']]


def num_ranges(n, r):
    """ Return the split points of a number n at point r """
    o = 0
    yield o
    while n > r:
        o += r
        n -= r
        yield o
    yield o + n


def apply_colours(days, colours):
    """ Apply given colours to list of day names """
    cdays = [sopel.formatting.color(i, j)
             for i, j in zip(days, itertools.cycle(colours))]

    return cdays


def split_msg(days):
    """ Split the days based on the max irc message size of 400 """
    days_comma = ['{}, '.format(i) for i in days]
    acc = list(itertools.accumulate(len(i) for i in days_comma))
    nr = list(num_ranges(len(', '.join(days)), 400))
    ranges = zip(nr, nr[1:])
    msgs = [[i for i, a in zip(days, acc) if lower < a < upper]
            for lower, upper in ranges]
    return [', '.join(i) for i in msgs]


@sopel.module.commands('days')
def days(bot, trigger):
    rj = request_api()
    days = get_days_from_json(rj)
    colours = random.sample(['01', '02', '03', '04', '06', '08', '11'], 7)
    cdays = apply_colours(days, colours)

    for msg in split_msg(cdays):
        bot.say(msg)
