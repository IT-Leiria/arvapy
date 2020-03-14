#!/bin/bash
cd ./docs
make html
sphinx-apidoc -f -o ./source ../
make html
cd ..
