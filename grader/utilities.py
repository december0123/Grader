__author__ = 'dec'

import random
import string


def calculate_integral(function, start, stop, num_of_steps):
    result = 0.0
    step = (stop - start) / num_of_steps
    for i in range(num_of_steps):
        result += function(start + i * step)
    return result * step


def get_random_string(length, upper=False, lower=False, digits=False):
    random_string = ''.join(
        random.SystemRandom().choice((string.ascii_lowercase if upper else "") +
                                     (string.ascii_uppercase if lower else "") +
                                     (string.digits if digits else "")) for _ in range(length))
    return random_string


def frange(start, stop, step):
    """
    Generator that produces numbers in range <start; stop> with step
    :param start:
    :param stop:
    :param step:
    """
    while start <= stop:
        yield start
        start += step

def calc_relative_error(model, actual):
    import math
    try:
        return math.fabs(model - float(actual)) / model
    except ValueError as e:
        correct_letters = 0
        for i in range(0, len(model)):
            if model[i] == actual[i]:
                correct_letters += 1
        return 1 - correct_letters / len(model)

