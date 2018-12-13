#!/bin/bash

echo "------------------"
echo "Initializing strings"
echo -e "------------------\n"

cd ..

pybabel init -i strings.pot -d translations -l ru -D strings
pybabel init -i strings.pot -d translations -l bg -D strings

echo -e "\nDone"