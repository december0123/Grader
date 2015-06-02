import configparser
import datetime
import os
import subprocess as sub

from grader.generator import Generator

class Grader:
    def __init__(self, root_dir, labs, students_to_grade=[]):
        config = configparser.RawConfigParser()
        config.read(os.path.expanduser("~") + "/.grader/.mail_config")
        self.server = config.get("mail", "server")
        self.username = config.get("mail", "username")
        self.password = config.get("mail", "password")
        config.read(os.path.expanduser("~") + "/.grader/.gen_config")
        self.acceptable_error = config.getfloat("common", "acceptable_error_for_float")
        self.labs = labs
        self.root_dir = root_dir
        self.cur_dir = os.getcwd()
        self.students_to_grade = students_to_grade
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
                if (student_dir in self.students_to_grade or not self.students_to_grade) and \
                        os.path.isdir(os.path.join(self.root_dir, student_dir)):
                    for lab in self.labs:
                        points = self.grade_lab(student_dir, lab)
                        report.write("Ocenilem " + student_dir + " na " +
                                     str(points) + " punktow za " + lab + "\n")
                        print("Ocenilem " + student_dir + " na " +
                              str(points) + " punktow za " + lab + "\n")
                        # self._send_mail(self.username, student_dir + "@student.pwr.edu.pl", "TEST", "TEST PLEASE IGNORE")
        self.cur_dir = self.root_dir

    def grade_lab(self, student_dir, lab):
        self.cur_dir = os.path.join(self.root_dir, student_dir, lab)
        points = 0
        if self.build_project(student_dir):
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
                generator = Generator()
                tests = generator.gen_samples(lab)
                passed_tests = 0

                for test in tests:
                    command = [self.cur_dir + "/" + lab] + test['input']
                    popen = sub.Popen(command, stdout=sub.PIPE)
                    output = popen.stdout.read().decode("utf-8")
                    popen.communicate()
                    line = "Wejscie: " + str(test['input']) + "\nSpodziewane wyjscie: " + str(test['output'])
                    if self._relative_error(test['output'], output) <= self.acceptable_error:
                        report.write(line + " OK\n")
                        passed_tests += 1
                    else:
                        report.write(line + " BLAD\n")
                        report.write("Otrzymane wyjscie: " + str(output) + "\n")
            return passed_tests / len(tests)
        except IOError as e:
            print(e)

    def _relative_error(self, model, actual):
        import math
        try:
            return math.fabs(model - float(actual)) / model
        except ValueError as e:
            correct_letters = 0
            for i in range(0, len(model)):
                if model[i] == actual[i]:
                    correct_letters += 1
            return 1 - correct_letters / len(model)

    def _send_mail(self, FROM, TO, SUBJECT, TEXT):
        import smtplib
        message = """\
            From: From Witam <witam@witam.pl> %s
            To: To Pozdrawiam %s
            Subject: %s
            %s
            """ % (FROM, TO, SUBJECT, TEXT)
        server = smtplib.SMTP(self.server)
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(FROM, TO, "uszanowanko")
        server.quit()

    def makefile_exists(self, student_dir, lab):
        return os.path.isfile(os.path.join(self.root_dir, student_dir, lab, "makefile"))
