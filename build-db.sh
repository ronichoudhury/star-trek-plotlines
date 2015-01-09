#!/bin/sh

python=${PYTHON}
if [ -z ${python} ]; then
    python="python"
fi

cd database
${python} startrek.py "../data/Star Trek Plotlines - Episodes.csv" "../data/Star Trek Plotlines - People.csv" "../data/Star Trek Plotlines - Plots.csv"
