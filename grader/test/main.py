#!/usr/bin/env python3.1
__author__ = 'dec'

import os
import re
import unittest

from grader.grader import Grader
from grader.generator import Generator

from grader.utilities import calc_relative_error


class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.number_of_tests = 7
        self.sample_length = 7
        self.g = Generator(number_of_tests=self.number_of_tests, sample_length=self.sample_length)

    def test_lab_1_gen_output_for_given_input(self):
        input_string = "test"
        self.assertEqual(input_string, Generator.gen_output_lab_1(input_string))

    def test_lab_1_gen_dict_of_inputs_and_outputs(self):
        in_out = self.g.gen_tests_lab1(self.sample_length)
        self.assertEqual(len(in_out), self.number_of_tests)
        for test in in_out:
            self.assertEqual(test["input"][0], test["output"])
            self.assertEqual(len(test["input"][0]), self.sample_length)

    def test_lab_2_gen_output_for_given_input(self):
        input_string = "test string WITH lower ANd UppER Case leTTERS"
        output_string = "t*st str*ng W*TH l*w*r *Nd *pp*R C*s* l*TT*RS"
        change_from = "AEIOUYaeiouy"
        change_into = "*"
        self.assertEqual(output_string, Generator.gen_output_lab_2(input_string, change_from, change_into))

    def test_lab_2_gen_dict_of_inputs_and_outputs(self):
        change_from = "AIEUOY"
        change_into = "&"
        in_out = self.g.gen_tests_lab2(self.sample_length, change_from, change_into)
        self.assertEqual(len(in_out), self.number_of_tests)
        for test in in_out:
            for char in test["input"][1]:
                self.failIf(char in change_from and char in test["output"], "Znaki nie zostaly zmienione")
            self.assertEqual(len(test["input"][0]), self.sample_length)

    def test_lab_3_gen_output_for_given_input(self):
        num_a = 9
        num_b = 1
        op = "+"
        self.assertEqual("0xa", Generator.gen_output_lab_3(num_a, num_b, op))

    def test_lab_3_gen_dict_of_inputs_and_outputs(self):
        bitness = 256
        op = "+"
        in_out = self.g.gen_tests_lab3(bitness, op)
        self.assertEqual(len(in_out), self.number_of_tests)
        for test in in_out:
            self.assertEqual(int(test['output'], 16),
                             eval(str(int(test['input'][0], 16)) + op + str(int(test['input'][1], 16))))

    def test_lab_6_gen_output_for_given_input(self):
        start = 1
        stop = 15
        num_of_steps = 100
        result = 112
        acceptable_error = 0.01

        def func(x):
            return x

        self.assertLessEqual(
            calc_relative_error(result, Generator.gen_output_lab_6(function=func, start=start, stop=stop,
                                                                   num_of_steps=num_of_steps)), acceptable_error)


class TestGrader(unittest.TestCase):
    def setUp(self):
        self.lab = "lab2"
        self.labs = ["lab1", "lab2"]
        self.root_dir = "/home/dec/studia/sem6/ak2/Grader/TEST"
        self.grader = Grader(root_dir=self.root_dir, labs=self.labs)
        self.good_student_dir = "200646"
        self.bad_student_dir = "200666"
        self.nonexistent_student_dir = "000000"

    def test_info(self):
        expected_info = "Podane drzewo katalogow: " + "/home/dec/studia/sem6/ak2/Grader/TEST" + "\n"
        expected_info.join("Laboratoria do ocenienia: " + "['lab1', 'lab2']")
        self.assertEqual(expected_info, self.grader.info)

    def test_grade_lab(self):
        self.assertTrue(self.grader.grade_lab(self.good_student_dir, self.lab))
        self.assertFalse(self.grader.grade_lab(self.bad_student_dir, self.lab))
        self.assertFalse(self.grader.grade_lab(self.nonexistent_student_dir, self.lab))

    def test_report_file_is_created(self):
        self.grader.grade_lab(self.good_student_dir, self.lab)
        report_file = os.path.join(self.root_dir, self.good_student_dir, self.lab, "Report.txt")
        self.assertTrue(os.path.isfile(report_file))

        with open(os.path.join(self.root_dir, self.good_student_dir, self.lab, "Report.txt"), "r") as output_file:
            line = output_file.readline()
            pattern = r"^\*{3} \d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2} \*{3}$"  # matches "*** dd.mm.yyyy hh:mm:ss ***"
            r = re.compile(pattern)
            self.assertTrue(r.match(line))


if __name__ == "__main__":
    unittest.main()
