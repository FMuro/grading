from thefuzz import process
from scipy import optimize
from scipy.sparse import csr_matrix
import numpy as np
import os
import sys
import csv
import collections
import re

# separate user-provided options and arguments (only expected argument "-d" for debug/test)
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

# We now give names to default script arguments

# CSV file with fullname;email
data = args[0]

# folder with the PDF files, whose names should be more or less the previous full names
path = args[1]

# get the list of PDF file names in path without extensions
filenames = [os.path.splitext(filename)[0] for filename in os.listdir(
    path) if filename.endswith('.pdf')]

# get dictionary whose keys are the names and whose values are the grades
names_grades_dict = {re.search("[^\d]*", filename).group(0): re.search(
    "\d*[,]?\d+", filename).group(0) for filename in filenames}


# create list of names in files
names_in_files = list(names_grades_dict.keys())

# parse CSV as list of rows and create the list of fullnames
with open(data, newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter=',')
    csv_list = list(reader)
    fullnames = [row[1]+' '+row[0] for row in csv_list]

# get the score matrix (filenames, fullnames)
rows_list = []
columns_list = []
scores_list = []
for file, count in collections.Counter(names_in_files).items():
    matches = process.extract(file, fullnames)
    for match in matches:
        rows_list.append(names_in_files.index(file))
        columns_list.append(fullnames.index(match[0]))
        scores_list.append(match[1])
rows = np.array(rows_list)
columns = np.array(columns_list)
scores = np.array(scores_list)
M = csr_matrix((scores, (rows, columns)), shape=(
    len(names_in_files), len(fullnames))).toarray()

# solve the linear sum assignment problem
[file_name_positions, full_name_positions] = optimize.linear_sum_assignment(
    M, maximize=True)
total_score = M[file_name_positions, full_name_positions].sum()

# create dictionary with name in fullname as key and name in file as value
names_dict = {fullnames[full_name_positions[i]]: names_in_files[file_name_positions[i]]
              for i in range(len(file_name_positions))}
names_dict_keys = names_dict.keys()

# create output CSV with top line link;email
output = open(os.path.basename(os.path.abspath(
    os.path.normpath(path)))+'_graded.csv', 'w')
writer = csv.writer(output, delimiter=';')

log_list=[]

for row in csv_list:
    full_name = row[1]+' '+row[0]
    if full_name in names_dict_keys:
        file_name = names_dict[full_name]
        grade = names_grades_dict[file_name]
        row[-1] = grade
        score = M[names_in_files.index(file_name),fullnames.index(full_name)]
        log_list.append([score, file_name, grade, full_name]) # log info

output = open(os.path.basename(os.path.abspath(
    os.path.normpath(path)))+'_graded.csv', 'w')
writer = csv.writer(output, delimiter=',', quotechar='"',
                    quoting=csv.QUOTE_ALL)
writer.writerows(csv_list)
output.close()

# create log file
sorted_log_list=sorted(log_list, key=lambda x:x[0]) # sort log in decreasing failiure likelyhood
with open(os.path.basename(os.path.abspath(os.path.normpath(path)))+'_grading.log', 'w') as log:
    # write log
    for item in sorted_log_list:
        log.write('---\n'+'SCORE: '+str(item[0])+'\n'+'OLD: '+item[1]+'\n'+'NEW: '+item[3]+'\n'+'GRADE: '+item[2]+'\n')
    log.close() # close log file