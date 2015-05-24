__author__ = 'dec'

import configparser
import os
import random
import re
import string
import sys

sys.path.append(os.path.expanduser("~") + "/.grader")

import lab6_function as lab6


class Generator:
    def __init__(self):
        config = configparser.RawConfigParser()
        config.read(os.path.expanduser("~") + "/.grader/.gen_config")

        self.labs = {'lab1': self.gen_samples_lab1,
                     'lab2': self.gen_samples_lab2,
                     'lab3': self.gen_samples_lab3,
                     'lab6': self.gen_samples_lab6}
        self.number_of_samples = config.getint("common", "number_of_samples")

        self.args = {"lab1": config.getint("lab1", "sample_length"),
                     "lab2": [config.getint("lab2", "sample_length"), config.get("lab2", "change_from"),
                              config.get("lab2", "change_to")],
                     "lab3": config.getint("lab3", "bitness"),
                     "lab6": lab6.func}

    @staticmethod
    def gen_output_lab_1(input_string):
        return input_string

    @staticmethod
    def gen_output_lab_2(input_string, change_from, change_into):
        return re.sub("[" + change_from + "]", change_into, input_string)

    # FIXME
    @staticmethod
    def gen_output_lab_3(num_a, num_b):
        return num_a + num_b

    @staticmethod
    def gen_output_lab_6(function, start, stop, step):
        return calculate_integral(function, start, stop, step)

    #TODO
    def gen_output_lab_7(function, start, stop, step):
        result = calculate_integral(function, start, stop, step)
        return "Wynik: " + str(result) + " Czas: "

    def gen_samples(self, lab):
        try:
            return self.labs[lab](self.args[lab])
        except TypeError:
            return self.labs[lab](*self.args[lab])

    def gen_samples_lab1(self, sample_length):
        in_out = []
        for i in range(self.number_of_samples):
            random_string = _random_string(sample_length, upper=True, lower=True, digits=True)
            in_out.append({'input': [random_string], 'output': self.gen_output_lab_1(random_string)})
        return in_out

    def gen_samples_lab2(self, sample_length, change_from, change_to):
        in_out = []
        for i in range(self.number_of_samples):
            random_string = _random_string(sample_length, upper=True, lower=True, digits=True)
            in_out.append({'input': [random_string, change_from, change_to],
                           'output': self.gen_output_lab_2(random_string, change_from, change_to)})
        return in_out

    # FIXME
    def gen_samples_lab3(self, bitness):
        in_out = []
        for i in range(self.number_of_samples):
            num_a = random.randint(0, (2 ** bitness) - 1)
            num_b = random.randint(0, (2 ** bitness) - 1)
            in_out.append({'input': [num_a, num_b], 'output': self.gen_output_lab_3(num_a, num_b)})
        return in_out

    def gen_samples_lab6(self, function):
        in_out = []
        for i in range(self.number_of_samples):
            start = random.randint(1, 100)
            stop = random.randint(start + 1, 100)
            step = random.uniform(0.1, 1)
            in_out.append({'input': [str(start), str(stop), str(step)],
                           'output': self.gen_output_lab_6(function, start, stop, step)})
        return in_out

def calculate_integral(function, start, stop, step):
    result = 0.0
    for i in _frange(start, stop, step):
        result += function(i)
    return result

def _random_string(length, upper=False, lower=False, digits=False):
    random_string = ''.join(
        random.SystemRandom().choice((string.ascii_lowercase if upper else "") +
                                     (string.ascii_uppercase if lower else "") +
                                     (string.digits if digits else "")) for _ in range(length))
    return random_string


def _frange(start, stop, step):
    """
    Generator that produces numbers in range <start; stop> with step
    :param start:
    :param stop:
    :param step:
    """
    while start <= stop:
        yield start
        start += step
