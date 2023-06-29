#!/bin/zsh
mkdir $1_cut
for x in $1/*.pdf
do
    filename=$(basename $x)
    echo "mv $filename ${filename/[0-9]*/}.pdf"
done