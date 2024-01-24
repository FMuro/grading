import os
import sys
import csv
import re
from libmatching.libmatching import PDF_names, best_matches

# CLI arguments

parser = argparse.ArgumentParser(
    prog='grading',
    description='Fill Blackboard Learn grading spreadsheets from PDF file names',
    epilog='Enjoy your teaching admin!')

parser.add_argument('-l', '--list', help='CSV file with columns name,surname,grade')
parser.add_argument('-f', '--folder', help="folder containing the PDF files called like 'Pepe Pérez, 3,5.pdf'")
parser.add_argument('-v', '--verbose', action='store_true',
                    help='print matching list with scores')

args = parser.parse_args()

def funcion():
    # CSV file with realname;email
    data = args.list

    # folder with the PDF files, whose names should be more or less the previous full names
    path = args.folder

    # get the list of PDF file names (without extension) in path
    filenames = PDF_names(path)

    # get dictionary whose keys are the names and whose values are the grades
    names_grades_dict = {re.search("[^\d|,]*", filename).group(0): re.search(
        "\d*[,]?\d+", filename).group(0) for filename in filenames}


    # create list of names in files
    names_in_files = list(names_grades_dict.keys())

    # parse CSV as list of rows and create the list of real names
    with open(data, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=',')
        csv_list = list(reader)

    # full name from CSV joining first and second column
    def full_name(row):
        return row[0]+' '+row[1]

    realnames = [full_name(row) for row in csv_list]

    # create best match list and dictionary for filenames and realnames
    # elements of the list are of the form [filename, best realname match, score]
    # the dictionary is of the form {best realname match: filename}
    matches_list, names_dict = best_matches(names_in_files, realnames)
    names_dict_keys = names_dict.keys()

    # print log if verbose mode is on ("-v" option) in decreasing failure likelihood order
    if args.verbose:
        sorted_log_list = sorted(matches_list, key=lambda x: x[2])
        for match in sorted_log_list:
            print(*match, sep=' | ')

    # fill grades in list

    for row in csv_list:
        realname = full_name(row)
        if realname in names_dict_keys:
            file_name = names_dict[realname]
            grade = names_grades_dict[file_name]
            row[-1] = grade

    # create output CSV with grade 3rd column filled in
    output = open(os.path.basename(os.path.abspath(
        os.path.normpath(path)))+'_graded.csv', 'w')
    writer = csv.writer(output, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_ALL)
    writer.writerows(csv_list)
    output.close()