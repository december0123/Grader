#!/usr/bin/env python3
import csv
from optparse import OptionParser
import os

from grader.grader import Grader


def get_students_from_csv(csv_file):
    """
    Parses given .csv file to retrieve students' index numbers.
    Lines that contain needed numbers look like this:
    ID;_xxxINDEX_NUMBER;LAST_NAME;NAMES;x;x;xx-xxx-xxx-xx-xx-xx-xx-;;DATE_OF_BIRTH;

    :param options:
    :return: list of students
    """

    file = csv.reader(open(csv_file), delimiter=';')
    students = []
    for row in file:
        if '_' not in row[1]:
            continue
        students.append(row[1][4:])
    return students


def main():
    parser = OptionParser(usage="%prog [options] <arguments>", version="%prog 0.7")
    parser.add_option("-D", "--directory", dest="root_dir", default=os.getcwd(),
                      help="Root directory with students' directories. Defaults to current working directory.",
                      metavar="root_dir")
    parser.add_option("-L", "--lab", action="append", dest="labs", help="Lab to grade.", metavar="lab")
    parser.add_option("-C", "--csv", dest="csv_file", help=".csv file with index numbers of students to grade",
                      metavar="csv_file")
    parser.add_option("-S", "--student", action="append", dest="students", help="Student to grade.",
                      metavar="student")
    parser.add_option("-M", "--mail", action="store_true", dest="mail", default=False, help="Send emails? Boolean.",
                      metavar="Boolean")

    (options, args) = parser.parse_args()

    if options.labs is None:
        print("Nie podano laboratorium do ocenienia!")
        return -1

    students_to_grade = []
    if options.csv_file is not None:
        students_to_grade = get_students_from_csv(options.csv_file)
    if options.students is not None:
        students_to_grade.extend(options.students)
    grader = Grader(options.root_dir, options.labs, students_to_grade, options.mail)

    grader.launch()


if __name__ == "__main__":
    main()
