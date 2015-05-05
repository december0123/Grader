#!/usr/bin/python3.1
from optparse import OptionParser
import os
import sys

from grader.grader import Grader


def main():
    if len(sys.argv) <= 2:
        print("Nie ma argumentow")
        return
    parser = OptionParser()
    parser.add_option("-D", "--directory", dest="filename",
                      help="specify root directory", metavar="FILE")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    (options, args) = parser.parse_args()

    root_dir = sys.argv[1]
    labs = sys.argv[2:]
    grader = Grader(root_dir, labs)

    for directory in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir, directory)):
            for lab in labs:
                grader.grade_lab(directory, lab)


if __name__ == "__main__":
    main()
