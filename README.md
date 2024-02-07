# What does this do?

The goal of this `python` package is to fill grading spreadsheets downloaded from **Blackboard Learn** from information contained in PDF files's titles. This can probably be adapted to other virtual learning environments like **Moodle**.

# Install

Run the following command in terminal:

```
pip install --upgrade git+https://github.com/FMuro/grading.git#egg=grading
```

Use this command to update the package too. 

# How to use

When downloading the spreadsheet to work offline, take care of:

- Select just a column to download (the one you want to grade).
- Choose `,` as delimiter.

We must have the following things:

- A CSV file `to_grade.csv` delimited with `,` with at least three columns: 
  * The first one should contain the family name.
  * The second one should contain the given name. 
  * The last one should be the grading placeholder.
- A folder `myfolder` with all PDF files. Their names should consist of a text name (without numbers) that resembles the person's full name, i.e. family name + given name, and a number at the end (the grade, with `,` as decimal separator and no other separator whatsoever). Like `Pérez Pepe, 3,5.pdf`. It is important that words (names and surnames) are always in the same order.

Install the requirements and run the package as follows:

```
$ grading --list path/to/to_grade.csv --folder path/to/myfolder
```

The output is a CSV file called `myfolder_graded.csv` which is like `to_grade.csv` but with the last column filled with grades.

The option `-v` prints a list of the form `file name | matched name | score` in decreasing failure likelihood order for you to check if there are errors.

The option `-t` removes grades from file names and stores them in `myfolder_trimmed` within your current location.

You can get help by running:

```
$ grading -h
```

# Testing

You can test this package by downloading the `test` folder and running the following commands:

```
$ cd test
$ grading -v -t -l to_grade.csv -f myfolder
$ cat myfolder_graded.csv
$ ls myfolder_trimmed
```