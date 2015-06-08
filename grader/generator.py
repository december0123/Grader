__author__ = 'dec'

import configparser
import os
import random
import re
import sys

sys.path.append(os.path.expanduser("~") + "/.grader")
import lab6_function as lab6
import lab7_function as lab7

import utilities as util


class Generator:
    def __init__(self, number_of_tests=None, sample_length=None):
        config = configparser.RawConfigParser()
        config.read(os.path.expanduser("~") + "/.grader/gen_config")

        self.labs = {'lab1': self.gen_tests_lab1,
                     'lab2': self.gen_tests_lab2,
                     'lab3': self.gen_tests_lab3,
                     'lab6': self.gen_tests_lab6,
                     'lab7': self.gen_tests_lab6}

        self.args = {"lab1": config.getint("lab1", "sample_length"),
                     "lab2": [config.getint("lab2", "sample_length"),
                              config.get("lab2", "change_from"),
                              config.get("lab2", "change_to")],
                     "lab3": [config.getint("lab3", "bitness"),
                              config.get("lab3", "operation")],
                     "lab6": lab6.func,
                     "lab7": lab7.func}

        if number_of_tests is None:
            self.number_of_tests = config.getint("common", "number_of_tests")
        else:
            self.number_of_tests = number_of_tests

        if sample_length is not None:
            self.args["lab1"] = sample_length
            self.args["lab2"][0] = sample_length

    @staticmethod
    def gen_output_lab_1(input_string):
        return input_string

    @staticmethod
    def gen_output_lab_2(input_string, change_from, change_into):
        return re.sub("[" + change_from + "]", change_into, input_string)

    @staticmethod
    def gen_output_lab_3(num_a, num_b, operation):
        result = hex(num_a) + operation + hex(num_b)
        return hex(eval(result))

    @staticmethod
    def gen_output_lab_6(function, start, stop, num_of_steps):
        return util.calculate_integral(function, start, stop, num_of_steps)

    def gen_tests(self, lab):
        try:
            return self.labs[lab](self.args[lab])
        except TypeError:
            return self.labs[lab](*self.args[lab])

    def gen_tests_lab1(self, sample_length):
        in_out = []
        for i in range(self.number_of_tests):
            random_string = util.get_random_string(sample_length, upper=True, lower=True, digits=True)
            in_out.append({'input': [random_string], 'output': self.gen_output_lab_1(random_string)})
        return in_out

    def gen_tests_lab2(self, sample_length, change_from, change_to):
        in_out = []
        for i in range(self.number_of_tests):
            random_string = util.get_random_string(sample_length, upper=True, lower=True, digits=True)
            in_out.append({'input': [random_string, change_from, change_to],
                           'output': self.gen_output_lab_2(random_string, change_from, change_to)})
        return in_out

    def gen_tests_lab3(self, bitness, op):
        in_out = []
        for i in range(self.number_of_tests):
            num_a = random.randint(0, 2 ** (bitness - 1))
            num_b = random.randint(0, 2 ** (bitness - 1))
            in_out.append({'input': [hex(num_a), hex(num_b)], 'output': self.gen_output_lab_3(num_a, num_b, op)})
        return in_out

    def gen_tests_lab6(self, function):
        in_out = []
        for i in range(self.number_of_tests):
            start = random.randint(1, 100)
            stop = random.randint(start + 1, 200)
            num_of_steps = 10000
            in_out.append({'input': [str(start), str(stop), str(num_of_steps)],
                           'output': self.gen_output_lab_6(function, start, stop, num_of_steps)})
        return in_out
