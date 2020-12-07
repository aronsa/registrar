#!/bin/sh

cp $1 demo_constraints.txt 
cp $2 demo_studentprefs.txt
python3 main.py
perl is_valid.pl demo_constraints.txt demo_studentprefs.txt schedule.txt
cp schedule.txt $3
