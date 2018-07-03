#!/bin/bash

python ./tester.py -i grammars/self.txt

for entry in "tests/positive"/*
do
    python tester.py -i "$entry" --grammar-check
    if [ $? -eq 0 ]
    then
      echo "OK $entry"
    else
      echo "FAILED $entry"
    fi
done

for entry in "tests/negative"/*
do
    python tester.py -i "$entry" --grammar-check
    if [ $? -eq 0 ]
    then
      echo "FAILED $entry"
    else
      echo "OK $entry"
    fi
done