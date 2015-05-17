import datetime
import os
import subprocess as sub

from grader.generator import Generator


class Grader:
    def __init__(self, root_dir, labs, students=None):
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
        try:
            with open(os.path.join(self.cur_dir, "Report.txt"), "w") as report:
                report.write("*** " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " ***\n")
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
                report.write("*** " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " ***\n")
                report.write("*** Zaczynam testowanie projektu... *** \n")
                report.flush()
                tests = self.generator.gen_samples(lab)
                for test in tests:
                    print(test)
                    test_input = test['input']
                    test_output = test['output']
                    command = [self.cur_dir + "/" + lab] + test_input
                    popen = sub.Popen(command, stdout=sub.PIPE)
                    output = popen.stdout.read().decode("utf-8")
                    popen.communicate()
                    line = "\n\nWejscie: " + str(list(test_input)) + "\nSpodziewane wyjscie: " + str(test_output)
                    if (float(output) if lab == "lab6" else output) == test_output:
                        print("OK")
                        report.write(line + " OK")
                    else:
                        print("BLAD")
                        print("Otrzymane wyjscie: " + output)
                        report.write(line + " BLAD\n")
                        report.write("Otrzymane wyjscie: " + output)
        except IOError as e:
            print(e)

    def makefile_exists(self, student_dir, lab):
        return os.path.isfile(os.path.join(self.root_dir, student_dir, lab, "makefile"))
