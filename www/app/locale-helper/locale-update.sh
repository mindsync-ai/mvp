#!/bin/bash

cd ..

pybabel update -i strings.pot -d translations -l ru -D strings
pybabel update -i strings.pot -d translations -l bg -D strings
