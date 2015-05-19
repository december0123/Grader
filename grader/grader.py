import datetime
import os
import subprocess as sub

from grader.generator import Generator


class Grader:
    def __init__(self, root_dir, labs, students=[]):
        self.labs = labs
        self.root_dir = root_dir
        self.cur_dir = os.getcwd()
        self.students = students
        self.generator = Generator()

    @property
    def info(self):
        info = "Podane drzewo katalogow: " + self.root_dir + "\n"
        info.join("Laboratoria do ocenienia: " + str(self.labs))
        return info

    def launch(self):
        with open(os.path.join(self.root_dir, "Final_Report.txt"), "w") as report:
            report.write("\n*** " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " ***\n")
            report.write("*** Raport zbiorowy *** \n")
            report.flush()
            for student_dir in os.listdir(self.root_dir):
                if (student_dir in self.students or not self.students) and \
                        os.path.isdir(os.path.join(self.root_dir, student_dir)):
                    for lab in self.labs:
                        self.grade_lab(student_dir, lab)
                        report.write(
                            "Ocenilem " + student_dir + " na " + str(self.grade_lab(student_dir, lab)) + " punktow\n")
                        print("Ocenilem " + student_dir + " na " + str(self.grade_lab(student_dir, lab)) + " punktow")
        self.cur_dir = self.root_dir

    def grade_lab(self, student_dir, lab):
        self.cur_dir = os.path.join(self.root_dir, student_dir, lab)
        build_succeeded = self.build_project(student_dir)
        points = 0
        if build_succeeded:
            points += 0.5
            try:
                points += self.test_project(lab) * 4.5
            except OSError as e:
                print(e)
        return points

    def build_project(self, student_dir):
        try:
            with open(os.path.join(self.cur_dir, "Report.txt"), "w") as report:
                report.write("\n*** " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " ***\n")
                report.write("*** Student: " + student_dir + " ***\n")
                report.write("*** Zaczynam budowanie projektu... *** \n")
                report.flush()
                popen = sub.Popen(["make", "-C" + self.cur_dir], stdout=report, stderr=report)
                popen.communicate()
                if popen.returncode == 0:
                    return True
                return False
        except IOError as e:
            print(e)
            return False

    def test_project(self, lab):
        try:
            with open(os.path.join(self.cur_dir, "Report.txt"), "a") as report:
                report.write("\n*** " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " ***\n")
                report.write("*** Zaczynam testowanie projektu... *** \n")
                report.flush()
                tests = self.generator.gen_samples(lab)
                passed_tests = 0
                for test in tests:
                    test_input = test['input']
                    test_output = test['output']
                    command = [self.cur_dir + "/" + lab] + test_input
                    popen = sub.Popen(command, stdout=sub.PIPE)
                    output = popen.stdout.read().decode("utf-8")
                    popen.communicate()
                    line = "Wejscie: " + str(list(test_input)) + "\nSpodziewane wyjscie: " + str(test_output)
                    if output == str(test_output):
                        report.write(line + " OK\n")
                        passed_tests += 1
                    else:
                        report.write(line + " BLAD\n")
                        report.write("Otrzymane wyjscie: " + output)
            return passed_tests / len(tests)
        except IOError as e:
            print(e)

    def makefile_exists(self, student_dir, lab):
        return os.path.isfile(os.path.join(self.root_dir, student_dir, lab, "makefile"))
