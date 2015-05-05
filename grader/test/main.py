#!/usr/bin/env python3.1
__author__ = 'dec'

from grader.grader import Grader
from grader.generator import Generator
import os
import re
import unittest


class TestGrader(unittest.TestCase):
    def setUp(self):
        self.lab = "lab1"
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

    def test_check_if_makefile_exists(self):
        good_path = os.path.join(self.root_dir, self.good_student_dir)
        bad_path = os.path.join(self.root_dir, self.bad_student_dir)
        self.assertTrue(self.grader.makefile_exists(good_path, self.lab))
        self.assertFalse(self.grader.makefile_exists(bad_path, self.lab))

    '''
    def test_build_project(self):
        self.assertTrue(self.grader.grade_lab(self.good_student_dir, self.lab))
        self.assertFalse(self.grader.grade_lab(self.bad_student_dir, self.lab))
        self.assertRaises(IOError, self.grader.build_project, self.nonexistent_student_dir, self.lab)
    '''
    def test_grade_student_lab(self):
        passed = self.grader.grade_lab(self.good_student_dir, self.lab)
        self.assertTrue(passed)
        passed = self.grader.grade_lab(self.bad_student_dir, self.lab)
        self.assertFalse(passed)

        build_output_file = os.path.join(self.root_dir, self.good_student_dir, self.lab, "Build_Output")
        self.assertTrue(os.path.isfile(build_output_file))

        with open(os.path.join(self.root_dir, self.good_student_dir, self.lab, "Build_Output"), "r") as output_file:
            line = output_file.readline()
            pattern = r"^\*{3} \d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2} \*{3}$"  # matches "*** dd.mm.yyyy hh:mm:ss ***"
            r = re.compile(pattern)
            self.assertTrue(r.match(line))


class TestGenerator(unittest.TestCase):

    def setUp(self):
        self.num_of_samples = 7
        self.sample_length = 7
        self.g = Generator()

    def test_lab_1_gen_output_for_given_input(self):
        input_string = "test"
        self.assertEqual(input_string, Generator.gen_output_lab_1(input_string))

    def test_lab_1_gen_dict_of_inputs_and_outputs(self):
        in_out = self.g.gen_samples("lab1")
        self.assertEqual(len(in_out), self.num_of_samples)
        for k, v in in_out.items():
            self.assertEqual(k, v)
            self.assertEqual(len(k), self.sample_length)

    def test_lab_2_gen_output_for_given_input(self):
        input_string = "test string WITH lower ANd UppER Case leTTERS"
        output_string = "t*st str*ng W*TH l*w*r *Nd *pp*R C*s* l*TT*RS"
        change_from = "AEIOUYaeiouy"
        change_into = "*"
        self.assertEqual(output_string, Generator.gen_output_lab_2(input_string, change_from, change_into))

    def test_lab_2_gen_dict_of_inputs_and_outputs(self):
        change_from = "AIEUOY"
        change_into = "&"
        in_out = self.g.gen_samples("lab2", (change_from, change_into))
        self.assertEqual(len(in_out), self.g.num_of_samples)
        for test_input, test_output in in_out.items():
            for char in test_input:
                self.failIf(char in change_from and char in test_output, "witam")
            self.assertEqual(test_input(test_input), self.sample_length)

    def test_lab_3_gen_output_for_given_input(self):
        num_a = (2**256) - 1
        num_b = 7
        self.assertEqual(num_a + num_b, Generator.gen_output_lab_3(num_a, num_b))

    def test_lab_3_gen_dict_of_inputs_and_outputs(self):
        bitness = 256
        in_out = self.g.gen_samples("lab3", bitness)
        self.assertEqual(len(in_out), self.num_of_samples)
        for key, value in in_out.items():
            self.assertEqual(key[0] + key[1], value)

if __name__ == "__main__":
    unittest.main()
