#!/usr/bin/env python
#coding: utf8

import re
from limiter.limits import GRANULARITIES

RATE_EXPR = re.compile(
    r"\s*([0-9]+)\s*(/|\s*per\s*)\s*([0-9]+)*\s*(hour|minute|second|day|month|year)[s]*",
    re.IGNORECASE
)


def parse_many(limit_string):
    """

    :param 速率: 10 per hour; 1 per second
    :raise ValueError
    """
    if not RATE_EXPR.match(limit_string):
        raise ValueError("couldn't parse rate limit string '%s'" % limit_string)
    for amount, _, multiples, granularity_string in  RATE_EXPR.findall(limit_string):
        granularity = granularity_from_string(granularity_string)
        yield granularity(amount, multiples)

def parse(limit_string):
    """

    :param 速率: 10 per hour; 1 per second
    :return RateItem
    """
    return list(parse_many(limit_string))[0]


def granularity_from_string(granularity_string):
    """

    :param 速率: 10 per hour; 1 per second
    :return: RateItem
    :raise ValueError
    """
    for granularity in GRANULARITIES:
        if granularity.match_granularity_str(granularity_string):
            return granularity
    raise ValueError("no granularity matched for %s" % granularity_string)
