# What does this do?

The goal of this `python` package is to fill in grading spreadsheets.

# Install

Run the following command in terminal:

```
pip install --upgrade git+https://github.com/FMuro/grading.git#egg=grading
```

Use this command to update the package too. 

# How to use

We must have the following things:

- A CSV file `to_grade.csv` delimited with `,` (configurable through options) with at least two columns: 
  
  | name       | grade |
  | ---------- | ----- |
  | Pepe Pérez |       |
  | ...        |       |

  ```
  name,grade
  Pepe Pérez,
  ...,
  ```

  
- A folder `myfolder` with all PDF files. Their names should look like `Pepe Pérez, 3,5.pdf`. Notice that the default decimal separator is `,` (configurable through options).

Run the command as follows:

```
grading --list path/to/to_grade.csv --folder path/to/myfolder
```

The output is a CSV file called `myfolder_graded.csv` which is like `to_grade.csv` but with the last column filled with grades.

You can get help by running:

```
grading -h
```

# Options

`--verbose` prints a list of the following form in decreasing failure likelihood order for you to check if there are errors

| FILE name  | MATCHED name | SCORE |
| ---------- | ------------ | ----- |
| Pepe Pérez | PEPE PEREZ   | 95    |
| ...        | ...          | ...   |

`--trim` trim degrees from names in PDF files and store them in `myfolder_trimmed`

`--delimiter DELIMITER`  CSV delimiter character. **Default is `,`** and other common options are `;` and `|`, and of course tabs, but you'd have to insert a real tab in the terminal (the way of doing that depends on the terminal).                                   

`--column COLUMN` number of column to fill with grades. It **deafults to the last one**. First column is `0`, last is `-1`, etc.

`--separator SEPARATOR` decimal separator, **default is `,`** and another common choice is `.` but it could also be `'`

`--names` when given and family names are in separate CSV columns, i.e. it looks in either of the following two ways

| GIVEN name | FAMILY name | grade |
| ---------- | ----------- | ----- |
| Pepe       | Pérez       |       |
| ...        | ...         |       |

```
GIVEN name,FAMILY name,grade
Pepe,Pérez,
...,...,
```

| FAMILY name | GIVEN name | grade |
| ----------- | ---------- | ----- |
| Pérez       | Pepe       |       |
| ...         | ...        |       |

```
FAMILY name,GIVEN name,grade
Pérez,Pepe,
...,...,
```

`--reversed` if `--names` is passed and file names look like `Pérez, Pepe, 3,5.pdf` while CSV colums look like `GIVEN name,FAMILY name,grade`, or the other way around, i.e. file names look like `Pepe Pérez, 3,5.pdf` and CSV colums look like `FAMILY name,GIVEN name,grade`

# Testing

You can test this package by downloading the `test` folder and running the following commands:

```
cd test
grading -v -t -n -l to_grade.csv -f myfolder
cat myfolder_graded.csv
ls myfolder_trimmed
grading -v -t -n -s . -l to_grade.csv -f myfolder_dot
cat myfolder_dot_graded.csv
ls myfolder_dot_trimmed
grading -v -t -n -s "'" -l to_grade.csv -f myfolder_apostrophe
cat myfolder_apostrophe_graded.csv
ls myfolder_apostrophe_trimmed
grading -v -n -d ";" -l to_grade_semicolon.csv -f myfolder
cat myfolder_graded.csv
grading -v -n -d "|" -l to_grade_bar.csv -f myfolder
cat myfolder_graded.csv
grading -v -n -d "	" -l to_grade_tab.csv -f myfolder
cat myfolder_graded.csv
```

# Warning

If your files are called like `Pérez, Pepe, 3,5.pdf` and your CSV file has a single names column which look like `Pepe Pérez` this script won't match names reliably. The same if files look like `Pepe Pérez, 3,5.pdf` and the CSV names column looks like `Pérez, Pepe`. Something like this can only be solved when family and given names are in separate columns and you use the options `--names --reversed`.

# Remove

```
pip uninstall grading
```