#!/usr/bin/env python3.1
from optparse import OptionParser
import os

from grader.grader import Grader


def main():
    parser = OptionParser(usage="%prog [options] <arguments>", version="%prog 0.1")
    parser.add_option("-D", "--directory", dest="root_dir", default=os.getcwd(),
                      help="Root directory with students' directories. Defaults to current working directory.",
                      metavar="root_dir")
    parser.add_option("-L", "--lab", action="append", dest="labs", help="Labs to grade.", metavar="lab")
    parser.add_option("-C", dest="csv_list", help="CSV file with index numbers of students to grade",
                      metavar="csv_file")

    (options, args) = parser.parse_args()

    if options.labs is None:
        print("Nie podano laboratorium do ocenienia!")
        return
    else:
        print("Root = ", options.root_dir)
        print("Labs = ", options.labs)

    grader = Grader(options.root_dir, options.labs)
    grader.launch()

if __name__ == "__main__":
    main()
