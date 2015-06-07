import configparser
import datetime
import os
import re
import subprocess as sub

from grader.generator import Generator
from grader.utilities import calc_relative_error

class Grader:
    def __init__(self, root_dir, labs, students_to_grade=[]):
        config = configparser.RawConfigParser()
        config.read(os.path.expanduser("~") + "/.grader/.mail_config")
        self.server = config.get("mail", "server")
        self.username = config.get("mail", "username")
        self.password = config.get("mail", "password")
        config.read(os.path.expanduser("~") + "/.grader/.gen_config")
        self.acceptable_error = config.getfloat("common", "acceptable_error")
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
            report.write("*** " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " ***\n")
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
                        # self.send_mail(self.username, student_dir + "@student.pwr.edu.pl", "TEST", "TEST PLEASE IGNORE")
        print("**************************************************************")
        print("Zakonczono ocenianie. Raport zbiorowy znajduje sie w pliku: ")
        print(os.path.join(self.root_dir, "Final_Report.txt"))
        print("Szczegolowe informacje znajduja sie w katalogach z zadaniami.")
        print("**************************************************************")
        self.cur_dir = self.root_dir

    def grade_lab(self, student_dir, lab):
        self.cur_dir = os.path.join(self.root_dir, student_dir, lab)
        points = 0
        try:
            if self.build_project(student_dir):
                points = self.test_project(lab)

            with open(os.path.join(self.cur_dir, "Report.txt"), "a") as report:
                report.write("\n*** " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " ***\n")
                report.write("*** Zdobyte punkty ***\n")
                report.write(str(points))
                report.flush()
        except OSError as e:
            print("Zgloszono wyjatek o tresci: ", e)
        except IOError as e:
            print("Zgloszono wyjatek o tresci: ", e)
        return points

    def build_project(self, student_dir):
        with open(os.path.join(self.cur_dir, "Report.txt"), "w") as report:
            report.write("*** " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " ***\n")
            report.write("*** Student: " + student_dir + " ***\n")
            report.write("*** Zaczynam budowanie projektu... *** \n")
            report.flush()
            popen = sub.Popen(["make", "-C" + self.cur_dir], stdout=report, stderr=report)
            popen.communicate()
            if popen.returncode == 0:
                return True
        return False

    def test_project(self, lab):
        with open(os.path.join(self.cur_dir, "Report.txt"), "a") as report:
            report.write("\n*** " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " ***\n")
            report.write("*** Zaczynam testowanie projektu... *** \n")
            report.flush()

            tests = self.generator.gen_samples(lab)
            passed_tests = 0

            for test in tests:
                # print(test['input'])
                # print(test['output'])
                command = [self.cur_dir + "/" + lab] + test['input']
                popen = sub.Popen(command, stdout=sub.PIPE)
                output = popen.stdout.read().decode("utf-8")
                # print(output)
                popen.communicate()
                line = "\nWejscie: " + str(test['input']) + "\nSpodziewane wyjscie: " + str(test['output'])
                if lab != "lab7":
                    if calc_relative_error(test['output'], output) <= self.acceptable_error:
                        report.write(line + " OK\n")
                        passed_tests += 1
                    else:
                        report.write(line + " BLAD\n")
                        report.write("Otrzymane wyjscie: " + str(output) + "\n")
                else:
                    # such regexp
                    # wow
                    # matches "SOMETHING: POSSIBLY_FLOATING_POINT_NUMBER SOMETHING: INTEGER"
                    regexp = re.compile(r"(.*:\s)(\d+\.?\d+?)\s(.*:\s)(\d+)")
                    m = re.match(regexp, output)
                    if calc_relative_error(test['output'], m.group(2)) <= self.acceptable_error:
                        report.write(line + " OK\n")
                        passed_tests += 0.5
                    else:
                        report.write(line + " BLAD\n")
                        report.write("Otrzymane wyjscie: " + str(output) + "\n")
                    cycles = float(m.group(4))
                    if cycles <= 10e6:
                        passed_tests += 0.5
                        report.write("+0.5 pkt za liczbe cykli w granicy 10e6.\n")
                    elif cycles <= 10e9:
                        passed_tests += 0.3
                        report.write("+0.3 pkt za liczbe cykli w granicy 10e9.\n")
                    elif cycles <= 10e12:
                        passed_tests += 0.1
                        report.write("+0.1 pkt za liczbe cykli w granicy 10e12.\n")
                    else:
                        report.write("0 pkt za liczbe cykli przekraczajaca 10e12.\n")
            points = 4.5 * (passed_tests / len(tests)) + 0.5  # + 0.5 for successful build
        return points

    def send_mail(self, FROM, TO, SUBJECT, TEXT):
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


