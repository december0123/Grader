import datetime
import os
import subprocess as sub

from grader.generator import Generator


class Grader:
    def __init__(self, root_dir, labs):
        self.labs = labs
        self.root_dir = root_dir
        self.cur_dir = root_dir
        self.num_of_samples = 5
        self.sample_length = 15
        bitness = 512
        self.change_from = "AEIOUY"
        self.change_to = "%"
        self.generator = Generator()
        self.opt = {"lab1": None, "lab2": {"change_from": self.change_from, "change_to": self.change_to}, "lab3": bitness}

    @property
    def info(self):
        info = "Podane drzewo katalogow: " + self.root_dir + "\n"
        info.join("Laboratoria do ocenienia: " + str(self.labs))
        return info

    def launch(self):
        for student_dir in os.listdir(self.root_dir):
            if os.path.isdir(os.path.join(self.root_dir, student_dir)):
                for lab in self.labs:
                    self.grade_lab(student_dir, lab)
        self.cur_dir = self.root_dir

    def grade_lab(self, student_dir, lab):
        self.cur_dir = os.path.join(self.root_dir, student_dir, lab)
        build_succeeded = self.build_project()
        if build_succeeded:
            self.test_project(lab)
        return build_succeeded

    def build_project(self):
        with open(os.path.join(self.cur_dir, "Report.txt"), "w") as report:
            report.write("*** " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " ***\n")
            report.write("*** Zaczynam budowanie projektu... *** \n")
            report.flush()
            ret_value = sub.Popen(["make", "-C" + self.cur_dir], stdout=report, stderr=report)
        ret_value.communicate()
        if ret_value.returncode == 0:
            return True
        return False

    def test_project(self, lab):
        with open(os.path.join(self.cur_dir, "Report.txt"), "a") as report:
            report.write("*** " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " ***\n")
            report.write("*** Zaczynam testowanie projektu... *** \n")
            report.flush()
            tests = self.generator.gen_samples(lab, self.opt[lab])
            for test_input, output in tests.items():
                print(test_input)
                w, i, t = test_input
                ret_value = sub.Popen([self.cur_dir + "/" + lab, w, i, t], stdout=sub.PIPE)
                output = ret_value.stdout.read().decode("utf-8")
                ret_value.communicate()
                line = "\n\nWejscie: " + w + i + t + "\nSpodziewane wyjscie: " + output
                if output == output:
                    report.write(line + " OK")
                else:
                    report.write(line + " BLAD\n")
                    report.write("Otrzymane wyjscie: " + output)

    def makefile_exists(self, student_dir, lab):
        return os.path.isfile(os.path.join(self.root_dir, student_dir, lab, "makefile"))
