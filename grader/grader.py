import datetime
import os
import subprocess as sub

from grader.generator import Generator


class Grader:
    def __init__(self, root_dir, labs, students=None):
        self.labs = labs
        self.root_dir = root_dir
        self.cur_dir = root_dir
        self.students = students
        self.num_of_samples = 5
        self.sample_length = 15
        self.bitness = 512
        self.change_from = "AEIOUY"
        self.change_to = "%"
        self.generator = Generator()
        self.opt = {"lab1": None, "lab2": [self.change_from, self.change_to], "lab3": self.bitness}

    @property
    def info(self):
        info = "Podane drzewo katalogow: " + self.root_dir + "\n"
        info.join("Laboratoria do ocenienia: " + str(self.labs))
        return info

    def launch(self):
        for student_dir in os.listdir(self.root_dir):
            if os.path.isdir(os.path.join(self.root_dir, student_dir)):
                if self.students is not None:
                    if student_dir in self.students:
                        for lab in self.labs:
                            self.grade_lab(student_dir, lab)
                            print("Ocenilem " + student_dir)
                else:
                    for lab in self.labs:
                        self.grade_lab(student_dir, lab)
                        print("Ocenilem " + student_dir)
        self.cur_dir = self.root_dir

    def grade_lab(self, student_dir, lab):
        self.cur_dir = os.path.join(self.root_dir, student_dir, lab)
        build_succeeded = self.build_project()
        if build_succeeded:
            try:
                self.test_project(lab)
            except OSError as e:
                print(e)
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
            for test_input, test_output in tests.items():
                command = [self.cur_dir + "/" + lab] + list(test_input)
                popen = sub.Popen(command, stdout=sub.PIPE)
                output = popen.stdout.read().decode("utf-8")
                popen.communicate()
                line = "\n\nWejscie: " + str(list(test_input)) + "\nSpodziewane wyjscie: " + test_output
                if output == test_output:
                    report.write(line + " OK")
                else:
                    report.write(line + " BLAD\n")
                    report.write("Otrzymane wyjscie: " + output)

    def makefile_exists(self, student_dir, lab):
        return os.path.isfile(os.path.join(self.root_dir, student_dir, lab, "makefile"))
