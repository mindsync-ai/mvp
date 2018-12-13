#!/bin/bash

echo "------------------"
echo "Extracting strings"
echo -e "------------------\n"

cd ..

pybabel extract -F babel.cfg --copyright-holder=Gamekeeper --version=2.0 --project="Gamekeeper CMS" -o strings.pot . ../../libs/db

echo -e "\nDone"