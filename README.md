The goal of this `python` script is to fill grading spreadsheets downloaded from **Blackboard Learn** from information contained in PDF files's titles. This can probably be adapted to other virtual learning environments like **Moodle**.

When downloading the spreadsheet to work offline, take care of:

- Select just a column to download (the one you want to grade).
- Choose `,` as delimiter.

We must have the following things:

- A CSV file `to_grade.csv` delimited with `,` with at least three columns: 
  * The first one should contain the family name(s).
  * The second one should contain the given name(s). 
  * The last one should be the grading placeholder.
- A folder `myfolder` with all PDF files. Their names should consist of a text name (without numbers) that resembles the person's full name, i.e. given name(s) + family name(s), and a number at the end (the grade, with `,` as decimal separator and no other separator whatsoever). Like `Pepe Pérez, 3,5.pdf`. It is important that words (names and surnames) are always in the same order.

Install the requirements and run the script as follows:

```
$ python3 grading.py path/to/to_grade.csv path/to/myfolder
```

The output is a CSV file called `myfolder_graded.csv` which is like `to_grade.csv` but with the last column filled with grades.

The option `-d` prints a list of the form `file name | macthed name | score` in decreasing failure likelihood order for you to check if there are errors.

You can test this script as follows. Assuming you're at this project's root:

```
$ cd test
$ python3 ../grading.py -d to_grade.csv myfolder
$ cat myfolder_graded.csv
```

The `python` script `cutgrade.py` removes grades from file names and stores the result somewhere else. If you run `python cutgrade.py path/to/myfolder/` you get the results in the subfolder `myfolder_cut` of your current location.

You can test this second script as follows. Again, assuming you're at this project's root:

```
$ cd test
$ python3 ../cutgrade.py myfolder
$ ls myfolder_cut
```
