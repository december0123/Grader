#!/usr/bin/env python3.1
import csv
from optparse import OptionParser
import os

from grader.grader import Grader


def get_students(options):
    file = csv.reader(open(options.csv_file), delimiter=';')
    dummy = 0
    students = []
    for row in file:
        dummy += 1
        if dummy > 10:
            students.append(row[1][4:])
    return students


def main():
    parser = OptionParser(usage="%prog [options] <arguments>", version="%prog 0.1")
    parser.add_option("-D", "--directory", dest="root_dir", default=os.getcwd(),
                      help="Root directory with students' directories. Defaults to current working directory.",
                      metavar="root_dir")
    parser.add_option("-L", "--lab", action="append", dest="labs", help="Labs to grade.", metavar="lab")
    parser.add_option("-C", dest="csv_file", help="CSV file with index numbers of students to grade",
                      metavar="csv_file")

    (options, args) = parser.parse_args()

    if options.labs is None:
        print("Nie podano laboratorium do ocenienia!")
        return

    students = None
    if options.csv_file is not None:
        students = get_students(options)

    grader = Grader(options.root_dir, options.labs, students)
    grader.launch()

if __name__ == "__main__":
    main()
