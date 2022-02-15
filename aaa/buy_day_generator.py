# The buy_day_generator() has too many accessories to be
# cleanly put into SimHandler. I'm giving it its own module. - Johann

from scipy.stats import norm, skewnorm
from typing import List, Any

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
import random


def reduce(sample: np.ndarray, count: int) -> List[float]:
    '''
    The z list from generate_buy_days() will have too many points (intended).
    One point for each person in the population is needed.
    The range has to be the same but not as many elements.

    :param sample: The List of points from where we derive a buy_day for each Attendee.
    :type sample: np.ndarray

    :param count: To how many elements do we condense the sample of values.
        Let it be an int (one for each person)
    :type count: int
    '''
    indexed: List = [item for item in enumerate(sample)]
    random.shuffle(indexed)
    trimmed = indexed[:count]
    trimmed.sort()
    return [item for index, item in trimmed]

def generate_buy_days(population: int,
                      days_until_concert: int,
                      granularity: float = 0.001) -> List[float]:
    '''
    Very few people would wait until the very last day to buy a
    ticket because it would be at its priciest. The majority of attendees
    will buy a ticket around the 5-10 day mark. The distribution of the ticket sales.
    by day wouldn't be uniform, just like how a population's height isn't.
    There's an average.

    :param population: Feed here the Attendee count.
    :type population: int

    :param days_until_concert: The number of days the ticket goes on sale.
    :type days_until_concert: int

    :param granularity: days_until_concert will be divided by granularity to determine resolution
        of points the from 0 until days_until_concert. This is given a default value.
    :type granularity: float

    :return: The list of ints with each int representing the predetermined buy day of a person.
    :rtype: List[int]
    '''

    # Difficulty typehinting these. They're NDArrays.
    x = np.arange(0, days_until_concert, granularity)
    z: List[float]  = reduce(x, population)

    return z
