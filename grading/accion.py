import os
import csv
import re
import shutil
from matching import PDF_names, best_matches, sorted_table
import argparse
import sys

# CLI arguments

parser = argparse.ArgumentParser(
    prog='grading',
    description='Fill grading spreadsheets from PDF file names',
    epilog='Enjoy your teaching admin!')

parser.add_argument('-l', '--list', help='CSV file to fill with colums: name, grade (see also -c, -s, -sr options)')
parser.add_argument('-f', '--folder', help="folder containing the PDF files called like 'Pepe Pérez, 3,5.pdf'", required=True)
parser.add_argument('-v', '--verbose', action='store_true',
                    help='print matching list with scores')
parser.add_argument('-t', '--trim', action='store_true',
                    help='trim degrees from names in PDF files')
parser.add_argument('-d', '--delimiter', help="CSV delimiter character (default: ,)", default=',')
parser.add_argument('-c', '--column', help="CSV number of column to fill with grades (first column is 0, last is -1, default: -1)", default='-1', type=int)
parser.add_argument('-s', '--separator', help="decimal separator (default: ,)", default=',')
parser.add_argument('-r', '--reversed', help="PDF file names are FAMILY + GIVEN but first CSV columns are GIVEN, FAMILY or the other way around", action='store_true')
parser.add_argument('-n', '--names', help="given and family names in separate CSV columns (the first two ones)", action='store_true', required='--reversed' in sys.argv)

args = parser.parse_args()


def grade_spreadsheet():
    # CSV file with realname;email
    data = args.list

    # folder with the PDF files, whose names should be more or less the previous full names
    path = args.folder

    # get the list of PDF file names (without extension) in path
    filenames = PDF_names(path)

    # fill grades in CSV file if provided
    # it need not be provided if you just want to trim the degrees from the PDF file names
    if data is not None:

        # get dictionary whose keys are the names and whose values are the grades
        names_grades_dict = {re.search("[^\d|,|;|"+args.separator+"]*", filename).group(0): re.search(
            "\d*["+args.separator+"]?\d+", filename).group(0) for filename in filenames}

        # create list of names in files
        names_in_files = list(names_grades_dict.keys())

        # parse CSV as list of rows and create the list of real names
        with open(data, newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter=args.delimiter)
            csv_list = list(reader)

        # full name from CSV joining first and second column
        def full_name(row):
            if args.names: # CSV with GIVEN name and FAMILY name in separate columns (the first two ones)
                if args.reversed: # FAMILY name and GIVEN name are in reversed order in CSV with respect to PDFs
                    return row[1]+' '+row[0]
                else:
                    return row[0]+' '+row[1]
            else: # CSV: full name
                return row[0].replace(',','').replace(';','') # remove possible , and ;

        realnames = [full_name(row) for row in csv_list]

        # create best match list and dictionary for filenames and realnames
        # elements of the list are of the form [filename, best realname match, score]
        # the dictionary is of the form {best realname match: filename}
        matches_list, names_dict = best_matches(names_in_files, realnames)
        names_dict_keys = names_dict.keys()

        # print log if verbose mode is on ("-v" option) in decreasing failure likelihood order
        if args.verbose:
            sorted_table(matches_list, old_name="FILE name", new_name="MATCHED name")

        # fill grades in list

        for row in csv_list:
            realname = full_name(row)
            if realname in names_dict_keys:
                file_name = names_dict[realname]
                grade = names_grades_dict[file_name]
                row[args.column] = grade

        # create output CSV with grade args.column filled in
        output = open(os.path.basename(os.path.abspath(
            os.path.normpath(path)))+'_graded.csv', 'w')
        writer = csv.writer(output, delimiter=args.delimiter, quotechar='"',
                            quoting=csv.QUOTE_ALL)
        writer.writerows(csv_list)
        output.close()

        # Indicate output CSV file
        print('\nGrades filled in CSV file:', output.name)

    if args.trim:

        # output folder name
        output_folder = os.path.basename(
            os.path.abspath(os.path.normpath(path)))+'_trimmed'

        # create output folder
        os.makedirs(output_folder, exist_ok=True)

        # copy files without grades to output folder
        for filename in filenames:
            shutil.copy(os.path.join(path, filename+'.pdf'), os.path.join(
                output_folder, re.search("[^\d|,|;|"+args.separator+"]*", filename).group(0)+'.pdf')) # remove numbers and , and ;
        
        # Indicate output folder
        print('\nPDF files without grades copied to folder:', output_folder)