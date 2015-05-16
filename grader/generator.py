__author__ = 'dec'

import random
import re
import string


class Generator:
    def __init__(self):
        self.labs = {'lab1': self.gen_samples_lab1, 'lab2': self.gen_samples_lab2, 'lab3': self.gen_samples_lab3}
        self.num_of_samples = 7
        self.sample_length = 7

    @staticmethod
    def gen_output_lab_1(input_string):
        return input_string

    @staticmethod
    def gen_output_lab_2(input_string, change_from, change_into):
        return re.sub("[" + change_from + "]", change_into, input_string)

    @staticmethod
    def gen_output_lab_3(num_a, num_b):
        return num_a + num_b

    def gen_samples(self, lab, args):
        try:
            return self.labs[lab](args)
        except TypeError:
            return self.labs[lab](*args)

    def gen_samples_lab1(self):
        in_out = []
        for i in range(self.num_of_samples):
            random_string = Generator.random_string(self.sample_length, upper=True, lower=True, digits=True)
            in_out.append({'input': [random_string], 'output': self.gen_output_lab_1(random_string)})
        return in_out

    def gen_samples_lab2(self, change_from, change_to):
        in_out = []
        for i in range(self.num_of_samples):
            random_string = Generator.random_string(self.sample_length, upper=True, lower=True, digits=True)
            in_out.append({'input': [random_string, change_from, change_to],
                           'output': self.gen_output_lab_2(random_string, change_from,
                                                           change_to)})
        return in_out

    def gen_samples_lab3(self, bitness):
        in_out = {}
        for i in range(self.num_of_samples):
            num_a = Generator.random_number(0, (2 ** bitness) - 1)
            num_b = Generator.random_number(0, (2 ** bitness) - 1)
            in_out[(num_a, num_b)] = self.gen_output_lab_3(num_a, num_b)
        return in_out

    @classmethod
    def random_number(cls, l_bound, h_bound):
        return random.randint(l_bound, h_bound)

    @classmethod
    def random_string(cls, length, upper=False, lower=False, digits=False):
        random_string = ''.join(
            random.SystemRandom().choice((string.ascii_lowercase if upper else "") +
                                         (string.ascii_uppercase if lower else "") +
                                         (string.digits if digits else "")) for _ in range(length))
        return random_string
