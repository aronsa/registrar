#!/bin/bash
rm demo_constraints.txt
rm demo_studentprefs.txt
rm schedule.txt
perl make_random_input.pl $1 $2 $3 $4 demo_constraints.txt demo_studentprefs.txt
python3 main.py

perl is_valid.pl demo_constraints.txt demo_studentprefs.txt schedule.txt
