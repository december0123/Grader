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
        self.gen = Generator(self.num_of_samples)
        self.bitness = 512
        self.tests = self.gen.gen_samples_lab2(sample_length=15, change_from="A", change_to="*")

    @property
    def info(self):
        info = "Podane drzewo katalogow: " + self.root_dir + "\n"
        info.join("Laboratoria do ocenienia: " + str([lab for lab in self.labs]))
        return info

    def launch(self):
        for directory in os.listdir(self.root_dir):
            if os.path.isdir(os.path.join(self.root_dir, directory)):
                for lab in self.labs:
                    self.grade_lab(directory, lab)

    def grade_lab(self, student, lab):
        self.cur_dir = os.path.join(self.root_dir, student)
        build_succeeded = self.build_project(student, lab)
        if build_succeeded:
            with open(os.path.join(self.cur_dir, "Report.txt"), "a") as report:
                report.write("*** " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " ***\n")
                report.write("*** Zaczynam testowanie projektu... *** \n")
                report.flush()
                for k, v in self.tests.items():
                    ret_value = sub.Popen([self.cur_dir+"/lab2", k, "A", "*"], stdout=sub.PIPE)
                    output = ret_value.stdout.read().decode("utf-8")
                    ret_value.communicate()
                    line = "\n\nWejscie: " + k + "\nSpodziewane wyjscie: " + v
                    if v == output:
                        report.write(line + " OK")
                    else:
                        report.write(line + " BLAD\n")
                        report.write("Otrzymane wyjscie: " + output)
        return build_succeeded

    def makefile_exists(self, student_dir, lab):
        return os.path.isfile(os.path.join(self.root_dir, student_dir, lab, "makefile"))

    def build_project(self, student_dir, lab):
        self.cur_dir = os.path.join(self.root_dir, student_dir, lab)
        with open(os.path.join(self.cur_dir, "Report.txt"), "w") as report:
            report.write("*** " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " ***\n")
            report.write("*** Zaczynam budowanie projektu... *** \n")
            report.flush()
            ret_value = sub.Popen(["make", "-C" + self.cur_dir], stdout=report, stderr=report)
        ret_value.communicate()
        if ret_value.returncode == 0:
            return True
        return False
