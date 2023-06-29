import os
import sys
import shutil
import re

# get path (the only option)
path=sys.argv[1]

#output folder name
output_folder=os.path.basename(os.path.abspath(
    os.path.normpath(path)))+'_cut'

# get the list of PDF file names in path without extensions
filenames = [os.path.splitext(filename)[0] for filename in os.listdir(
    path) if filename.endswith('.pdf')]

# create subfolder called 'normalized' if it doesn't already exist
os.makedirs(output_folder, exist_ok=True)

# copy files without grades to subfolder
for filename in filenames:
    shutil.copy(os.path.join(path, filename+'.pdf'), os.path.join(output_folder,re.search("[^\d]*", filename).group(0)+'.pdf'))