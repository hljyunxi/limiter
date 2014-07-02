#!/usr/bin/env python
#coding: utf8

import weakref

TIME_UNIT = {
    'DAY': (60*60*24, 'day'),
    'MONTH': (60*60*24*30, 'month'),
    'YEAR': (60*60*24*30*12, 'year'),
    'HOUR': (60*60, 'hour'),
    'MINUTE': (60, 'minute'),
    'SECOND': (1, 'second'),
}

GRANULARITIES = []

class LimitMetaType(type):
    def __new__(cls, name, parents, dct):
        granularity = super(LimitMetaType, cls).__new__(cls,\
                name, parents, dct)

        if 'granularity' in dct:
            GRANULARITIES.append(granularity)
        return granularity


class LimitItem(object):
    __metaclass__ = LimitMetaType

    def __init__(self, amount, multiples = 1, namespace="LIMITER"):
        self.amount = int(amount)
        self.multiples = int(multiples) if multiples else 1
        self.namespace = namespace

    def key_for(self, *identifiers):
        remainder = '/'.join(identifiers + (str(self.multiples),\
                self.granularity[1]))

        return '%s/%s' % (self.namespace, remainder)

    @classmethod
    def match_granularity_str(cls, granularity_str):
        return granularity_str in cls.granularity[1:]

    @property
    def expiry(self):
        return self.multiples * self.granularity[0]

    def __eq__(self, other):
        return (self.amount == other.amount) and\
                (self.granularity==other.granularity)


class PER_YEAR(LimitItem):
    granularity = TIME_UNIT['YEAR']


class PER_MONTH(LimitItem):
    granularity = TIME_UNIT['MONTH']


class PER_DAY(LimitItem):
    granularity = TIME_UNIT['DAY']


class PER_HOUR(LimitItem):
    granularity = TIME_UNIT['HOUR']


class PER_MINUTE(LimitItem):
    granularity = TIME_UNIT['MINUTE']


class PER_SECOND(LimitItem):
    granularity = TIME_UNIT['SECOND']


class LimitItemManager(object):
    def __init__(self, storage):
        self.storage = weakref.ref(storage)

    def hit(self, item, *identifiers):
        return (
            self.storage().set_and_get(item.key_for(*identifiers), item.expiry)\
                    <= item.amount
        )

    def check(self, item):
        self.storage().get(item.key) < item.amount
